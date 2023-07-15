import sys
sys.path.append('../output')
from output.assertion import *

class Parent():
    assertions: list[Assertion] = []
    tag: str = ""
    branch: int = 1
    branch_coverage: float = 0.0

    def __init__(self):
        self.assertions = []
        self.tag = ""
        self.branch = 1
        self.branch_coverage = 0.0
        

class ClassParent():
    parents: list[Parent] = []
    branch_coverage: float = 0.0

    def __init__(self):
        self.parents = []
        self.branch_coverage = 0.0