import contextlib
import io
import re

from bloqade.qasm2.parse import pprint


def get_qasm_string(ast) -> str:
    with io.StringIO() as buf, contextlib.redirect_stdout(buf):
        pprint(ast)
        raw_qasm = buf.getvalue()

    # Remove ANSI escape sequences
    ansi_escape = re.compile(r"\x1b\[[0-9;]*m")
    clean_qasm = ansi_escape.sub("", raw_qasm)

    return clean_qasm
