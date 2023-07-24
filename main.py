from recognition.recognition import *
from ga.generate import *
from ga.ga import *
from ga.parent import *
from output.test_file_generator import *
from output.assertion import *
import sys
sys.path.append('recognition')
sys.path.append('ga')
sys.path.append('output')


def main():
    # Fill with information for raw AST, summary AST, and unit test file name
    summary = "./subject/CHANGE_THIS.summary.txt"
    raw = "./subject/CHANGE_THIS.raw.txt"
    file_name = "CHANGE_THIS"

    summary_text = ""
    raw_text = ""
    with open(summary, "r") as f:
        summary_text = f.read()
    with open(raw, "r") as f:
        raw_text = f.read()

    file_kt = file_recognition(summary_text, raw_text)
    for fun in file_kt.class_body.functions:
        print("Function Branch Count ", fun.branch)
        print("ClassType", file_kt.class_body.type)
        print("FunName", fun.name)

    ga = GeneticAlgorithm(class_name=file_kt.class_body.name,
                          functions=file_kt.class_body.functions, 
                          iteration=100, 
                          parent_count=8, 
                          is_companion=file_kt.class_body.is_companion, 
                          max_generation=7,
                          class_type=file_kt.class_body.type)
    ga.do_process()
    class_parent = ga.get_best_parent()
    print(class_parent.branch_coverage)
    for parent in class_parent.parents:
        print(len(parent.assertions))
        print(parent.branch_coverage)

    print_to_file(class_body=file_kt.class_body, class_parent=class_parent,
                  package=file_kt.package, file_name=file_kt.class_body.name + file_name, is_companion=file_kt.class_body.is_companion)


if __name__ == "__main__":
    main()
