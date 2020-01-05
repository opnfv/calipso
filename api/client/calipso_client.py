import requests
import json
import time
from datetime import datetime
import argparse

try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning
    urllib3.disable_warnings(InsecureRequestWarning)

from six.moves.urllib.parse import urljoin
from sys import exit

# This is a calipso api client designed to be small and simple
# assuming environment_config details are already deployed by CVIM (typically: cvim-<mgmt_hostname>)
# For central CVIM monitoring add this client per pod scanning and allow adding multiple environments


class CalipsoClient:

    def __init__(self, api_host, api_port, api_password, es_index=False, verify_tls=False):
        self.api_server = api_host
        self.username = "calipso"
        self.password = api_password
        self.port = api_port
        self.schema = "https"
        self.es_index = es_index
        self.verify_tls = verify_tls
        self.auth_url = "auth/tokens"
        self.headers = {'Content-Type': 'application/json'}
        self.token = None
        self.auth_body = {
            "auth": {
                "methods": ["credentials"],
                "credentials": {
                    "username": self.username,
                    "password": self.password
                }
            }
        }

    @property
    def base_url(self):
        return "{}://{}:{}".format(self.schema, self.api_server, self.port)

    def get_token(self):
        try:
            resp = self.send_request("POST", self.auth_url, payload=self.auth_body)
            cont = resp.json()
            if "token" not in cont:
                fatal("Failed to fetch auth token. Response:\n{}".format(cont))
            self.token = cont["token"]
            self.headers.update({'X-Auth-Token': self.token})
            return self.token
        except requests.exceptions.RequestException as e:
            fatal("Error sending request: {}".format(e))

    @staticmethod
    def pp_json(json_text, sort=True, indents=4):
        json_data = json.loads(json_text) if type(json_text) is str else json_text
        print(json.dumps(json_data, sort_keys=sort, indent=indents))

    def _send_request(self, method, url, payload):
        method = method.lower()
        if method == 'post':
            response = requests.post(url, json=payload, headers=self.headers, verify=self.verify_tls,
                                     timeout=3)
        elif method == 'delete':
            response = requests.delete(url, headers=self.headers, verify=self.verify_tls)
        elif method == 'put':
            response = requests.put(url, json=payload, headers=self.headers, verify=self.verify_tls,
                                    timeout=3)
        else:
            response = requests.get(url, params=payload, headers=self.headers, verify=self.verify_tls,
                                    timeout=3)
        return response

    def send_request(self, method, url, payload):
        try:
            return self._send_request(method, urljoin(self.base_url, url), payload)
        except requests.ConnectionError:
            fatal("SSL Connection could not be established")

    def call_api(self, method, endpoint, payload=None, fail_on_error=True):
        if not self.token:
            self.get_token()

        response = self.send_request(method, endpoint, payload)

        if response.status_code == 404:
            fatal("Endpoint or payload item not found")
        elif response.status_code == 400:
            fatal("Environment or resource not found, or invalid keys. "
                  "Response: {}".format(response.content))

        content = json.loads(response.content)
        if 'error' in content and fail_on_error:
            fatal(content['error'])
        return content

    def scan_handler(self, environment):
        # post scan request, for specific environment, get doc_id
        scan_reply = self.scan_request(environment=environment)
        print("Scan request posted for environment {}".format(environment))
        scan_doc_id = scan_reply["id"]
        # check status of scan id and wait till scan status is 'completed'
        scan_status = "pending"
        while scan_status != "completed" and scan_status != "completed_with_errors":
            scan_doc = self.scan_check(environment=environment,
                                     doc_id=scan_doc_id)
            scan_status = scan_doc["status"]
            print("Wait for scan to complete, scan status: {}".format(scan_status))
            time.sleep(2)
            if scan_status == "failed":
                fatal("Scan has failed, please debug in scan container")
        if scan_status == "completed_with_errors":
            print("Inventory, links and cliques has been discovered with some errors")
        elif scan_status == "completed":
            print("Inventory, links and cliques has been discovered")
        else:
            exit(0)

    def scan_request(self, environment, freq="NOW"):
        if freq == "NOW":
            request_payload = {
                "log_level": "warning",
                "clear": True,
                "scan_only_inventory": False,
                "scan_only_links": False,
                "scan_only_cliques": False,
                "env_name": environment,
                "es_index": self.es_index
            }
            return self.call_api('post', 'scans', request_payload)
        else:
            request_payload = {
                "freq": freq,
                "log_level": "warning",
                "clear": True,
                "scan_only_links": False,
                "scan_only_cliques": False,
                "env_name": environment,
                "es_index": self.es_index,
                "scan_only_inventory": False,
                "submit_timestamp": datetime.now().isoformat()
            }
            return self.call_api('post', 'scheduled_scans', request_payload)

    def scan_check(self, environment, doc_id, scheduled=False):
        scan_params = {"env_name": environment, "id": doc_id}
        if scheduled is False:
            return self.call_api('get', 'scans', scan_params)
        else:
            return self.call_api('get', 'scheduled_scans', scan_params)


