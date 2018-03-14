"""This class provides the necessary classes for agents (general), predators and prey."""

import numpy as np

from tools import generate_uuid


class Agent:
    """
    This class provides an agent object.

    It has the following attributes:
        - food_reserve
        - max_food_reserve
        - generation
        - ID
        - .... more to come

    Accessing the attributes is done via properties and setter, if necessary.
    """

    # slots -------------------------------------------------------------------
    __slots__ = ['_food_reserve', '_max_food_reserve', '_generation', '_uuid'
                 '_UUID_LENGTH']

    # class constants
    _UUID_LENGTH = 34  # len(uuid) + 2

    # Init --------------------------------------------------------------------
    def __init__(self, *, food_reserve: int, max_food_reserve: int=None,
                 generation: int=None, **kwargs):
        """Initialise the agent instance."""
        # Initialize values
        self._food_reserve = 0
        self._max_food_reserve = None
        self._generation = None
        self._uuid = None

        # Set property managed attributes
        self.food_reserve = food_reserve
        self.max_food_reserve = max_food_reserve

    # Properties --------------------------------------------------------------
    # food_reserve
    @property
    def food_reserve(self) -> int:
        """The food reserve of the agent."""
        return self._food_reserve

    @food_reserve.setter
    def food_reserve(self, food_reserve: int) -> None:
        """The food reserve setter."""
        if not isinstance(food_reserve, int):
            raise TypeError("food_reserve can only be of type integer, but"
                            " type {} was given".format(type(food_reserve)))

        elif food_reserve < 0:
            raise ValueError("food_reserve must be positive, but {} was given."
                             "".format(food_reserve))

        else:
            self._food_reserve = food_reserve

    # max_food_reserve
    @property
    def max_food_reserve(self) -> int:
        """The maximal food reserve of the agent."""
        return self._max_food_reserve

    @max_food_reserve.setter
    def max_food_reserve(self, max_food_reserve: int) -> None:
        """The maximal food reserve setter."""
        if not isinstance(max_food_reserve, int):
            raise TypeError("max_food_reserve can only be of type integer, "
                            "but type {} was given"
                            "".format(type(max_food_reserve)))

        elif max_food_reserve < self.food_reserve:
            raise ValueError("max_food_reserve must be greater or equal than"
                             " food_reserve={}, but {} was given."
                             "".format(self.food_reserve, max_food_reserve))

        elif self.max_food_reserve:
            raise RuntimeError("max_food_reserve is already set.")

        else:
            self._max_food_reserve = max_food_reserve

    # generation
    @property
    def generation(self) -> int:
        """The generation of the agent."""
        return self._generation

    @generation.setter
    def generation(self, generation: int) -> None:
        """The generation setter."""
        if not isinstance(generation, int):
            raise TypeError("generation can only be of type integer, "
                            "but {} was given.".format(type(generation)))

        elif generation < 0:
            raise ValueError("generation must be positive but {} was given"
                             "".format(generation))

        elif self.generation:
            raise RuntimeError("generation is already set.")

        else:
            self._generation = generation

    # id
    @property
    def uuid(self) -> str:
        """The uuid of the agent."""
        return self._uuid

    @uuid.setter
    def uuid(self, uuid: str) -> None:
        """The uuid setter."""
        if not isinstance(uuid, str):
            raise TypeError("uuid can only be of type str, but {} was given."
                            "".format(type(uuid)))

        elif len(uuid) < self._UUID_LENGTH:
            raise ValueError("uuid must be of length {} but given uuid {} has "
                             "length {}".format(self._UUID_LENGTH, uuid,
                                                len(uuid)))
        elif self.uuid:
            raise RuntimeError("uuid is already set.")

        else:
            self._uuid = uuid