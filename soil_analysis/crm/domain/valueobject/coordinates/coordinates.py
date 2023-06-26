from abc import ABC, abstractmethod
from typing import Tuple


class Coordinates(ABC):
    @abstractmethod
    def get_coordinates(self) -> Tuple[float, float]:
        pass
