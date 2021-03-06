"""This class provides the necessary classes for agents (general), predators and prey."""

import numpy as np
import random as rd
from collections import namedtuple, deque
from typing import Callable, NamedTuple, Union

memory = namedtuple('Memory', ('States', 'Rewards', 'Actions'))


class Agent:
    """
    This class provides an agent object.

    It has the following attributes:
        - food_reserve
        - max_food_reserve
        - generation, a counter, representing the number of parents
        - p_breed, the breeding probability
        - kin, a string providing the type of agent
        - memory, a named tuple of deques saving the agents' states, rewards
            and actions
        - kwargs, a dictionary storing every additional property that might
            find its way into the class call.

    class constants:
        - HEIRSHIP, a list of properties to pass down to the next generation

    Accessing the attributes is done via properties and setter, if necessary.

    The only necessary argument to specify is the food reserve. The rest is optional.
    """

    # class constants
    HEIRSHIP = ['max_food_reserve', 'generation', 'p_breed', '_kwargs']

    # slots -------------------------------------------------------------------
    __slots__ = ['_food_reserve', '_max_food_reserve', '_generation',
                 '_p_breed', '_kin', '_kwargs', '_memory']

    # Init --------------------------------------------------------------------
    def __init__(self, *, food_reserve: Union[int, float], max_food_reserve: int=None,
                 generation: int=None, p_breed: float=1.0, kin: str=None,
                 mem: tuple=None, **kwargs):
        """Initialise the agent instance."""
        # Initialize values
        self._food_reserve = 0
        self._max_food_reserve = None
        self._generation = None
        self._p_breed = 1.0
        self._kin = None
        self._kwargs = kwargs  # just set the value directly here.
        self._memory = None

        # Set property managed attributes
        self.food_reserve = food_reserve
        self.p_breed = p_breed

        if kin:  # if kin is given, set kin
            self.kin = kin

        else:  # otherwise just set 'Agent' as kin
            self.kin = self.__class__.__name__

        if max_food_reserve:
            self.max_food_reserve = max_food_reserve

        if generation is not None:
            self.generation = generation

        if mem is not None:
            self.memory = mem
        else:
            self.memory = memory(deque(), deque(), deque())  # initialize empty lists

    # magic method ------------------------------------------------------------
    def __str__(self) -> str:
        """Return the agents properties."""
        props = ("{}\tID: {}\tgeneration: {}\tfood_reserve: {}\t"
                 "max_food_reserve: {}".format(self.kin,  # self.uuid,
                                               self.generation,
                                               self.food_reserve,
                                               self.max_food_reserve))

        return props

    # Properties --------------------------------------------------------------
    # food_reserve
    @property
    def food_reserve(self) -> int:
        """The food reserve of the agent."""
        return self._food_reserve

    @food_reserve.setter
    def food_reserve(self, food_reserve: Union[int, float]) -> None:
        """The food reserve setter."""
        if not isinstance(food_reserve, (int, float)):
            raise TypeError("food_reserve can only be of type integer, but"
                            " type {} was given".format(type(food_reserve)))

        elif food_reserve < 0:
            raise ValueError("food_reserve must be positive, but {} was given."
                             "".format(food_reserve))

        elif self.max_food_reserve:
            if food_reserve >= self.max_food_reserve:
                self._food_reserve = self.max_food_reserve

            else:
                self._food_reserve = food_reserve

        else:
            self._food_reserve = food_reserve

    # max_food_reserve
    @property
    def max_food_reserve(self) -> Union[int, float]:
        """The maximal food reserve of the agent."""
        return self._max_food_reserve

    @max_food_reserve.setter
    def max_food_reserve(self, max_food_reserve: Union[int, float]) -> None:
        """The maximal food reserve setter."""
        if not isinstance(max_food_reserve, (int, float)):
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

    # breeding probability
    @property
    def p_breed(self) -> float:
        """The breeding probability of the Agent."""
        return self._p_breed

    @p_breed.setter
    def p_breed(self, p_breed: float) -> None:
        """The breeding probability setter."""
        if not isinstance(p_breed, float):
            raise TypeError("p_breed must be of type float, but {} was given."
                            "".format(type(p_breed)))
        elif p_breed < 0 or p_breed > 1:
            raise ValueError("p_breed must be between 0 and 1 but {} was given."
                             "".format(p_breed))

        else:
            self._p_breed = p_breed

    # kin
    @property
    def kin(self) -> str:
        """Return kin of the agent."""
        return self._kin

    @kin.setter
    def kin(self, kin: str) -> None:
        """The kin setter for the agent."""
        if not isinstance(kin, str):
            raise TypeError("kin must be of type str, but {} was given."
                            "".format(type(kin)))
        # elif self.kin:
        #     raise RuntimeError("kin is alreday set and cannot be changed on the"
        #                       " fly.")

        else:
            self._kin = kin

    # memory for learning
    @property
    def memory(self) -> NamedTuple:
        """Hold the history of all states, rewards and actions for a single agent."""
        return self._memory

    @memory.setter
    def memory(self, memory: NamedTuple) -> None:
        """Set the NamedTuple for the memory."""
        if not isinstance(memory, tuple):
            raise TypeError("memory must be of type tuple, but {} was given."
                            "".format(type(memory)))
        elif self._memory is not None:
            raise RuntimeError("memory already set. This should not have "
                               "happened.")
        else:
            self._memory = memory

    # staticmethods -----------------------------------------------------------
    # no staticmethods so far...

    # classmethods ------------------------------------------------------------
    @classmethod
    def _procreate_empty(cls, *, food_reserve: int) -> Callable:
        """The classmethod creates a new "empty" instance of `cls`.

        food_reserve needs to be set explicitely.
        """
        return cls(food_reserve=food_reserve)

    # methods -----------------------------------------------------------------
    def procreate(self, *, food_reserve: int) -> Callable:
        """Take a class instance and inherit all attributes in `HEIRSHIP` from self.

        Return a `cls` instance with attributes set.
        """
        # create empty instance
        offspring = self._procreate_empty(food_reserve=food_reserve)

        # iterate over all attributes
        for attr in self.HEIRSHIP:
            parent_attr = getattr(self, attr)
            if parent_attr is not None:
                # adapt generation counter if set in parent
                if attr == 'generation':
                    setattr(offspring, attr, parent_attr+1)
                else:
                    setattr(offspring, attr, parent_attr)

        return offspring


