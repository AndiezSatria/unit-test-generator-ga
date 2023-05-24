from output.assertion import *
from recognition.code_recognition import *
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


def generate_parent(class_name: str, function: Function, i: int) -> Assertion:
    parent = Assertion()
    parent.type = AssertType.NOT_EQUALS
    parent.name = function.name + "_" + str(i)
    parent.real_function = class_name + "." + function.name

    if function.return_value == None:
        return None

    data_type = function.return_value
    if data_type == "Int":
        rand_expected: int = random.randint(-10000, 10000)
        if function.return_nullable == True:
            parent.expected = null_generator(rand_expected)
        else:
            parent.expected = rand_expected
    elif data_type == "Double" or data_type == "Float":
        rand_expected: int = random.uniform(-10000.0, 10000.0)
        if function.return_nullable == True:
            parent.expected = null_generator(rand_expected)
        else:
            parent.expected = rand_expected
    elif data_type == "String":
        rand_n = random.randint(1, 20)
        rand_string = "".join(random.choice(
            string.ascii_letters + string.digits + string.punctuation) for _ in range(rand_n))
        if function.return_nullable == True:
            parent.expected = null_generator(rand_string)
        else:
            parent.expected = rand_string
    elif data_type == "Boolean":
        rand_boolean = random.randint(0, 1)
        if rand_boolean == 0:
            if function.return_nullable == True:
                parent.expected = null_generator(False)
            else:
                parent.expected = False
        else:
            if function.return_nullable == True:
                parent.expected = null_generator(True)
            else:
                parent.expected = True
    for param in function.params:
        data_type = param.return_value
        if data_type == "Int":
            rand_real: int = random.randint(-10000, 10000)
            if function.return_nullable == True:
                parent.real.append(null_generator(rand_real))
            else:
                parent.real.append(rand_real)
        elif data_type == "Double" or data_type == "Float":
            rand_real: float = random.uniform(-10000.0, 10000.0)
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
    return parent
