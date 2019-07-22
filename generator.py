# Generators generate a stream of random tetrominoes.
# A generator consists of:
#     - random source (source of randomness)
#     - packer
#     - unpacker
# 
# The random source generates random integers between 1 and 7.
# These integers represent the Tetromino types I, J, L, O, S, T, and Z.
# The random source outputs the integers to the packer
# 
# The packer packs these integers into bags of n tetrominoes obeying certain
# bagging rules, e.g. packing into bags of 7 unique integers. The packer 
# yields these bags to the unpacker.
# 
# The unpacker unpacks these bags and offers the preview of x next
# tetrominoes, e.g. 3 next tetrominoes.
# The unpacker yields the first next tetromino to the program.


import generators.python9001.python9001 as gen
import generators.ones.ones as ones
from collections import deque
from typing import Callable
import random
import logging
import logging.config
import logging_conf

# Setup logging
logging.config.dictConfig(logging_conf.dict_config)
logger = logging.getLogger(__name__)


class Random_Source():
    """
    This is a wrapper for a python-like random integer function.
    """
    def __init__(self, seed=None, set_seed=None, function=None, args=(), kwargs={}):
        self.seed = seed
        self.set_seed = set_seed
        # set the seed
        if self.set_seed is not None:
            self.set_seed(self.seed)
        self.function = function
        self.args = args
        self.kwargs = kwargs
    def __next__(self):
        random_number = self.function(*self.args, **self.kwargs)
        logger.debug(f"Random_Source returning {random_number}")
        return random_number


def one_I_in_7(rs: Random_Source):
    maxlen = 7
    bag = deque([], maxlen)
    logger.debug("filling the bag")
    while len(bag) < maxlen:
        to_append = next(rs)
        if to_append not in bag:
            logger.debug(f"{to_append} is not in the bag")
            bag.append(to_append)
            logger.debug(f"added {to_append} to the bag")
        else:
            logger.debug(f"discarding {to_append}, it is already in the bag")
    logger.debug("bag filled")
    yield bag


def no_rules(rs: Random_Source):
    number = next(rs)
    logger.debug(f"got {number}, yielding {number}")
    yield deque([number], 1)


def seven_ones(rs: Random_Source):
    maxlen = 7
    result = deque([], maxlen)
    while len(result) < result.maxlen:
        to_check = next(rs)
        if to_check == 1:
            logger.debug(f"appending {to_check}")
            result.append(to_check)
        else:
            logger.debug(f"discarding {to_check}")
    logger.debug(f"returning full bag: {result}")
    yield result


packer_dict = {"one_I_in_7": one_I_in_7,
               "no_rules": no_rules,
               "seven_ones": seven_ones,
               }


class Unpacker():
    def __init__(self, packer: Callable[[Random_Source], deque], rs: Random_Source):
        self.packer = packer
        self.rs = rs
        self.got_bag = deque([], 0)
        logger.debug(f"initialized unpacker with {self.got_bag}")
    def next(self):
        try:
            logger.debug(f"trying popleft() from {self.got_bag}")
            result = self.got_bag.popleft()
        except IndexError:
            logger.debug("requesting new bag")
            self.got_bag = next(self.packer(self.rs))
            logger.debug(f"got new bag: {self.got_bag}, popping left...")
            result = self.got_bag.popleft()
        return result
    def show_next(self, n: int):
        try:
            return tuple(next(self) for _ in range(n))
        except IndexError as err:
            logger.exception("Got an IndexError in Unpacker. This should not happen")


gen_dict = {"python9001": Random_Source(function=gen.generate),
            "randint17": Random_Source(seed=9001, set_seed=random.seed, function=random.randint, args=(1, 7)),
            "ones": Random_Source(function=ones.generate),
            }


if __name__ == "__main__":
    u = Unpacker(packer_dict["one_I_in_7"], gen_dict["python9001"])
    for _ in range(8):
        print(u.next())
    logger.debug(f"======= CHANGING PACKER WHILE BAG IS NOT EMPTY ========")
    u.packer = packer_dict["seven_ones"]
    for _ in range(10):
        print(u.next())
    logger.debug("========= CHANGING RANDOM SOURCE WHILE BAG IS NOT EMPTY ======")
    u.rs = gen_dict["ones"]
    for _ in range(7):
        print(u.next())
    logger.debug(f"======= CHANGING PACKER WHILE BAG IS NOT EMPTY ========")
    u.packer = packer_dict["no_rules"]
    for _ in range(10):
        print(u.next())