class Predator(Agent):
    """Predator class derived from Agent.

    This provides (additionally to class Agent):
        - p_eat, the probability to eat a prey agent (should be defined as
            1-p_flee), is here for simplicity. (TODO: fix that)
    """

    # class constants
    HEIRSHIP = Agent.HEIRSHIP + ['p_eat']

    # slots -------------------------------------------------------------------
    __slots__ = ['_p_eat']

    # init --------------------------------------------------------------------
    def __init__(self, *, food_reserve: Union[int, float], p_eat: float=1.0,
                 max_food_reserve: Union[int, float]=None, p_breed: float=1.0,
                 generation: int=None, **kwargs):
        """Initialise a Predator instance."""
        super().__init__(food_reserve=food_reserve,
                         max_food_reserve=max_food_reserve,
                         generation=generation,
                         p_breed=p_breed,
                         kin=self.__class__.__name__,
                         **kwargs)

        # initialise new attributes
        self._p_eat = 1.0

        # set new (property managed) attributes
        self.p_eat = p_eat

    # magic method ------------------------------------------------------------
    def __str__(self) -> str:
        """Return the agents properties."""
        props = ("Kin: {}\tgen: {}\tfood_res: {}\t"
                 "max_food_res: {}\t p_eat: {}".format(self.kin,  # self.uuid,
                                                       self.generation,
                                                       self.food_reserve,
                                                       self.max_food_reserve,
                                                       self.p_eat))

        return props

    # properties --------------------------------------------------------------
    @property
    def p_eat(self) -> float:
        """The eating probability of the predator."""
        return self._p_eat

    @p_eat.setter
    def p_eat(self, p_eat: float) -> None:
        """The eating probability setter."""
        if not isinstance(p_eat, float):
            raise TypeError("p_eat must be of type float, but {} was given."
                            "".format(type(p_eat)))
        elif p_eat < 0 or p_eat > 1:
            raise ValueError("p_eat must be between 0 and 1 but {} was given."
                             "".format(p_eat))

        else:
            self._p_eat = p_eat


