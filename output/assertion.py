from recognition.code_recognition import *
import sys
from enum import Enum
sys.path.append('../recognition')


class AssertType(Enum):
    EQUALS = "equeals"
    NOT_EQUALS = "not_equals"
    ASSERT = "assert"


class Assertion:
    name: str = ""
    type: AssertType
    real_function: str = ""
    expected = None
    real = []

    def __init__(self):
        self.name = ""
        self.type = AssertType.EQUALS
        self.real_function = ""
        self.expected = None
        self.real = []
