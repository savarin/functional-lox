import enum
from typing import Optional

import chunk


class FunctionType(enum.Enum):
    """
    """
    TYPE_FUNCTION = "TYPE_FUNCTION"
    TYPE_SCRIPT = "TYPE_SCRIPT"


class Function():
    def __init__(self):
        # type: () -> None
        """Stores function bytecode with name and arity."""
        self.function_type = None  # type: Optional[FunctionType]
        self.arity = 0
        self.bytecode = None  # type: Optional[chunk.Chunk]
        self.name = None


def init_function(function_type):
    # type: (FunctionType) -> Function
    """Initialize new function."""
    fun = Function()
    fun.function_type = function_type
    fun.bytecode = chunk.init_chunk()

    return fun


def free_function(fun):
    #
    """
    """
    fun.bytecode = chunk.free_chunk(fun.bytecode)
    return init_function()