def fatal(err):
    print(err)
    exit(1)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_server",
                        help="FQDN or IP address of the API Server"
                             " (default=localhost)",
                        type=str,
                        default="localhost",
                        required=False)
    parser.add_argument("--api_port",
                        help="TCP Port exposed on the API Server "
                             " (default=8747)",
                        type=int,
                        default=8747,
                        required=False)
    parser.add_argument("--api_password",
                        help="API password (secret) used by the API Server "
                             " (default=calipso_default)",
                        type=str,
                        default="calipso_default",
                        required=False)
    parser.add_argument("--environment",
                        help="specify environment(pod) name configured on the API server"
                             " (default=None)",
                        type=str,
                        default=None,
                        required=False)
    parser.add_argument("--scan",
                        help="actively discover the specific cloud environment -"
                             " options: NOW/HOURLY/DAILY/WEEKLY/MONTHLY/YEARLY"
                             " (default=None)",
                        type=str,
                        default=None,
                        required=False)
    parser.add_argument("--method",
                        help="method to use on the API server -"
                             " options: get/post/delete/put"
                             " (default=None)",
                        type=str.lower,
                        default=None,
                        required=False)
    parser.add_argument("--endpoint",
                        help="endpoint url extension to use on the API server -"
                             " options: please see API documentation for endpoints"
                             " (default=None)",
                        type=str,
                        default=None,
                        required=False)
    parser.add_argument("--es_index",
                        help="index environment inventory, links and cliques on ElasticSearch DB"
                             " options: boolean, add argument or not"
                             " (default=False)",
                        action='store_true',
                        default=False,
                        required=False)
    parser.add_argument("--payload",
                        help="dict string with parameters to send to the API -"
                             " options: please see API documentation per endpoint"
                             " (default=None)",
                        type=str,
                        default=None,
                        required=False)
    parser.add_argument("--verify_tls",
                        help="verify full certificate chain from server -"
                             " options: boolean, add option or not"
                             " (default=False)",
                        action='store_true',
                        default=False,
                        required=False)
    parser.add_argument("--page",
                        help="a page number for retrieval"
                             " (default=0)",
                        type=int,
                        default=0,
                        required=False)
    parser.add_argument("--page_size",
                        help="a number of total objects listed per page" 
                             " (default=1000)",
                        type=int,
                        default=1000,
                        required=False)
    parser.add_argument("--guide",
                        help="get a reply back with API guide location",
                        dest='guide',
                        default=False,
                        action='store_true',
                        required=False)

    parser.add_argument("--version",
                        help="get a reply back with calipso_client version",
                        action='version',
                        default=None,
                        version='%(prog)s version: 0.6.8')

    args = parser.parse_args()

    if args.guide:
        guide_url = "https://cloud-gogs.cisco.com/mercury/calipso/src/master/docs/release/api-guide.rst"
        print("wget/curl from: {}".format(guide_url))
        exit(0)

    cc = CalipsoClient(args.api_server, args.api_port, args.api_password, args.es_index, args.verify_tls)
    per_environment_collections = ["inventory", "cliques", "links", "messages",
                                   "scans", "scheduled_scans"]

    if (args.es_index is True) and (args.scan is None):
        fatal("es_index should only be used with --scan requests")

    # currently, only environment_configs and constants allowed without environment
    if args.endpoint in per_environment_collections and args.environment is None:
        fatal("This request requires an environment")
    if args.endpoint == "environment_configs" or args.endpoint == "constants":
        if args.method is None:
            fatal("Method is needed for this type of request")
        if args.environment is not None:
            fatal("Environment not needed for this request, please remove")
        if args.payload:  # case for a specific environment or specific constant
            payload_str = args.payload.replace("'", "\"")
            payload_json = json.loads(payload_str)
            env_reply = cc.call_api(args.method, args.endpoint, payload_json)
        else:  # case for all environments
            env_reply = cc.call_api(args.method, args.endpoint)
        cc.pp_json(env_reply)
        exit(0)

    scan_options = ["NOW", "HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"]
    if args.scan is not None:
        if args.environment is None:
            fatal("Scan request requires an environment")
        if args.scan not in scan_options:
            fatal("Unaccepted scan option, use --help for more details")
        if args.method is not None:
            fatal("Method not needed for scan requests, please remove")
        if args.payload is not None:
            fatal("Payload not needed for scan requests, please remove")
        if args.endpoint is not None:
            fatal("Endpoint not needed for scan requests, please remove")
        else:
            if args.scan == "NOW":
                cc.scan_handler(environment=args.environment)
            else:
                # post scan schedule, for specific environment, get doc_id
                schedule_reply = cc.scan_request(environment=args.environment,
                                                 freq=args.scan)
                schedule_doc_id = schedule_reply["id"]
                time.sleep(2)
                schedule_doc = cc.scan_check(environment=args.environment,
                                             doc_id=schedule_doc_id,
                                             scheduled=True)
                print("Scheduled scan at: {}\nSubmitted at: {}\nScan frequency: {}"
                      .format(schedule_doc['scheduled_timestamp'], schedule_doc['submit_timestamp'], schedule_doc['freq']))
            exit(0)

    if args.environment is not None and args.endpoint not in per_environment_collections:
        fatal("Environment is not needed for this request, please remove")

    #  generic request for items from any endpoint using any method, per environment
    if args.endpoint is None or args.method is None:
        fatal("Endpoint and method are needed for this type of request")
    method_options = ["get", "post", "delete", "put"]
    if args.method not in method_options:
        fatal("Unaccepted method option, use --help for more details")
    if not isinstance(args.page, int) or not isinstance(args.page, int):
        fatal("Unaccepted page or page_size (must be a number")
    params = {"env_name": args.environment, "page": args.page,
              "page_size": args.page_size} if args.environment is not None else {}
    if args.payload:
        payload_str = args.payload.replace("'", "\"")
        try:
            payload_json = json.loads(payload_str)
            params.update(payload_json)
        except ValueError as e:
            fatal("unsupported payload data {}, should follow JSON formatting".format(e))
    reply = cc.call_api(args.method, args.endpoint, params)
    cc.pp_json(reply)
    exit(0)


