class ScanEnvironment:

    run_scan_count = 0
    scan_links_count = 0
    scan_cliques_count = 0
    result = []

    def set_result(self, result):
        self.result = result

    def run_scan(self, *args):
        ScanEnvironment.run_scan_count += 1
        return self.result

    def scan_links(self, *args):
        ScanEnvironment.scan_links_count += 1

    def scan_cliques(self, *args):
        ScanEnvironment.scan_cliques_count += 1

    def set_env(self, env):
        pass

    @classmethod
    def reset_counts(cls):
        cls.run_scan_count = 0
        cls.scan_cliques_count = 0
        cls.scan_links_count = 0