import numpy as np
from dataclasses import dataclass


@dataclass
class Allocations:

    name: str
    shape: [int, tuple]
    allow_invalid: bool
    is_occupied: np.ndarray
    places: np.ndarray

    def __init__(
            self,
            shape: [int, tuple],
            allow_invalid: bool = False,
            name: str = None
    ) -> None:
        self.name = name if name is not None else self.__class__.__name__
        self.shape = shape
        self.allow_invalid = allow_invalid
        self.reset()

    @property
    def places(self) -> np.ndarray:
        return self._places.reshape(self.shape)

    @property
    def is_occupied(self) -> np.ndarray:
        return np.nonzero(self._places)

    def reset(self) -> None:
        self._places = np.zeros(self.shape, dtype=int).reshape(-1)
        self.error_signal = False

    def allocate(self, to_allocate: [int, list, np.ndarray]) -> None:

        error_signal = False

        if not isinstance(to_allocate, np.ndarray):
            to_allocate = np.array(to_allocate)

        if not isinstance(self.shape, int):
            to_allocate = np.ravel_multi_index(to_allocate.transpose(), dims=self.shape)

        if np.any(np.isin(self.is_occupied, to_allocate)):
            error_signal = True

        if not error_signal or self.allow_invalid:
            self._places[to_allocate] = 1

        self.error_signal = bool(max(self.error_signal, error_signal))

    def step(self) -> None:
        self.error_signal = False


def main():
    test_allocations = Allocations(12)
    print(test_allocations)
    test_allocations.allocate(2)
    print(test_allocations.places)
    print(test_allocations.is_occupied)
    print(test_allocations.error_signal)
    test_allocations.allocate(2)
    print(test_allocations.error_signal)

    test_allocations.step()
    test_allocations.allocate([3, 4, 5])
    print(test_allocations.places)
    print(test_allocations.is_occupied)
    print(test_allocations.error_signal)
    test_allocations.allocate([3, 4, 5])
    print(test_allocations.places)
    print(test_allocations.is_occupied)
    print(test_allocations.error_signal)

    print()
    test_allocations = Allocations((5, 5), allow_invalid=True)
    print(test_allocations)
    test_allocations.allocate([[3, 2], [4, 1], [0, 3]])
    print(test_allocations.places)
    print(test_allocations.is_occupied)
    print(test_allocations.error_signal)

    test_allocations.allocate([[1, 2], [4, 1], [0, 0]])
    print(test_allocations.places)
    print(test_allocations.is_occupied)
    print(test_allocations.error_signal)


if __name__ == '__main__':
    main()
