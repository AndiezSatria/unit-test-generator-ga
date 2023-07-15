from enum import Enum

class ClassType(Enum):
    CLASS = "class"
    OBJECT = "object"
    ABSTRACT = "abstract"
    INTERFACE = "interface"

class Declaration(Enum):
    VAR = "var"
    VAL = "val"

class Statement:
    variables: list[any] = []
    literals: list[str] = []
    expressions: list[str] = []
    declaration: Declaration = None
    is_return: bool = False
    branch_condition = None
    branch_expressions = []

    def __init__(self):
        self.literals = []
        self.expressions = []
        self.declaration = None
        self.variables = []
        self.is_return = False
        self.branch_condition = None
        self.branch_expressions = []


class Parameter:
    name = ""
    return_value = None
    default_value = None
    return_nullable = False

    def __init__(self, name="",return_value=None, return_nullable=False) -> None:
        self.name = name
        self.return_value = return_value
        self.return_nullable = return_nullable   

class Function:
    name = ""
    params: list[Parameter] = []
    statements = []
    branch: int = 0
    return_value = None
    return_nullable = False

    def __init__(self, name="", params=[], return_value=None, return_nullable=False, statements=[]) -> None:
        self.name = name
        self.params = params
        self.return_value = return_value
        self.return_nullable = return_nullable
        self.statements = statements

    def add_param(self, param: Parameter):
        self.params.append(param)

class ClassBody:
    name = ""
    type: ClassType = None
    is_companion: bool = False
    params: list[Parameter] = []
    functions: list[Function] = []

    def __init__(self, name, params=[], functions=[], type:ClassType = None, is_companion=False) -> None:
        self.name = name
        self.params = params
        self.functions = functions 
        self.type = type 
        self.is_companion = is_companion

class File:
    package = ""
    class_body = None

    def __init__(self, package, class_body: ClassBody=None) -> None:
        self.package = package
        self.class_body = class_body
