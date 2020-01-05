import abc

from base.utils.inventory_mgr import InventoryMgr


class ValidatorBase(metaclass=abc.ABCMeta):
    def __init__(self, env):
        self.env = env
        self.inv = InventoryMgr()

    @abc.abstractmethod
    def run(self) -> (bool, list):
        return True, []
