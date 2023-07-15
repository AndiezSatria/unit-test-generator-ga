from recognition.recognition import *
from output.test_file_generator import *
from ga.parent import *
from ga.generate import *
import random
import sys
import pandas as pd
import subprocess
from os.path import exists
sys.path.append('../recognition')
sys.path.append('../output')
sys.path.insert(0, 'ga')


class GeneticAlgorithm():
    class_parents: list[ClassParent] = []
    child_class_parents: list[ClassParent]
    iteration: int = 0
    parent_count: int = 0
    max_generation: int = 0
    functions: list[Function] = []
    class_name: str
    is_companion: bool
    class_type: ClassType

    def __init__(self, iteration: int, functions: list, class_name: str, parent_count: int, is_companion: bool, max_generation:int, class_type:ClassType) -> None:
        self.iteration = iteration
        self.functions = functions
        self.class_name = class_name
        self.parent_count = parent_count
        self.is_companion = is_companion
        self.max_generation = max_generation
        self.class_type = class_type
        self.child_class_parents = []
        self.generate_class_parent()

    def do_process(self):
        k = 0
        optimum = True
        while optimum:
            print("Process ", k)
            # Cross Over
            print("===========Cross Over=============")
            for _ in range(0, self.max_generation):
                rand_parent_one = 0
                rand_parent_two = 0
                while rand_parent_one == rand_parent_two:
                    for _ in range(0, 10):
                        rand_parent_one = random.randint(0, len(self.class_parents) - 1)
                        rand_parent_two = random.randint(0, len(self.class_parents) - 1)
                class_parent_one: ClassParent = self.class_parents[rand_parent_one]
                class_parent_two: ClassParent = self.class_parents[rand_parent_two]

                new_class_parent = ClassParent()
                temp_branch_coverage = []
                for j in range(0, len(class_parent_one.parents)):
                    parent_one: Parent = class_parent_one.parents[j]
                    parent_two: Parent = class_parent_two.parents[j]
                    print("Function Tag One", parent_one.tag)
                    print("Function Tag Two", parent_two.tag)

                    new_parent = self.cross_over(
                        parents_one=parent_one, parents_two=parent_two, fun_name=parent_one.tag, return_type=self.functions[j].return_value)
                    new_class_parent.parents.append(new_parent)

                    branch_coverage, new_parent.branch = self.count_fitness(
                        parent=new_parent, class_parent=new_class_parent)

                    new_parent.branch_coverage = branch_coverage
                    temp_branch_coverage.append(branch_coverage)


                new_class_parent.branch_coverage = sum(
                    temp_branch_coverage) / len(temp_branch_coverage)
                self.child_class_parents.append(new_class_parent)
            self.class_parents.extend(self.child_class_parents)
            print("===========End of Cross Over=============")

            # Mutation
            self.mutation()

            # Elitism
            self.elitism()

            best_parent = self.get_best_parent()
            k += 1
            for parent in best_parent.parents:
                print("Branch Coverage", best_parent.branch_coverage)
                print("Count Branch", len(parent.assertions))
                if (best_parent.branch_coverage >= 0.85 and len(parent.assertions) <= parent.branch) or k == self.iteration:
                    optimum = False

    def count_fitness(self, parent: Parent, class_parent: ClassParent) -> tuple[float, int]:
        print_to_kotlin_app(class_body=self.class_name, functions=self.functions,
                            class_parent=class_parent, file_name="Test" + parent.tag, is_companion=self.is_companion)
        if not exists("./kotlin_app/app/src/main/kotlin/kotlin_app/" + self.class_name + ".kt"):
            subprocess.run(["copy", "C:\\Users\\LEGION\\Documents\\Data\\Kuliah\\Semester4\\TA\\Python\\subject\\kotlin" + "\\" + self.class_name + ".kt",
                        "C:\\Users\\LEGION\\Documents\\Data\\Kuliah\\Semester4\\TA\\Python\\kotlin_app\\app\\src\\main\\kotlin\\kotlin_app" + "\\" + self.class_name + ".kt"], shell=True)
        subprocess.run(["gradle", "jacocoTestReport"],
                       shell=True, cwd="./kotlin_app")
        df = pd.read_csv(
            "./kotlin_app/app/build/customJacocoReportDir/test/jacocoTestReport.csv")
        print(df.columns)

        class_name = self.class_name
        if self.is_companion and self.class_type.value is ClassType.CLASS.value:
            class_name += ".Companion"
        df_result = df.loc[df['CLASS'] == class_name]
        instruction_covered = df_result['INSTRUCTION_COVERED']
        instruction_missed = df_result['INSTRUCTION_MISSED']
        branch_covered = df_result['BRANCH_COVERED']
        branch_missed = df_result['BRANCH_MISSED']

        branch = int(branch_covered + branch_missed)
        instruction = int(instruction_covered + instruction_missed)
        coverage = float(instruction_covered) / float(instruction)
        print("Branch Coverage", coverage)
        return coverage, branch
    
    def count_fitness_assert(self, parent: Parent, fun_name: str) -> float:
        print_to_kotlin_app_assert(class_body=self.class_name, fun_name=fun_name, file_name="Test" + parent.tag, parent=parent, is_companion=self.is_companion)
        if not exists("./kotlin_app/app/src/main/kotlin/kotlin_app/" + self.class_name + ".kt"):
            subprocess.run(["copy", "C:\\Users\\LEGION\\Documents\\Data\\Kuliah\\Semester4\\TA\\Python\\subject\\kotlin" + "\\" + self.class_name + ".kt",
                        "C:\\Users\\LEGION\\Documents\\Data\\Kuliah\\Semester4\\TA\\Python\\kotlin_app\\app\\src\\main\\kotlin\\kotlin_app" + "\\" + self.class_name + ".kt"], shell=True)
        subprocess.run(["gradle", "jacocoTestReport"],
                       shell=True, cwd="./kotlin_app")
        df = pd.read_csv(
            "./kotlin_app/app/build/customJacocoReportDir/test/jacocoTestReport.csv")
        print(df.columns)

        class_name = self.class_name
        if self.is_companion and self.class_type.value is ClassType.CLASS.value:
            class_name += ".Companion"
        df_result = df.loc[df['CLASS'] == class_name]
        instruction_covered = df_result['INSTRUCTION_COVERED']
        instruction_missed = df_result['INSTRUCTION_MISSED']

        instruction = int(instruction_covered + instruction_missed)
        coverage = float(instruction_covered) / float(instruction)
        print("Branch Coverage", coverage)
        return coverage

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
                        class_name=self.class_name, 
                        function=fun, 
                        i=i,
                        is_companion=self.is_companion)
                    parent.assertions.append(assertion)

                class_parent.parents.append(parent)
                branch_coverage, parent.branch = self.count_fitness(parent=parent, class_parent=class_parent)

                parent.branch_coverage = branch_coverage
                temp_branch_coverage.append(branch_coverage)

            class_parent.branch_coverage = sum(
                temp_branch_coverage) / len(temp_branch_coverage)
            self.class_parents.append(class_parent)

    def cross_over(self, parents_one: Parent, parents_two: Parent, fun_name: str, return_type:str) -> Parent:
        new_parent = Parent()
        new_parent.tag = fun_name
        new_parent.branch = parents_one.branch
        if len(parents_one.assertions) <= len(parents_two.assertions):
            rand_len = len(parents_one.assertions)
            # if parents_one.branch < rand_len:
            #     rand_len = random.randint(0, len(parents_one.assertions))

            for i in range(0, rand_len):
                # rand_one = random.randint(0, len(parents_one) - 1)
                # rand_two = random.randint(0, len(parents_one) - 1)
                child = Assertion()
                child.type = AssertType.EQUALS
                child.real_function = parents_one.assertions[i].real_function
                child.name = parents_one.assertions[i].name

                # temp_expected = None
                # if rand_parent == 0:
                #     temp_expected = parents_two.assertions[i].expected
                # else:
                #     temp_expected = parents_one.assertions[i].expected
                temp_real = []
                for j in range(0, len(parents_one.assertions[i].real)):
                    rand_parent = random.randint(0, 1)
                    if rand_parent == 0:
                        temp_real.append(parents_one.assertions[i].real[j])
                    else:
                        temp_real.append(parents_two.assertions[i].real[j])
                
                # TODO : Buat function main untuk print hasil crossover untuk mendapatkan expected
                # child.expected = temp_expected
                child.real = temp_real
                print_main_kotlin(child, is_companion=self.is_companion, class_body=self.class_name)
                process = subprocess.run(["gradle", "run"],shell=True, cwd="./kotlin_app",capture_output=True, text=True)
                output = process.stdout

                index = output.find(":app:run") + len(":app:run") + 1
                index_n = output.find("BUILD SUCCESSFUL") - 1
                expected: str = output[index:index_n]
                if return_type == "Boolean":
                    if expected == "true":
                        child.expected = True
                    else:
                        child.expected = False
                elif return_type == "Int":
                    child.expected = int(expected)
                elif return_type == "Double" or return_type == "Float":
                    child.expected = float(expected)
                else:
                    child.expected = expected

                new_parent.assertions.append(child)
                coverage = self.count_fitness_assert(parent=new_parent, fun_name=fun_name)
                if new_parent.branch_coverage >= coverage:
                    new_parent.assertions.remove(child)
                
                new_parent.branch_coverage = coverage
                if coverage == 1.0:
                    break
            print("New Child Assertions ", len(new_parent.assertions))
        else:
            rand_len = len(parents_two.assertions)
            # if parents_one.branch < rand_len:
            #     rand_len = random.randint(0, len(parents_two.assertions))
            for i in range(0, rand_len):
                # rand_one = random.randint(0, len(parents_one) - 1)
                # rand_two = random.randint(0, len(parents_one) - 1)
                child = Assertion()
                child.type = AssertType.EQUALS
                child.real_function = parents_two.assertions[i].real_function
                child.name = parents_one.assertions[i].name

                # temp_expected = None
                # if rand_parent == 0:
                #     temp_expected = parents_two.assertions[i].expected
                # else:
                #     temp_expected = parents_one.assertions[i].expected
                temp_real = []
                for j in range(0, len(parents_two.assertions[i].real)):
                    rand_parent = random.randint(0, 1)
                    if rand_parent == 0:
                        temp_real.append(parents_one.assertions[i].real[j])
                    else:
                        temp_real.append(parents_two.assertions[i].real[j])
                # child.expected = temp_expected
                child.real = temp_real
                print_main_kotlin(child, is_companion=self.is_companion, class_body=self.class_name)
                process = subprocess.run(["gradle", "run"],shell=True, cwd="./kotlin_app",capture_output=True, text=True)
                output = process.stdout

                index = output.find(":app:run") + len(":app:run") + 1
                index_n = output.find("BUILD SUCCESSFUL") - 1
                expected: str = output[index:index_n]
                if return_type == "Boolean":
                    if expected == "true":
                        child.expected = True
                    else:
                        child.expected = False
                elif return_type == "Int":
                    child.expected = int(expected)
                elif return_type == "Double" or return_type == "Float":
                    child.expected = float(expected)
                else:
                    child.expected = expected
                
                new_parent.assertions.append(child)
                coverage = self.count_fitness_assert(parent=new_parent, fun_name=fun_name)
                if new_parent.branch_coverage >= coverage:
                    new_parent.assertions.remove(child)
                
                new_parent.branch_coverage = coverage
                if coverage == 1.0:
                    break
            print("New Child Assertions ", len(new_parent.assertions))

        return new_parent

    def mutation(self):
        for class_parent in self.class_parents:
            temp_branch_coverage = []
            for j in range(0, len(class_parent.parents)):
                for assertion in class_parent.parents[j].assertions:
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

                    print_main_kotlin(assertion, is_companion=self.is_companion, class_body=self.class_name)
                    process = subprocess.run(["gradle", "run"],shell=True, cwd="./kotlin_app",capture_output=True, text=True)
                    output = process.stdout

                    index = output.find(":app:run") + len(":app:run") + 1
                    index_n = output.find("BUILD SUCCESSFUL") - 1
                    expected: str = output[index:index_n]

                    if self.functions[j].return_value == "Boolean":
                        if expected == "true":
                            assertion.expected = True
                        else:
                            assertion.expected = False
                    elif self.functions[j].return_value == "Int":
                        assertion.expected = int(expected)
                    elif self.functions[j].return_value == "Double" or self.functions[j].return_value == "Float":
                        assertion.expected = float(expected)
                    else:
                        assertion.expected = expected

                branch_coverage, class_parent.parents[j].branch = self.count_fitness(parent=class_parent.parents[j], class_parent=class_parent)
                class_parent.parents[j].branch_coverage = branch_coverage
                temp_branch_coverage.append(branch_coverage)
            class_parent.branch_coverage = sum(temp_branch_coverage) / len(temp_branch_coverage)

    def sort_on_branch_coverage(self, class_parent: ClassParent):
        return class_parent.branch_coverage
    
    def sort_on_len_of_assertion(self, class_parent: ClassParent):
        assertions = []
        for parent in class_parent.parents:
            for assertion in parent.assertions:
                assertions.append(assertion)
        return len(assertions)

    def elitism(self):
        temp = []
        temp.extend(self.class_parents)
        temp.sort(key=self.sort_on_len_of_assertion, reverse=False)
        temp.sort(key=self.sort_on_branch_coverage, reverse=True)
        self.class_parents = temp[:self.parent_count]

    def get_best_parent(self) -> ClassParent:
        return self.class_parents[0]
