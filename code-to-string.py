import marshal
from base64 import b64decode, b64encode
from types import CodeType
from typing import Mapping, Union, Any
from reportlab.pdfgen import canvas

def b64compile(__source: Union[str, bytes, CodeType]):
    typecheck = {
        CodeType: lambda x: x,
        str: lambda x: compile(x, '<string>', 'exec'),
        bytes: lambda x: compile(x.decode('utf-8'), '<string>', 'exec')
    }
    _code_obj = typecheck[type(__source)](__source)
    _code_b64_str = b64encode(marshal.dumps(_code_obj)).decode('utf-8')
    return _code_b64_str

def _base64_to_code_obj(__source: Union[str, bytes]):
    return marshal.loads(b64decode(__source))

def b64exec(__source: Union[str, bytes, CodeType], __locals: Union[Mapping[str, Any], None] = None):
    typecheck = {
        CodeType: lambda x: x,
        bytes: lambda x: _base64_to_code_obj(x),
        str: lambda x: _base64_to_code_obj(x)
    }
    _code = typecheck[type(__source)](__source)
    if not isinstance(__locals, Mapping):
        __locals = {}
    while True:
        try:
            return exec(_code, {}, __locals)
        except NameError as err:
            err.__traceback__ = err.__traceback__.tb_next
            raise err
        
def generate_txt_from_code(compiled_code: str, output_filename: str):
    txt_filename = "texto_codificado.txt"
    with open(txt_filename, "w", encoding="utf-8") as txt_file:
        txt_file.write(compiled_code)
        
if __name__ == '__main__':
    test_string = 'hello world'
    compiled_code = b64compile(b'print(test_string)')
    print(compiled_code)
    generate_txt_from_code(compiled_code, "compiled_code.pdf")
    b64exec(_base64_to_code_obj(compiled_code), __locals={'test_string': test_string })

