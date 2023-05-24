import random
import sys
import pandas as pd
import subprocess
sys.path.append('../recognition')
sys.path.append('../output')
sys.path.insert(0, 'ga')
from ga.generate import *
from ga.parent import *
from output.test_file_generator import *
from recognition.recognition import *


class GeneticAlgorithm():
    class_parents = []
    iteration: int = 0
    parent_count: int = 0
    functions: list[Function] = []
    class_name: str = ""

    def __init__(self, iteration: int, functions: list, class_name: str, parent_count: int) -> None:
        self.iteration = iteration
        self.functions = functions
        self.class_name = class_name
        self.parent_count = parent_count
        self.generate_class_parent()

    def do_process(self):
        k = 0
        optimum = True
        while optimum:
            print("Process ", k)
            # Cross Over
            print("===========Cross Over=============")
            for i in range(0, len(self.class_parents)):
                rand_parent = random.randint(0, len(self.class_parents) - 1)
                class_parent_one: ClassParent = self.class_parents[i]
                class_parent_two: ClassParent = self.class_parents[rand_parent]

                new_class_parent = ClassParent()
                temp_branch_coverage = []
                for j in range(0, len(class_parent_one.parents)):
                    parent_one: Parent = class_parent_one.parents[j]
                    parent_two: Parent = class_parent_two.parents[j]
                    print("Function Tag One", parent_one.tag)
                    print("Function Tag Two", parent_two.tag)

                    new_parent = self.cross_over(
                        parents_one=parent_one, parents_two=parent_two, fun_name=parent_one.tag)

                    new_class_parent.parents.append(new_parent)
                    branch_coverage = self.count_fitness(
                        branch=new_parent.branch, parent=new_parent, class_parent=new_class_parent)

                    new_parent.branch_coverage = branch_coverage
                    temp_branch_coverage.append(branch_coverage)
                new_class_parent.branch_coverage = sum(
                    temp_branch_coverage) / len(temp_branch_coverage)
                self.class_parents.append(new_class_parent)

            print("===========End of Cross Over=============")

            # Mutation
            self.mutation()

            # Elitism
            self.elitism()

            best_parent = self.get_best_parent()
            k += 1
            if best_parent.branch_coverage >= 0.8 or k == self.iteration:
                optimum = False

    def count_fitness(self, parent: Parent, class_parent: ClassParent, branch: int) -> float:
        print_to_kotlin_app(class_body=self.class_name, functions=self.functions,
                            class_parent=class_parent, file_name="Test" + parent.tag)
        subprocess.run(
            ["cd", "C:\\Users\\LEGION\\Documents\\Data\\Kuliah\\Semester4\\TA\\Python\\kotlin_app"], shell=True)
        subprocess.run(["copy", "C:\\Users\\LEGION\\Documents\\Data\\Kuliah\\Semester4\\TA\\Python\\subject\kotlin" + "\\" + self.class_name + ".kt",
                       "C:\\Users\\LEGION\\Documents\\Data\\Kuliah\\Semester4\\TA\\Python\\kotlin_app\\app\\src\\main\\kotlin\\kotlin_app" + "\\" + self.class_name + ".kt"], shell=True)
        subprocess.run(["gradle", "jacocoTestReport"], shell=True, cwd="./kotlin_app")
        df = pd.read_csv(
            "./kotlin_app/app/build/customJacocoReportDir/test/jacocoTestReport.csv")
        print(df.columns)

        generated_branch = len(parent.assertions)
        if generated_branch > branch:
            return 0.0
        return float(generated_branch) / float(branch)

    def generate_class_parent(self):
        for _ in range(0, self.parent_count):
            class_parent = ClassParent()
            temp_branch_coverage = []
            for fun in self.functions:
                # print("Generate Fun ", fun.name)
                rand = random.randint(1, 50)
                parent = Parent()
                parent.branch = fun.branch
                parent.tag = fun.name
                for i in range(0, rand):
                    assertion = generate_parent(
                        class_name=self.class_name, function=fun, i=i)
                    parent.assertions.append(assertion)
                class_parent.parents.append(parent)
                branch_coverage = self.count_fitness(
                    branch=parent.branch, parent=parent, class_parent=class_parent)
                parent.branch_coverage = branch_coverage
                temp_branch_coverage.append(branch_coverage)
            class_parent.branch_coverage = sum(
                temp_branch_coverage) / len(temp_branch_coverage)
            self.class_parents.append(class_parent)

    def cross_over(self, parents_one: Parent, parents_two: Parent, fun_name: str) -> Parent:
        new_parent = Parent()
        new_parent.tag = fun_name
        new_parent.branch = parents_one.branch
        if len(parents_one.assertions) <= len(parents_two.assertions):
            childs = []
            rand_len = len(parents_one.assertions)
            if parents_one.branch < rand_len:
                rand_len = random.randint(0, len(parents_one.assertions))

            for i in range(0, rand_len):
                # rand_one = random.randint(0, len(parents_one) - 1)
                # rand_two = random.randint(0, len(parents_one) - 1)
                rand_parent = random.randint(0, 1)
                child = Assertion()
                child.type = AssertType.NOT_EQUALS
                child.real_function = parents_one.assertions[i].real_function
                child.name = parents_one.assertions[i].name

                temp_expected = None
                if rand_parent == 0:
                    temp_expected = parents_two.assertions[i].expected
                else:
                    temp_expected = parents_one.assertions[i].expected
                temp_real = []
                for j in range(0, len(parents_one.assertions[i].real)):
                    if rand_parent == 0 and j % 2 == 0:
                        temp_real.append(parents_one.assertions[i].real[j])
                    else:
                        temp_real.append(parents_two.assertions[i].real[j])
                child.expected = temp_expected
                child.real = temp_real
                childs.append(child)
            print("New Child Assertions ", len(childs))
            new_parent.assertions = childs
        else:
            childs = []
            rand_len = len(parents_two.assertions)
            if parents_one.branch < rand_len:
                rand_len = random.randint(0, len(parents_two.assertions))
            for i in range(0, rand_len):
                # rand_one = random.randint(0, len(parents_one) - 1)
                # rand_two = random.randint(0, len(parents_one) - 1)
                rand_parent = random.randint(0, 1)
                child = Assertion()
                child.type = AssertType.NOT_EQUALS
                child.real_function = parents_two.assertions[i].real_function
                child.name = parents_one.assertions[i].name

                temp_expected = None
                if rand_parent == 0:
                    temp_expected = parents_two.assertions[i].expected
                else:
                    temp_expected = parents_one.assertions[i].expected
                temp_real = []
                for j in range(0, len(parents_two.assertions[i].real)):
                    if rand_parent == 0 and j % 2 == 0:
                        temp_real.append(parents_one.assertions[i].real[j])
                    else:
                        temp_real.append(parents_two.assertions[i].real[j])
                child.expected = temp_expected
                child.real = temp_real
                childs.append(child)
            print("New Child Assertions ", len(childs))
            new_parent.assertions = childs

        return new_parent

    def mutation(self):
        for class_parent in self.class_parents:
            for parent in class_parent.parents:
                for assertion in parent.assertions:
                    for i in range(0, len(assertion.real)):
                        temp = assertion.real[i]
                        if type(temp) is int:
                            temp += random.randint(-100, 100)
                        if type(temp) is float:
                            temp += random.uniform(-10.0, 10.0)
                        if type(temp) is str:
                            temp = temp[:-2] + "".join(random.choice(
                                string.ascii_letters + string.digits + string.punctuation) for _ in range(2))
                        if type(temp) is bool:
                            temp = temp or False

                        assertion.real[i] = temp

    def sort_on_branch_coverage(self, class_parent: ClassParent):
        return class_parent.branch_coverage

    def elitism(self):
        self.class_parents.sort(key=self.sort_on_branch_coverage, reverse=True)
        temp = self.class_parents[:self.parent_count]
        self.class_parents = temp

    def get_best_parent(self) -> ClassParent:
        return self.class_parents[0]
