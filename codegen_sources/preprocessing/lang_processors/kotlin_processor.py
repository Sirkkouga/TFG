import re
from pathlib import Path
import typing as tp
import random
import string

from .tree_sitter_processor import TreeSitterLangProcessor, TREE_SITTER_ROOT

KOTLIN_TOKEN2CHAR: tp.Dict[str, str] = {
    "STOKEN00": "//",
    "STOKEN01": "/*",
    "STOKEN02": "*/",
    "STOKEN03": "/**",
    "STOKEN04": "**/",
    "STOKEN05": '"""',
    "STOKEN06": "\\n",
    "STOKEN07": "\\r",
    "STOKEN08": ";",
    "STOKEN09": "{",
    "STOKEN10": "}",
    "STOKEN11": r"\'",
    "STOKEN12": r"\"",
    "STOKEN13": r"\\",
}
KOTLIN_CHAR2TOKEN: tp.Dict[str, str] = {
    value: " " + key + " " for key, value in KOTLIN_TOKEN2CHAR.items()
}

class KotlinProcessor(TreeSitterLangProcessor):
    def __init__(self, root_folder: Path = TREE_SITTER_ROOT) -> None:
        super().__init__(
            ast_nodes_type_string=[
                "comment",
                "block_comment",
                "line_comment",
                "string_literal",
                "character_literal",
            ],
            stokens_to_chars=KOTLIN_TOKEN2CHAR,
            chars_to_stokens=KOTLIN_CHAR2TOKEN,
            root_folder=root_folder,
        )

    def tokenize_code(self, code: str, keep_comments: bool = False, process_strings: bool = True) -> tp.List[str]:
        tokens = super().tokenize_code(code, keep_comments, process_strings)
        return tokens

    def detokenize_code(self, code: tp.Union[tp.List[str], str]) -> str:
        if isinstance(code, list):
            code = " ".join(code)
        for token, char in KOTLIN_TOKEN2CHAR.items():
            code = code.replace(token, char)
        return code

    def obfuscate_code(self, code):
        tokens = self.tokenize_code(code)
        var_names = set(re.findall(r'\bvar\s+(\w+)', code))
        obfuscated_names = {name: self._generate_random_name() for name in var_names}

        obfuscated_code = code
        for original, obfuscated in obfuscated_names.items():
            obfuscated_code = re.sub(r'\b' + original + r'\b', obfuscated, obfuscated_code)

        return obfuscated_code, obfuscated_names

    def obfuscate_types(self, code: str) -> tp.Tuple[str, str]:
        type_names = set(re.findall(r'\b[A-Z]\w*\b', code))
        obfuscated_types = {name: self._generate_random_name(prefix="T") for name in type_names}

        obfuscated_code = code
        for original, obfuscated in obfuscated_types.items():
            obfuscated_code = re.sub(r'\b' + original + r'\b', obfuscated, obfuscated_code)

        return obfuscated_code, obfuscated_types

    def extract_functions(self, code: tp.Union[str, tp.List[str]], tokenized: bool = True) -> tp.Tuple[tp.List[str], tp.List[str]]:
        if isinstance(code, list):
            code = " ".join(code)
        functions = re.findall(r'fun\s+\w+\s*\(.*?\)\s*{', code)
        return functions, code

    def get_function_name(self, function: str) -> str:
        match = re.match(r'fun\s+(\w+)', function)
        if match:
            return match.group(1)
        return ""

    def extract_arguments(self, function):
        match = re.search(r'\((.*?)\)', function)
        if match:
            args = match.group(1)
            return [arg.strip() for arg in args.split(",")]
        return []

    @staticmethod
    def format(code: str) -> str:
        formatted_code = code.strip()
        return formatted_code

    def _generate_random_name(self, length: int = 8, prefix: str = "VAR") -> str:
        return prefix + ''.join(random.choices(string.ascii_letters + string.digits, k=length))