if __name__ == "__main__":
    run()

# examples of running client with some arguments:
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --endpoint environment_configs
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --endpoint environment_configs --payload "{'name': 'staging'}"
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --environment staging --scan NOW
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --environment staging --scan WEEKLY
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --environment staging --endpoint messages
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --environment staging --endpoint messages --payload "{'id': '17678.55917.5562'}"
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --environment staging --endpoint scans
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --environment staging --method get --endpoint scans --payload "{'id': '5cd2c6de01b845000dbaf0d9'}"
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --environment staging --endpoint inventory
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --environment staging --endpoint inventory --payload "{'page_size': '2000'}"
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --environment staging --endpoint links
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --environment staging --endpoint links --payload "{'id': '5cd2aa2699bb0dc9c2f9021f'}"
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --environment staging --endpoint cliques
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --environment staging --endpoint cliques --payload "{'id': '5cd2aa3199bb0dc9c2f911fc'}"
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --environment staging --endpoint scheduled_scans
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --environment staging --endpoint scheduled_scans --payload "{'id': '5cd2aad401b845000d186174'}"
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --environment staging --endpoint inventory --payload "{'id': '01776a49-a522-41ab-ab7c-94f4297c4227'}"
# --api_server korlev-calipso-testing.cisco.com --api_port 8747 --method get --environment staging --endpoint inventory --payload "{'type': 'instance', 'page_size': '1500'}"
# --api_server korlev-calipso-testing.cisco.com --api_password bxLkRiwCkk6xyXMS --method get --endpoint constants --payload "{'name': 'link_types'}"
# --api_server korlev-calipso-testing.cisco.com --api_password bxLkRiwCkk6xyXMS --method get --endpoint constants --payload "{'name': 'object_types'}"
