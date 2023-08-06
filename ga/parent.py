import sys
sys.path.append('../output')
from output.assertion import *

class Parent():
    assertions: list[Assertion] = []
    tag: str = ""
    branch: int = 1
    coverage: float = 0.0

    def __init__(self):
        self.assertions = []
        self.tag = ""
        self.branch = 1
        self.coverage = 0.0
        

class ClassParent():
    parents: list[Parent] = []
    coverage: float = 0.0

    def __init__(self):
        self.parents = []
        self.coverage = 0.0