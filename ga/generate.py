from output.assertion import *
from recognition.code_recognition import *
from output.test_file_generator import *
from os.path import exists
import subprocess
import string
import random
import sys
sys.path.append('../output')
sys.path.append('../recognition')


def null_generator(real: any) -> any:
    return_value = real
    rand_boolean = random.randint(0, 1)
    if rand_boolean == 1:
        return_value = None
    return return_value


def generate_parent(class_name: str, function: Function, i: int, is_companion:bool=True) -> Assertion:
    parent = Assertion()
    parent.type = AssertType.EQUALS
    parent.name = function.name + "_" + str(i)
    if is_companion:
        parent.real_function = class_name + "." + function.name
    else:
       parent.real_function = "classTest." + function.name 

    if function.return_value == None:
        return None

    for param in function.params:
        data_type = param.return_value
        if data_type == "Int":
            rand_real: int = random.randint(-100, 100)
            if function.return_nullable == True:
                parent.real.append(null_generator(rand_real))
            else:
                parent.real.append(rand_real)
        elif data_type == "Double" or data_type == "Float":
            rand_real: float = random.uniform(-100.0, 100.0)
            if function.return_nullable == True:
                parent.real.append(null_generator(rand_real))
            else:
                parent.real.append(rand_real)
        elif data_type == "String":
            rand_n = random.randint(1, 20)
            rand_string = "".join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(rand_n))
            if function.return_nullable == True:
                parent.real.append(null_generator(rand_string))
            else:
                parent.real.append(rand_string)
        elif data_type == "Boolean":
            rand_boolean = random.randint(0, 1)
            if rand_boolean == 0:
                if function.return_nullable == True:
                    parent.real.append(null_generator(False))
                else:
                    parent.real.append(False)
            else:
                if function.return_nullable == True:
                    parent.real.append(null_generator(True))
                else:
                    parent.real.append(True)
    print_main_kotlin(parent, is_companion=is_companion, class_body=class_name)
    if not exists("./kotlin_app/app/src/main/kotlin/kotlin_app/" + class_name + ".kt"):
        subprocess.run(["copy", "C:\\Users\\LEGION\\Documents\\Data\\Kuliah\\Semester4\\TA\\Python\\subject\\kotlin" + "\\" + class_name + ".kt",
            "C:\\Users\\LEGION\\Documents\\Data\\Kuliah\\Semester4\\TA\\Python\\kotlin_app\\app\\src\\main\\kotlin\\kotlin_app" + "\\" + class_name + ".kt"], shell=True)
        
    process = subprocess.run(["gradle", "run"],shell=True, cwd="./kotlin_app",capture_output=True, text=True)
    output = process.stdout

    data_type = function.return_value
    index = output.find(":app:run") + len(":app:run") + 1
    index_n = output.find("BUILD SUCCESSFUL") - 1
    expected = output[index:index_n]
    print("Expected Value", expected)
    if data_type == "Boolean":
        if expected == "true":
            parent.expected = True
        else:
            parent.expected = False
    elif data_type == "Int":
        parent.expected = int(expected)
    elif data_type == "Double" or data_type == "Float":
        parent.expected = float(expected)
    else:
        parent.expected = expected

    return parent
