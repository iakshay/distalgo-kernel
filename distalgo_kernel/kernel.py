import io
import ast
import traceback
from ipykernel.kernelbase import Kernel
from contextlib import redirect_stdout, redirect_stderr
from da.compiler.ui import dastr_to_pycode, parse_compiler_args
from da.compiler.ui import dastr_to_pyast

ctx = {}

#
# https://stackoverflow.com/a/39381428/1173425
#
def exec_then_eval(code, globals, locals):
    print(obj)
    block = ast.parse(code, mode='exec')

    # assumes last node is an expression
    last = ast.Expression(block.body.pop().value)

    _globals, _locals = {}, {}
    exec(compile(block, '<string>', mode='exec'), ctx, ctx)

    exp = eval(compile(last, '<string>', mode='eval'), ctx, ctx)

    print(exp)

def da_execute(code):
    ns = parse_compiler_args([])

    stdout = io.StringIO()
    stderr = io.StringIO()

    with redirect_stdout(stdout), redirect_stderr(stderr):
        obj = dastr_to_pycode(code, '<str>', ns)

    stdout = io.StringIO()
    stderr = io.StringIO()

    with redirect_stdout(stdout), redirect_stderr(stderr):
        try:
            exec_then_eval(obj, ctx, ctx)
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
        'file_extension': '.txt',
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
