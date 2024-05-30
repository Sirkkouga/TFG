import subprocess
import typing as tp
from pathlib import Path
import re
import random
import string
from .lang_processor import LangProcessor

class BytecodeProcessor(LangProcessor):
    def __init__(self):
        super().__init__()

    @classmethod
    def _language(cls) -> str:
        return 'bytecode'

    def bytecode_to_ir(self, bytecode_path: Path) -> str:
        result = subprocess.run(
            ['javap', '-c', '-p', bytecode_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            raise Exception(f"Error decompiling bytecode: {result.stderr.decode()}")
        return result.stdout.decode()

    def ir_to_bytecode(self, ir: str, output_path: Path) -> None:
        temp_ir_path = output_path.with_suffix('.java')
        with open(temp_ir_path, 'w') as file:
            file.write(ir)
        result = subprocess.run(
            ['javac', str(temp_ir_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            raise Exception(f"Error compiling intermediate representation: {result.stderr.decode()}")
        compiled_class = temp_ir_path.with_suffix('.class')
        if compiled_class.exists():
            compiled_class.rename(output_path)
        temp_ir_path.unlink()

    def decompile_bytecode(self, bytecode_path: Path) -> str:
        result = subprocess.run(
            ['javap', '-c', '-p', bytecode_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            raise Exception(f"Error decompiling bytecode: {result.stderr.decode()}")
        return result.stdout.decode()

    def compile_source_to_bytecode(self, source_code: str, output_path: Path) -> None:
        source_path = output_path.with_suffix('.java')
        with open(source_path, 'w') as file:
            file.write(source_code)
        result = subprocess.run(
            ['javac', str(source_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            raise Exception(f"Error compiling source code: {result.stderr.decode()}")
        compiled_class = source_path.with_suffix('.class')
        if compiled_class.exists():
            compiled_class.rename(output_path)
        source_path.unlink()

    def extract_methods(self, bytecode_path: Path) -> tp.List[str]:
        decompiled_code = self.decompile_bytecode(bytecode_path)
        methods = re.findall(r'\b(\w+)\s*\(.*?\)\s*\{', decompiled_code)
        return methods

    def obfuscate_code(self, bytecode_path: Path, output_path: Path) -> tp.Tuple[str, dict]:
        decompiled_code = self.decompile_bytecode(bytecode_path)
        methods = set(re.findall(r'\b(\w+)\(', decompiled_code))
        obfuscated_names = {name: self._generate_random_name() for name in methods}

        obfuscated_code = decompiled_code
        for original, obfuscated in obfuscated_names.items():
            obfuscated_code = re.sub(r'\b' + original + r'\b', obfuscated, obfuscated_code)

        self.ir_to_bytecode(obfuscated_code, output_path)
        return obfuscated_code, obfuscated_names

    def obfuscate_types(self, bytecode_path: Path, output_path: Path) -> tp.Tuple[str, dict]:
        decompiled_code = self.decompile_bytecode(bytecode_path)
        types = set(re.findall(r'\b[A-Z]\w*\b', decompiled_code))
        obfuscated_types = {name: self._generate_random_name(prefix="T") for name in types}

        obfuscated_code = decompiled_code
        for original, obfuscated in obfuscated_types.items():
            obfuscated_code = re.sub(r'\b' + original + r'\b', obfuscated, obfuscated_code)

        self.ir_to_bytecode(obfuscated_code, output_path)
        return obfuscated_code, obfuscated_types

    def tokenize_code(self, code: str, keep_comments: bool = False, process_strings: bool = True) -> tp.List[str]:
        tokens = re.findall(r'\w+|\S', code)
        return tokens

    def detokenize_code(self, code: tp.Union[tp.List[str], str]) -> str:
        if isinstance(code, list):
            code = ' '.join(code)
        return code

    def extract_functions(self, code: tp.Union[str, tp.List[str]], tokenized: bool = True) -> tp.Tuple[tp.List[str], tp.List[str]]:
        if isinstance(code, list):
            code = ' '.join(code)
        functions = re.findall(r'\b(\w+\s*\(.*?\)\s*\{)', code)
        return functions, code

    def get_function_name(self, function: str) -> str:
        match = re.match(r'\b(\w+)\s*\(', function)
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

# Register the BytecodeProcessor to LangProcessor
BytecodeProcessor.__init_subclass__()

# Add a debug print statement to check registration
print("Registered languages:", LangProcessor.processors)
