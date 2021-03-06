import chunk
import function
import vm
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    import scanner
    import value


def test_manual_init():
    # type: () -> None
    bytecode = chunk.init_chunk()

    bytecode, constant = chunk.add_constant(bytecode, 1.2)
    bytecode = chunk.write_chunk(bytecode, chunk.OpCode.OP_CONSTANT, 123)
    bytecode = chunk.write_chunk(bytecode, constant, 123)

    bytecode, constant = chunk.add_constant(bytecode, 3.4)
    bytecode = chunk.write_chunk(bytecode, chunk.OpCode.OP_CONSTANT, 123)
    bytecode = chunk.write_chunk(bytecode, constant, 123)

    bytecode = chunk.write_chunk(bytecode, chunk.OpCode.OP_ADD, 123)

    bytecode, constant = chunk.add_constant(bytecode, 4.6)
    bytecode = chunk.write_chunk(bytecode, chunk.OpCode.OP_CONSTANT, 123)
    bytecode = chunk.write_chunk(bytecode, constant, 123)

    bytecode = chunk.write_chunk(bytecode, chunk.OpCode.OP_DIVIDE, 123)
    bytecode = chunk.write_chunk(bytecode, chunk.OpCode.OP_NEGATE, 123)

    bytecode = chunk.write_chunk(bytecode, chunk.OpCode.OP_PRINT, 123)
    bytecode = chunk.write_chunk(bytecode, chunk.OpCode.OP_NIL, 123)
    bytecode = chunk.write_chunk(bytecode, chunk.OpCode.OP_RETURN, 123)

    fun = function.init_function(function.FunctionType.TYPE_SCRIPT)
    fun.bytecode = bytecode

    emulator = vm.init_vm()
    assert emulator.frames is not None
    frame = emulator.frames[emulator.frame_count]
    emulator.frame_count += 1

    frame.fun = fun
    frame.ip = 0
    frame.slots_top = 1
    assert emulator.stack is not None
    frame.slots = list(emulator.stack)
    frame.slots[0] = fun

    result = vm.run(emulator)
    assert result[0] == vm.InterpretResult.INTERPRET_OK
    assert result[1] == chunk.OpCode.OP_RETURN
    assert result[2] == [-1.0]

    vm.free_vm(emulator)


def interpret(source, result, opcode, output):
    # type: (scanner.Source, vm.InterpretResult, chunk.OpCode, List[value.Value]) -> None
    emulator = vm.init_vm()
    result_tuple = vm.interpret(emulator, source, 0)

    assert result_tuple[0] == result
    assert result_tuple[1] == opcode
    assert result_tuple[2] == output

    vm.free_vm(emulator)


def test_basic_add():
    # type: () -> None
    interpret(
        source="print 1 + 1;",
        result=vm.InterpretResult.INTERPRET_OK,
        opcode=chunk.OpCode.OP_RETURN,
        output=[2],
    )


def test_basic_subtract():
    # type: () -> None
    interpret(
        source="print 2 - 1;",
        result=vm.InterpretResult.INTERPRET_OK,
        opcode=chunk.OpCode.OP_RETURN,
        output=[1],
    )


def test_basic_multiply():
    # type: () -> None
    interpret(
        source="print 3 * 3;",
        result=vm.InterpretResult.INTERPRET_OK,
        opcode=chunk.OpCode.OP_RETURN,
        output=[9],
    )


def test_basic_divide():
    # type: () -> None
    interpret(
        source="print 9 / 3;",
        result=vm.InterpretResult.INTERPRET_OK,
        opcode=chunk.OpCode.OP_RETURN,
        output=[3],
    )


def test_basic_negate():
    # type: () -> None
    interpret(
        source="print -1;",
        result=vm.InterpretResult.INTERPRET_OK,
        opcode=chunk.OpCode.OP_RETURN,
        output=[-1],
    )


def test_basic_scope():
    # type: () -> None
    interpret(
        source="""\
        {
            print 1;
        }
        """,
        result=vm.InterpretResult.INTERPRET_OK,
        opcode=chunk.OpCode.OP_RETURN,
        output=[1],
    )


def test_single_variable_single_scope():
    # type: () -> None
    interpret(
        source="""\
        {
            let a = 1;
            print a;
        }
        """,
        result=vm.InterpretResult.INTERPRET_OK,
        opcode=chunk.OpCode.OP_RETURN,
        output=[1],
    )


def test_single_variable_multiple_scope():
    # type: () -> None
    interpret(
        source="""\
        {
            let a = 1;
            print a;

            {
                a = 2;
                print a;
            }

            print a;
        }
        """,
        result=vm.InterpretResult.INTERPRET_OK,
        opcode=chunk.OpCode.OP_RETURN,
        output=[1, 2, 2],
    )


def test_multiple_variable_single_scope():
    # type: () -> None
    interpret(
        source="""\
        {
            let a = 1;
            print a;

            let b = 2;
            print b;
        }
        """,
        result=vm.InterpretResult.INTERPRET_OK,
        opcode=chunk.OpCode.OP_RETURN,
        output=[1, 2],
    )


def test_multiple_variable_multiple_scope():
    # type: () -> None
    interpret(
        source="""\
        {
            let a = 1;
            print a;

            {
                let b = 2;
                print b;
            }

            print a;
        }
        """,
        result=vm.InterpretResult.INTERPRET_OK,
        opcode=chunk.OpCode.OP_RETURN,
        output=[1, 2, 1],
    )


def test_multiple_variable_scope_error():
    # type: () -> None
    interpret(
        source="""\
        {
            let a = 1;
            print a;

            {
                let b = 2;
            }

            print b;
        }
        """,
        result=vm.InterpretResult.INTERPRET_RUNTIME_ERROR,
        opcode=chunk.OpCode.OP_GET_LOCAL,
        output=[1],
    )


def test_basic_function():
    # type: () -> None
    interpret(
        source="""\
        {
            fun a() {
                return 1;
            }

            print a();
        }
        """,
        result=vm.InterpretResult.INTERPRET_OK,
        opcode=chunk.OpCode.OP_RETURN,
        output=[1],
    )