class Prey(Agent):
    """Prey class derived from Agent.

    This provides (additionally to class Agent):
        - p_flee, the fleeing probability
        - got_eaten, boolean flag to specify whether a prey got eaten or not.
    """

    # class constants
    # _UUID_LENGTH = Agent._UUID_LENGTH
    HEIRSHIP = Agent.HEIRSHIP + ['p_flee']

    # slots -------------------------------------------------------------------
    __slots__ = ['_p_flee', '_got_eaten']

    # init --------------------------------------------------------------------
    def __init__(self, *, food_reserve: Union[int, float], p_breed: float=1.0,
                 max_food_reserve: Union[int, float]=None, p_flee: float=0.0,
                 generation: int=None, **kwargs):
        """Initialise a Prey instance."""
        super().__init__(food_reserve=food_reserve,
                         max_food_reserve=max_food_reserve,
                         generation=generation,
                         p_breed=p_breed,
                         kin=self.__class__.__name__,
                         **kwargs)

        # initialise new attributes
        self._p_flee = 0.0
        self._got_eaten = False

        if p_flee is not None:
            # set new (property managed) attributes
            self.p_flee = p_flee

    # magic method ------------------------------------------------------------
    def __str__(self) -> str:
        """Return the agents properties."""
        props = ("Kin: {}\tgen: {}\tfood_res: {}\t"
                 "max_food_res: {}\t p_flee: {}\t"
                 " got_eaten: {}".format(self.kin,  # self.uuid,
                                         self.generation,
                                         self.food_reserve,
                                         self.max_food_reserve,
                                         self.p_flee,
                                         self.got_eaten))

        return props

    # properties --------------------------------------------------------------
    @property
    def p_flee(self) -> float:
        """The fleeing probability of the prey."""
        return self._p_flee

    @p_flee.setter
    def p_flee(self, p_flee: float) -> None:
        """The fleeing probability setter."""
        if not isinstance(p_flee, float):
            raise TypeError("p_flee must be of type float, but {} was given."
                            "".format(type(p_flee)))
        elif p_flee < 0 or p_flee > 1:
            raise ValueError("p_flee must be between 0 and 1 but {} was given."
                             "".format(p_flee))

        else:
            self._p_flee = p_flee

    @property
    def got_eaten(self) -> bool:
        """Flag if prey was eaten (needed for actor-critic)."""
        return self._got_eaten

    @got_eaten.setter
    def got_eaten(self, got_eaten: bool) -> None:
        """Set if prey got eaten."""
        if not isinstance(got_eaten, bool):
            raise TypeError("got_eaten must be of type bool, but {} was given."
                            "".format(type(got_eaten)))

        else:
            self._got_eaten = got_eaten


