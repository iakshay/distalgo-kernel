import io
import ast
import traceback
from ipykernel.kernelbase import Kernel
from contextlib import redirect_stdout, redirect_stderr
from da.compiler.ui import dastr_to_pycode, parse_compiler_args
from da.compiler.ui import dastr_to_pyast
import _ast
ctx = {}

#
# https://stackoverflow.com/a/39381428/1173425
#
def exec_then_eval(code, globals, locals):
    ns = parse_compiler_args([])
    block = dastr_to_pyast(code, 'str', ns)

    # assumes last node is an expression
    if isinstance(block.body[-1], _ast.Expr):
        last = ast.Expression(block.body.pop().value)
        exec(compile(block, '<string>', mode='exec'), ctx, ctx)
        exp = eval(compile(last, '<string>', mode='eval'), ctx, ctx)

        print(exp)

    else:
        exec(compile(block, '<string>', mode='exec'), ctx, ctx)

def da_execute(code):
    stdout = io.StringIO()
    stderr = io.StringIO()

    with redirect_stdout(stdout), redirect_stderr(stderr):
        try:
            exec_then_eval(code, ctx, ctx)
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)
    return stdout.getvalue()

class DistAlgoKernel(Kernel):
    implementation = 'DistAlgo'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.da',
    }
    banner = "DistAlgo kernel - as useful as a parrot"

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            stream_content = {'name': 'stdout', 'text': da_execute(code)}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
