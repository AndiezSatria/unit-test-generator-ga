from recognition.recognition import *
from ga.generate import *
from ga.parent import *
from output.assertion import *
import sys
sys.path.append('../recognition')
sys.path.append('../ga')
sys.path.insert(0, 'output')


def print_to_file(class_body: ClassBody, class_parent: ClassParent, package: str, file_name: str):
    printed = """package """ + package + "\n"
    printed += """
import kotlin.test.Test
import kotlin.test.assertNotEquals
import kotlin.test.assertEquals

    """
    printed += "class " + class_body.name + "Test() {\n"
    for i in range(0, len(class_body.functions)):
        printed += """    @Test
    fun """ + class_body.functions[i].name + "Test() {\n"
        for assertion in class_parent.parents[i].assertions:
            if assertion.type == AssertType.ASSERT:
                printed += "        assert("
            elif assertion.type == AssertType.EQUALS:
                printed += "        assertEquals("
            elif assertion.type == AssertType.NOT_EQUALS:
                printed += "        assertNotEquals("
            if type(assertion.expected) is str:
                printed += str(assertion.expected) + r'''")''' + ", "
            else:
                printed += str(assertion.expected) + ", "

            printed += assertion.real_function + "("
            for j in range(0, len(assertion.real)):
                if type(assertion.real[j]) is str:
                    string = '''"''' + str(assertion.real[j]) + '''"'''
                    printed += string
                else:
                    printed += str(assertion.real[j])
                if j != len(assertion.real) - 1:
                    printed += ", "
                else:
                    printed += ")\n"
        printed += "    }\n"
    printed += "}"

    try:
        with open("./output/kotlin/" + file_name + ".kt", "w+") as f:
            f.write(printed)
            print("File " + file_name + ".kt has been created")
            f.close()
    except:
        print("There is error occured")


def print_to_kotlin_app(class_body: str, functions: list[Function], class_parent: ClassParent, file_name: str):
    printed = """package kotlin_app\n\n"""
    printed += """
import kotlin.test.Test
import kotlin.test.assertNotEquals
import kotlin.test.assertEquals

    """
    printed += "class " + class_body + "Test() {\n"
    for i in range(0, len(functions)):
        printed += """    @Test
    fun """ + functions[i].name + "Test() {\n"
        for assertion in class_parent.parents[i].assertions:
            if assertion.type == AssertType.ASSERT:
                printed += "        assert("
            elif assertion.type == AssertType.EQUALS:
                printed += "        assertEquals("
            elif assertion.type == AssertType.NOT_EQUALS:
                printed += "        assertNotEquals("
            if type(assertion.expected) is str:
                printed += str(assertion.expected) + r'''")''' + ", "
            else:
                printed += str(assertion.expected) + ", "

            printed += assertion.real_function + "("
            for j in range(0, len(assertion.real)):
                if type(assertion.real[j]) is str:
                    string = '''"''' + str(assertion.real[j]) + '''"'''
                    printed += string
                else:
                    printed += str(assertion.real[j])
                if j != len(assertion.real) - 1:
                    printed += ", "
                else:
                    printed += ")"
            printed += ")\n"
        printed += "    }\n"
    printed += "}"

    try:
        with open("./kotlin_app/app/src/test/kotlin/kotlin_app/" + file_name + ".kt", "w+") as f:
            f.write(printed)
            print("File " + file_name + ".kt has been created")
            f.close()
    except:
        print("There is error occured")