# -----------------------------------------------------------------------------
class OrientedPredator(Predator):
    """Predator class derived from Predator class.

    This class holds an additional feature of having a directed action. In
    other words, an Agent of this class can only act in the direction it is
    looking.

    Additional properties:
        - orient, a 2-tuple of the (X,Y) coordinates of the agents orientation
            note, that when using plt.quiver one has to provide x,y coordinates
            whereas np.where returns y,x values.
    """

    # class constants
    HEIRSHIP = Predator.HEIRSHIP

    # slots -------------------------------------------------------------------
    __slots__ = ['_orient']

    # init --------------------------------------------------------------------
    def __init__(self, *, food_reserve: Union[int, float], p_breed: float=1.0,
                 max_food_reserve: Union[int, float]=None, p_eat: float=1.0,
                 generation: int=None, orient: tuple=None, **kwargs):
        """Initialze a OrientedPredator instance."""
        super().__init__(food_reserve=food_reserve,
                         max_food_reserve=max_food_reserve,
                         generation=generation,
                         p_breed=p_breed,
                         p_eat=p_eat,
                         # kin=self.__class__.__name__,
                         **kwargs)

        # initialize new attributes
        self._orient = (0, 0)

        # set new (property managed) attributes
        self.orient = orient

    # magic method ------------------------------------------------------------
    def __str__(self) -> str:
        """Return the agents properties."""
        props = ("Kin: {}\tgen: {}\tfood_res: {}\t"
                 "max_food_res: {}\t p_eat: {}\t orient: {}"
                 "".format(self.kin, self.generation, self.food_reserve,
                           self.max_food_reserve, self.p_eat, self.orient))

        return props

    # properties --------------------------------------------------------------
    @property
    def orient(self) -> tuple:
        """The agents' orientation as (Y,X) tuple."""
        return self._orient

    @orient.setter
    def orient(self, orient: tuple) -> None:
        """Set the agents orientation."""
        if orient is None:
            self._generate_orient()

        elif not isinstance(orient, tuple) or len(orient) > 2:
            raise TypeError("Orientation must be of 2-tuple but {} of length"
                            "{} was given.".format(type(orient), len(orient)))

        else:
            self._orient = orient

    # methods -----------------------------------------------------------------
    def _generate_orient(self) -> None:
        """Generate a random orientation for an agent."""
        y = rd.choice([-1, 0, 1])  # first variable
        x = rd.choice([-1, 1]) if y == 0 else 0  # set x depending on y
        orient = [y, x]
        np.random.shuffle(orient)  # shuffle the resulting 2-vector to remove any bias
        self.orient = tuple(orient)


class OrientedPrey(Prey):
    """Prey class derived from Prey class.

    This class holds an additional feature of having a directed action. In
    other words, an Agent of this class can only act in the direction it is
    looking.

    Additional properties:
        - orient, a 2-tuple of the (X,Y) coordinates of the agents orientation
            note, that when using plt.quiver one has to provide x,y coordinates
            whereas np.where returns y,x values.
    """

    # class constants
    HEIRSHIP = Prey.HEIRSHIP

    # slots -------------------------------------------------------------------
    __slots__ = ['_orient']

    # init --------------------------------------------------------------------
    def __init__(self, *, food_reserve: Union[int, float], p_breed: float=1.0,
                 max_food_reserve: Union[int, float]=None, p_flee: float=0.0,
                 generation: int=None, orient: tuple=None, **kwargs):
        """Initialze a OrientedPredator instance."""
        super().__init__(food_reserve=food_reserve,
                         max_food_reserve=max_food_reserve,
                         generation=generation,
                         p_breed=p_breed,
                         p_flee=p_flee,
                         # kin=self.__class__.__name__,
                         **kwargs)

        # initialize new attributes
        self._orient = (0, 0)

        # set new (property managed) attributes
        self.orient = orient

    # magic method ------------------------------------------------------------
    def __str__(self) -> str:
        """Return the agents properties."""
        props = ("Kin: {}\tgen: {}\tfood_res: {}\t"
                 "max_food_res: {}\t p_flee: {}\t orient: {}"
                 "".format(self.kin, self.generation, self.food_reserve,
                           self.max_food_reserve, self.p_flee, self.orient))

        return props

    # properties --------------------------------------------------------------
    @property
    def orient(self) -> tuple:
        """The agents' orientation as (Y,X) tuple."""
        return self._orient

    @orient.setter
    def orient(self, orient: tuple) -> None:
        """Set the agents orientation."""
        if orient is None:
            self._generate_orient()

        elif not isinstance(orient, tuple) or len(orient) > 2:
            raise TypeError("Orientation must be of 2-tuple but {} of length"
                            "{} was given.".format(type(orient), len(orient)))

        else:
            self._orient = orient

    # methods -----------------------------------------------------------------
    def _generate_orient(self) -> None:
        """Generate a random orientation for an agent."""
        y = rd.choice([-1, 0, 1])  # first variable
        x = rd.choice([-1, 1]) if y == 0 else 0  # set x depending on y
        orient = [y, x]
        np.random.shuffle(orient)  # shuffle the resulting 2-vector to remove any bias
        self.orient = tuple(orient)
