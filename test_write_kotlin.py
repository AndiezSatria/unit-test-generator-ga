import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def find_function_identifier(word = ""):
    index = word.find("FUN") + len("FUN")
    index_identifier = word[index:].find("Identifier:") + len("Identifier:") + index
    index_enter = word[index_identifier:].find("\n") + index_identifier
    index_space = word[index_identifier:index_enter].find(" ")

    index_function_name = index_enter
    if index_space != -1:
        index_function_name = index_space + index_identifier

    return word[index_identifier:index_function_name]

def find_function_params(word = ""):
    index_param = word.find("parameter")
    if index_param == -1:
        return None
    else:
        index_param += len("parameter")
        index_identifier = index_param
        block_index = word[index_param:].find("blockLevelExpression") + len("blockLevelExpression") + index_param

        i = True
        params = []
        while i:
            param = []

            index_name = word[index_identifier:block_index].find("Identifier:")
            real_index = index_name + len("Identifier:") + index_identifier
            index_enter = word[real_index:].find("\n") + real_index
            index_space = word[real_index:index_enter].find(" ")

            index_function_name = index_enter
            if index_space != -1:
                index_function_name = index_space + real_index
            if index_name != -1:
                index_identifier = real_index
                param.append(word[real_index:index_function_name])
            else:
                i = False

            index_type = word[index_function_name:block_index].find("Identifier:")
            real_index = index_type + len("Identifier:") + index_function_name
            index_enter = word[real_index:].find("\n") + real_index
            index_space = word[real_index:index_enter].find(" ")

            index_type_name = index_enter
            if index_space != -1:
                index_type_name = index_space + real_index
            if index_name != -1:
                index_identifier = real_index
                param.append(word[real_index:index_type_name])
            else:
                i = False
            params.append(param)
        params.remove([])
        return params

img = cv2.imread('parseTree.png')

text = pytesseract.image_to_string(img)
print(text)

# lines = ['fun main() {', "\tprint(\"Hallo\")", "}"]
# with open("demo.kt", "a") as f:

#     for line in lines:
#         f.write(line)
#         f.write('\n')


function_name = find_function_identifier(text)
params = find_function_params(text)
print(function_name)
print(params)