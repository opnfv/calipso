from base.fetcher import Fetcher
from base.utils.inventory_mgr import InventoryMgr


class Processor(Fetcher):

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def run(self):
        self.log.info("Running processor: {}".format(self.__class__.__name__))

    def find_by_type(self, object_type):
        return self.inv.find_items({"environment": self.env, "type": object_type})
