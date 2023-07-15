from recognition.recognition import *
from ga.parent import *
from output.assertion import *
import sys
sys.path.append('../recognition')
sys.path.append('../ga')
sys.path.insert(0, 'output')


def print_to_file(class_body: ClassBody, class_parent: ClassParent, package: str, file_name: str, is_companion: bool):
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
        if not is_companion:
            printed += "        val classTest = " + class_body.name + "()\n"
        for assertion in class_parent.parents[i].assertions:
            if assertion.type == AssertType.ASSERT:
                printed += "        assert("
            elif assertion.type == AssertType.EQUALS:
                printed += "        assertEquals("
            elif assertion.type == AssertType.NOT_EQUALS:
                printed += "        assertNotEquals("
            if type(assertion.expected) is str:
                printed += '''"''' + str(assertion.expected) + '''"''' + ", "
            elif type(assertion.expected) is bool:
                printed += str(assertion.expected).lower() + ","
            else:
                printed += str(assertion.expected) + ", "

            printed += assertion.real_function + "("
            for j in range(0, len(assertion.real)):
                if type(assertion.real[j]) is str:
                    string = '''"''' + str(assertion.real[j]) + '''"'''
                    printed += string
                elif type(assertion.real[j]) is bool:
                    printed += str(assertion.real[j]).lower()
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
        with open("./output/kotlin/" + file_name + ".kt", "w+") as f:
            f.write(printed)
            print("File " + file_name + ".kt has been created")
            f.close()
    except:
        print("There is error occured")


def print_to_kotlin_app(class_body: str, functions: list[Function], class_parent: ClassParent, file_name: str, is_companion: bool):
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
        if not is_companion:
            printed += "        val classTest = " + class_body + "()\n"
        for assertion in class_parent.parents[i].assertions:
            if assertion.type == AssertType.ASSERT:
                printed += "        assert("
            elif assertion.type == AssertType.EQUALS:
                printed += "        assertEquals("
            elif assertion.type == AssertType.NOT_EQUALS:
                printed += "        assertNotEquals("
            if type(assertion.expected) is str:
                printed += '''"''' + str(assertion.expected) + '''"''' + ", "
            elif type(assertion.expected) is bool:
                printed += str(assertion.expected).lower() + ","
            else:
                printed += str(assertion.expected) + ", "

            printed += assertion.real_function + "("
            for j in range(0, len(assertion.real)):
                if type(assertion.real[j]) is str:
                    string = '''"''' + str(assertion.real[j]) + '''"'''
                    printed += string
                elif type(assertion.real[j]) is bool:
                    printed += str(assertion.real[j]).lower()
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


def print_to_kotlin_app_assert(class_body: str, fun_name: str, parent: Parent, file_name: str, is_companion: bool):
    printed = """package kotlin_app\n\n"""
    printed += """
import kotlin.test.Test
import kotlin.test.assertNotEquals
import kotlin.test.assertEquals

"""
    printed += "class " + class_body + "Test() {\n"
    printed += """    @Test
    fun """ + fun_name + "Test() {\n"
    if not is_companion:
        printed += "        val classTest = " + class_body + "()\n"
    for assertion in parent.assertions:
        if assertion.type == AssertType.ASSERT:
            printed += "        assert("
        elif assertion.type == AssertType.EQUALS:
            printed += "        assertEquals("
        elif assertion.type == AssertType.NOT_EQUALS:
            printed += "        assertNotEquals("
        if type(assertion.expected) is str:
            printed += '''"''' + str(assertion.expected) + '''"''' + ", "
        elif type(assertion.expected) is bool:
            printed += str(assertion.expected).lower() + ","
        else:
            printed += str(assertion.expected) + ", "

        printed += assertion.real_function + "("
        for j in range(0, len(assertion.real)):
            if type(assertion.real[j]) is str:
                string = '''"''' + str(assertion.real[j]) + '''"'''
                printed += string
            elif type(assertion.real[j]) is bool:
                printed += str(assertion.real[j]).lower()
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

def print_main_kotlin(assertion: Assertion, is_companion:bool, class_body:str):
    printed = """package kotlin_app
    
fun main() {
"""
    if not is_companion:
        printed += "    val classTest = " + class_body + "()\n"
    printed += "    val result = "
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
    printed += """
    print(result)
}"""
    try:
        with open("./kotlin_app/app/src/main/kotlin/kotlin_app/App.kt", "w+") as f:
            f.write(printed)
            print("File App.kt has been created")
            f.close()
    except:
        print("There is error occured")
