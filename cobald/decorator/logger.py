import logging

from cobald.interfaces.pool import Pool
from cobald.interfaces.proxy import PoolDecorator


class Logger(PoolDecorator):
    """
    Proxy which logs all changes to ``target.demand``
    """
    @property
    def demand(self):
        return self.target.demand

    @demand.setter
    def demand(self, value):
        self._logger.log(
            self.level, 'demand = %s [demand=%s, supply=%s, utilisation=%.2f, consumption=%.2f]',
            value, self.target.demand, self.target.supply, self.target.utilisation, self.target.allocation)
        self.target.demand = value

    @property
    def identifier(self) -> str:
        return self._logger.name

    @identifier.setter
    def identifier(self, value: str):
        if value is None:
            value = self.target.__class__.__qualname__
        self._logger = logging.getLogger(value)

    def __init__(self, target: Pool, identifier: str = None, level: int = logging.INFO):
        super().__init__(target=target)
        self._logger = None  # type: logging.Logger
        self.identifier = identifier
        self.level = level