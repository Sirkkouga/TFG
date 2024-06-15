import re

from .lang_processor import LangProcessor, NEWLINE_TOK

BYTECODE_LANGUAGE_NAME = "bytecode"

class BytecodeProcessor(LangProcessor):
 def tokenize_code(
        self, code: str, keep_comments: bool = False, process_strings: bool = True
    ):
        code = code.replace("\n", f" NEW_LINE ").replace("\r", "")
        return re.sub(r"\s+", " ", code).split(" ")

def detokenize_code(self, code):
    return code.replace(f" NEW_LINE ", "\n").replace(NEWLINE_TOK, "\n")