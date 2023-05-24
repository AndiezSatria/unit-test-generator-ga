import sys
sys.path.append('recognition')
sys.path.append('ga')
sys.path.append('output')
from output.assertion import *
from output.test_file_generator import *
from ga.parent import *
from ga.ga import *
from ga.generate import *
from recognition.recognition import *


def main():
    summary_text = ""
    raw_text = ""
    with open("./subject/test.summary.txt", "r") as f:
        summary_text = f.read()
    with open("./subject/test.raw.txt", "r") as f:
        raw_text = f.read()

    file_kt = file_recognition(summary_text, raw_text)
    for fun in file_kt.class_body.functions:
        print("Function Branch Count ", fun.branch)

    ga = GeneticAlgorithm(class_name=file_kt.class_body.name,
                          functions=file_kt.class_body.functions, iteration=100, parent_count=4)
    ga.do_process()
    class_parent = ga.get_best_parent()
    print(class_parent.branch_coverage)
    for parent in class_parent.parents:
        print(len(parent.assertions))
        print(parent.branch_coverage)
    
    print_to_file(class_body=file_kt.class_body, class_parent=class_parent, package=file_kt.package, file_name="TestVersionOne")


if __name__ == "__main__":
    main()
