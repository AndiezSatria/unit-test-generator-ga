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
    variables = []
    literals = []
    expressions = []
    declaration = None
    is_return = False
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
    params = []
    statements = []
    branch = 0
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
    params = []
    functions: list[Function] = []

    def __init__(self, name, params=[], functions=[], type:ClassType = None) -> None:
        self.name = name
        self.params = params
        self.functions = functions 
        self.type = type 

class File:
    package = ""
    class_body = None

    def __init__(self, package, class_body: ClassBody=None) -> None:
        self.package = package
        self.class_body = class_body
