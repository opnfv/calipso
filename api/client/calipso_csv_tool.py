from calipso_client import CalipsoClient
import csv
import argparse
import dateutil.parser
from datetime import datetime


class CalipsoCsvTool:

    def __init__(self):
        self.filename = "sprint_data.csv"
        self.csv_columns = ["ENVIRONMENT", "PROJECT_NAME", "CPU_QUOTA",
                            "MEM_QUOTA", "HOST", "NAME", "NETWORK",
                            "FLAVOR_NAME", "CPU", "MEMORY", "DISK",
                            "STATUS", "POWER_STATE",
                            "DAYS_SINCE_CREATED", "INSTANCE_UUID"]

    def write_dicts_to_csv(self, att_list, env):
        try:
            filename = "{}_{}".format(env, self.filename)
            cf = open(filename, "w+")
            writer = csv.DictWriter(cf, fieldnames=self.csv_columns)
            writer.writeheader()
            for att in att_list:
                writer.writerow(att)
            cf.close()
            return True
        except IOError:
            return False


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
                             " - typically 'cvim-<mgmt_hostname>'"
                             " (default=None)",
                        type=str,
                        default=None,
                        required=True)
    parser.add_argument("--scan_first",
                        help="scan environment if not scanned earlier (slower)"
                             " options: boolean, add argument or not"
                             " (default=False)",
                        action='store_true',
                        default=False,
                        required=False)
    parser.add_argument("--version",
                        help="get a reply back with csv_tool version",
                        action='version',
                        default=None,
                        version='%(prog)s version: 0.6.8')

    args = parser.parse_args()

    cc = CalipsoClient(args.api_server, args.api_port, args.api_password, False)
    if args.scan_first:
        print("\nSCAN initiated NOW using calipso_client, wait until completed...")
        cc.scan_handler(environment=args.environment)
    instances = cc.call_api("get", "inventory",
                            payload={"env_name": args.environment, "type": "instance"})["objects"]
    attributes_list = []
    for i in instances:
        instance_id = i["id"]
        instance = cc.call_api("get", "inventory",
                               payload={"env_name": args.environment, "id": instance_id})
        project_id = instance["project_id"]
        project = cc.call_api("get", "inventory",
                              payload={"env_name": args.environment, "id": project_id})
        quota_set = project["quota_set"]
        cores_limit = quota_set["cores"]["limit"]
        ram_limit = quota_set["ram"]["limit"]
        addresses = list(instance["addresses"])
        address_list = []
        for item in addresses:
            items = list(item["addresses"])
            for addr in items:
                address_list.append(addr["addr"])
        addresses_joined = ';'.join(address_list)
        flavor = instance["flavor"]
        power_state = "Running" if instance["power_state"] == 1 else "Shutdown"
        created_at = dateutil.parser.parse(instance["created_at"]).replace(tzinfo=None)
        time_now = datetime.now().replace(tzinfo=None)
        duration = time_now - created_at

        attributes = {
                         "ENVIRONMENT": instance["environment"],
                         "PROJECT_NAME": project["name"],
                         "CPU_QUOTA": cores_limit,
                         "MEM_QUOTA": ram_limit,
                         "HOST": instance["host"],
                         "NAME": instance["name"],
                         "NETWORK": addresses_joined,
                         "FLAVOR_NAME": flavor["name"],
                         "CPU": flavor["vcpus"],
                         "MEMORY": flavor["ram"],
                         "DISK": flavor["disk"],
                         "STATUS": instance["vm_state"],
                         "POWER_STATE": power_state,
                         "DAYS_SINCE_CREATED": duration.days,
                         "INSTANCE_UUID": instance["uuid"]
        }
        attributes_list.append(attributes)
    cs = CalipsoCsvTool()
    print("\nCreating the requested CSV file: {}_{}".format(args.environment, cs.filename))
    written = cs.write_dicts_to_csv(attributes_list, args.environment)
    if written:
        print("\n...Done\n")
    else:
        fatal("\nI/O error (no file?)")
    exit(0)


if __name__ == "__main__":
    run()

