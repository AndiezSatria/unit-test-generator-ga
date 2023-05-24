from code_recognition import *
import sys
sys.path.insert(0, 'recognition')

_default_token = "(DEFAULT_TOKEN_CHANNEL)"


def file_recognition(summary_text: str, raw_text: str):
    index = summary_text.find("PackageHeader") + len("PackageHeader") + 1
    index_braces = summary_text[index:].find(")") + index
    file = File(summary_text[index:index_braces])
    class_body = class_body_recognition(
        summary_text=summary_text, raw_text=raw_text)
    file.class_body = class_body
    return file


def class_body_recognition(summary_text: str, raw_text: str):
    index = summary_text.find("KlassDeclaration") + len("KlassDeclaration") + 1
    index_braces = summary_text[index:].find(")") + index
    index_space = summary_text[index:index_braces].find(" ") + index
    class_type = summary_text[index:index_space]
    class_name = summary_text[index_space+1:index_braces]

    type = None
    if class_type == "object":
        type = ClassType.OBJECT
    elif class_type == "class":
        type = ClassType.CLASS
    elif class_type == "interface":
        type = ClassType.INTERFACE
    elif class_type == "abstract":
        type = ClassType.ABSTRACT

    class_body = ClassBody(class_name, type=type)

    index_class_body = summary_text[index_braces:].find(
        "classBody") + index_braces
    params = param_recognition(
        summary_text=summary_text, start_index=index_braces, end_index=index_class_body)
    class_body.params = params

    class_body.functions = functions_recognition(summary_text, raw_text)

    return class_body


def param_recognition(summary_text: str, start_index: int = 0, end_index: int = -1):
    i = True
    index_param = summary_text[start_index:end_index].find("parameter")
    if index_param == -1:
        return []
    else:
        index_param = index_param + start_index + len("parameter")
        params = []
        while i:
            param = Parameter()

            index_brace = 0
            if end_index == -1:
                index_brace = summary_text[index_param:].find(
                    ")") + index_param
            else:
                index_brace = summary_text[index_param:end_index].find(
                    ")") + index_param

            index_name = index_param + 1
            end_name_index = summary_text[index_name:index_brace].find(
                " ") + index_name
            index_null = summary_text[end_name_index:index_brace].find("?")
            if index_null != -1:
                index_null += end_name_index
                param.return_nullable = True
                param.return_value = summary_text[end_name_index+1:index_null]
            else:
                param.return_value = summary_text[end_name_index+1:index_brace]

            param.name = summary_text[index_name:end_name_index]

            index_brace += 1
            index_default = summary_text[index_brace:end_index].find(
                "Klass"+param.return_value)
            if index_default != -1:
                index_default += index_brace + len("Klass"+param.return_value)
                if end_index == -1:
                    param.default_value = summary_text[index_default:].strip()
                else:
                    param.default_value = summary_text[index_default:end_index].strip(
                    )

            params.append(param)
            new_index_param = summary_text[index_brace:end_index].find(
                "parameter")
            if new_index_param == -1:
                i = False
            else:
                new_index_param = new_index_param + \
                    index_brace + len("parameter")
                index_param = new_index_param
        return params


def functions_recognition(summary_text: str, raw_text: str):
    index_function = summary_text.find("fun")
    if index_function == -1:
        return []
    else:
        functions = []
        index_function += len("fun")
        i = True
        while i:
            function = Function()

            index_brace = summary_text[index_function:].find(
                ")") + index_function
            index_name = index_function + 1
            end_name_index = summary_text[index_name:index_brace].find(
                " ") + index_name
            index_return_value = end_name_index + 1

            function.name = summary_text[index_name:end_name_index]
            if index_return_value != index_brace:
                function.return_value = summary_text[index_return_value:index_brace]

            index_brace += 1
            new_index_param = summary_text[index_brace:].find("fun")

            if new_index_param == -1:
                i = False
            else:
                new_index_param += index_brace
                index_function = new_index_param + len("fun")

            function.params = param_recognition(
                summary_text=summary_text, start_index=index_brace, end_index=new_index_param)
            function.statements, function.branch = statement_recognition(
                raw_text, function.name)
            functions.append(function)
        return functions


def statement_recognition(raw_text: str, func_name: str):
    branch = 1
    statements = []

    fun_name = raw_text.find(func_name)
    fun_body = raw_text[fun_name:].find(
        "functionBody") + len("functionBody") + fun_name

    start_of_fun = raw_text[fun_body:].find(_default_token) + fun_body
    start_of_fun_statement = text_of_enter(
        raw_text[fun_body:start_of_fun]).split(" ")

    # TODO: If first after parameter is equal sign, it is the return statement
    if start_of_fun_statement[0] != 'LCURL':
        statement = Statement()
        statement.is_return = True

    # Find enter after left curl bracket
    start_of_fun += len(_default_token)
    index_n = raw_text[start_of_fun:].find(_default_token) + start_of_fun
    n = text_of_enter(raw_text[start_of_fun:index_n]).split(" ")
    if n[0] == "\\n":
        start_of_fun = index_n + len(_default_token)

    # for next iteration
    next_fun = raw_text[fun_name:].find("fun")
    if next_fun != -1:
        next_fun += fun_name
    i = True
    start_of_fun += len(_default_token)
    current_n = start_of_fun
    while i:
        j = True
        statement = Statement()
        while j:
            index_default_token = raw_text[current_n:].find(
                _default_token) + current_n
            line = text_of_enter(
                raw_text[current_n:index_default_token]).split(" ")
            # Insert the line into statement
            current_n = index_default_token + len(_default_token)
            # print(line)
            if line[0] == "\\n":
                j = False
            else:
                if line[0] == "VAR":
                    statement.declaration = Declaration.VAR
                    continue
                if line[0] == "VAL":
                    statement.declaration = Declaration.VAL
                    continue
                if line[0].lower() == "identifier":
                    statement.variables.append(line[1])
                    continue
                if "literal" in line[0].lower() or "strtext" in line[0].lower():
                    statement.literals.append(line[1])
                    continue
                if "return" in line[0].lower():
                    statement.is_return = True
                    continue
                if "if" in line[0].lower():
                    new_count, current_n, statement.branch_condition, statement.branch_expressions = if_statement(
                        raw_text, current_n)
                    branch *= new_count
                    j = False
                if "else" in line[0].lower():
                    new_count, current_n, statement.branch_condition, statement.branch_expressions = if_statement(
                        raw_text, current_n)
                    branch += new_count
                    j = False
                if "when" in line[0].lower():
                    new_count, current_n, statement.branch_condition, statement.branch_expressions = when_statement(
                        raw_text, current_n)
                    branch *= new_count
                    j = False
                statement.expressions.append(line[0])
        statements.append(statement)
        end_of_fun = raw_text[current_n:].find(_default_token) + current_n
        end_of_fun_statement = text_of_enter(
            raw_text[current_n:end_of_fun]).split(" ")
        # print(end_of_fun_statement)
        if end_of_fun_statement[0] == 'RCURL' or end_of_fun_statement[0] == "\\n":
            i = False
    return statements, branch


def when_statement(text: str, current_index: int):
    branch = 1
    branch_condition = None
    branch_n = current_index
    i = True

    # Condition
    index_token = text[branch_n:].find(_default_token) + branch_n
    branch_line = text_of_enter(text[branch_n:index_token]).split(" ")
    branch_n = index_token + len(_default_token)

    if branch_line[0] == "LPAREN":
        branch_condition = Statement()
        while i:
            index_token = text[branch_n:].find(
                _default_token) + branch_n
            branch_line = text_of_enter(
                text[branch_n:index_token]).split(" ")
            branch_n = index_token + len(_default_token)
            if branch_line[0] == "RPAREN":
                i = False
            else:
                if branch_line[0].lower() == "identifier":
                    branch_condition.variables.append(branch_line[1])
                    continue
                if "literal" in branch_line[0].lower() or "strtext" in branch_line[0].lower():
                    branch_condition.literals.append(branch_line[1])
                    continue
                branch_condition.expressions.append(branch_line[0])
        i = True     
        index_token = text[branch_n:].find(_default_token) + branch_n
        branch_line = text_of_enter(text[branch_n:index_token]).split(" ")

    # Branch Statements
    branch_statements = []
    if branch_line[0] == "LCURL":
        branch_n = index_token + len(_default_token)
        index_token = text[branch_n:].find(_default_token) + branch_n
        branch_line = text_of_enter(text[branch_n:index_token]).split(" ")
        if branch_line[0] == "\\n":
            index_default_token = text[branch_n:].find(
                _default_token) + branch_n
            branch_n = index_default_token + len(_default_token)
        while i:
            j = True
            inner_branch_statements = []
            statement = Statement()
            condition = Statement()

            while j:
                index_default_token = text[branch_n:].find(
                    _default_token) + branch_n
                line = text_of_enter(
                    text[branch_n:index_default_token]).split(" ")
                # Insert the line into statement
                branch_n = index_default_token + len(_default_token)

                if line[0].lower() == "arrow":
                    j = False
                else:
                    if line[0].lower() == "identifier":
                        condition.variables.append(line[1])
                        continue
                    if "literal" in line[0].lower() or "strtext" in line[0].lower():
                        condition.literals.append(line[1])
                        continue
                    condition.expressions.append(line[0])
            branch += 1
            statement.branch_condition = condition
            j = True

            index_token = text[branch_n:].find(_default_token) + branch_n
            branch_line = text_of_enter(text[branch_n:index_token]).split(" ")
            # print("Search LCURL", branch_line)

            if branch_line[0] == "LCURL":
                no_line = False
                branch_n = index_token + len(_default_token)
                index_token = text[branch_n:].find(_default_token) + branch_n
                branch_line = text_of_enter(text[branch_n:index_token]).split(" ")
                # print("Search \\n", branch_line)
                if branch_line[0] == "\\n":
                    index_default_token = text[branch_n:].find(
                        _default_token) + branch_n
                    branch_n = index_default_token + len(_default_token)
                while j:
                    k = True
                    inner_branch_statement = Statement()
                    while k:
                        index_default_token = text[branch_n:].find(
                            _default_token) + branch_n
                        line = text_of_enter(
                            text[branch_n:index_default_token]).split(" ")
                        # Insert the line into statement
                        branch_n = index_default_token + len(_default_token)
                        # print("Inner Branch Statements", line)
                        if line[0] == "\\n" or line[0] == "RCURL":
                            k = False
                            if line[0] == "RCURL":
                                no_line = True
                                j = False
                        else:
                            if line[0] == "VAR":
                                inner_branch_statement.declaration = Declaration.VAR
                                continue
                            if line[0] == "VAL":
                                inner_branch_statement.declaration = Declaration.VAL
                                continue
                            if line[0].lower() == "identifier":
                                inner_branch_statement.variables.append(
                                    line[1])
                                continue
                            if "literal" in line[0].lower() or "strtext" in line[0].lower():
                                inner_branch_statement.literals.append(line[1])
                                continue
                            if "return" in line[0].lower():
                                inner_branch_statement.is_return = True
                                continue
                            if "if" in line[0].lower():
                                new_count, branch_n, inner_branch_statement.branch_condition, inner_branch_statement.branch_expressions = if_statement(
                                    text, branch_n)
                                branch *= new_count
                            if "else" in line[0].lower():
                                new_count, branch_n, inner_branch_statement.branch_condition, inner_branch_statement.branch_expressions = if_statement(
                                    text, branch_n)
                                branch += new_count
                            if "when" in line[0].lower():
                                new_count, branch_n, inner_branch_statement.branch_condition, inner_branch_statement.branch_expressions = when_statement(
                                    text, branch_n)
                                branch *= new_count
                            inner_branch_statement.expressions.append(line[0])
                    inner_branch_statements.append(inner_branch_statement)
                    
                    if not no_line:
                        end_of_fun = text[branch_n:].find(
                            _default_token) + branch_n
                        end_of_fun_statement = text_of_enter(
                            text[branch_n:end_of_fun]).split(" ")
                    
                        # print(end_of_fun_statement)
                        if end_of_fun_statement[0] == "\\n":
                            branch_n = end_of_fun + len(_default_token)
                            end_of_fun = text[branch_n:].find(
                                _default_token) + branch_n
                            end_of_fun_statement = text_of_enter(
                                text[branch_n:end_of_fun]).split(" ")
                    
                        # print(end_of_fun_statement)
                        if end_of_fun_statement[0] == 'RCURL':
                            branch_n = end_of_fun + len(_default_token)
                            j = False
            else:
                j = True
                inner_branch_statement = Statement()
                while j:
                    index_default_token = text[branch_n:].find(
                        _default_token) + branch_n
                    line = text_of_enter(
                        text[branch_n:index_default_token]).split(" ")
                    # Insert the line into statement
                    branch_n = index_default_token + len(_default_token)
                    # print("Inner Branch Statements", line)
                    if line[0] == "\\n":
                        j = False
                    else:
                        if line[0] == "VAR":
                            inner_branch_statement.declaration = Declaration.VAR
                            continue
                        if line[0] == "VAL":
                            inner_branch_statement.declaration = Declaration.VAL
                            continue
                        if line[0].lower() == "identifier":
                            inner_branch_statement.variables.append(line[1])
                            continue
                        if "literal" in line[0].lower() or "strtext" in line[0].lower():
                            inner_branch_statement.literals.append(line[1])
                            continue
                        inner_branch_statement.expressions.append(line[0])
                inner_branch_statements.append(inner_branch_statement)
            
            statement.branch_expressions = inner_branch_statements

            branch_statements.append(statement)

            end_of_fun = text[branch_n:].find(_default_token) + branch_n
            end_of_fun_statement = text_of_enter(
                text[branch_n:end_of_fun]).split(" ")
            
            # print(end_of_fun_statement)
            if end_of_fun_statement[0] == "\\n":
                branch_n = end_of_fun + len(_default_token)
                end_of_fun = text[branch_n:].find(
                    _default_token) + branch_n
                end_of_fun_statement = text_of_enter(
                    text[branch_n:end_of_fun]).split(" ")
                
            # print(end_of_fun_statement)
            if end_of_fun_statement[0] == 'RCURL':
                branch_n = end_of_fun + len(_default_token)
                end_of_fun = text[branch_n:].find(
                    _default_token) + branch_n
                branch_n = end_of_fun + len(_default_token)
                i = False
    return branch, branch_n, branch_condition, branch_statements


def if_statement(text: str, current_index: int):
    branch = 1
    branch_condition = None
    branch_n = current_index
    i = True

    # Condition
    index_token = text[branch_n:].find(_default_token) + branch_n
    branch_line = text_of_enter(text[branch_n:index_token]).split(" ")
    branch_n = index_token + len(_default_token)
    # print("IF STATEMENT", branch_line[0])
    if branch_line[0] == "LPAREN":
        branch_condition = Statement()
        while i:
            index_token = text[branch_n:].find(
                _default_token) + branch_n
            branch_line = text_of_enter(
                text[branch_n:index_token]).split(" ")
            branch_n = index_token + len(_default_token)
            # print(branch_line)
            if branch_line[0] == "RPAREN":
                i = False
            else:
                if branch_line[0].lower() == "identifier":
                    branch_condition.variables.append(branch_line[1])
                    continue
                if "literal" in branch_line[0].lower() or "strtext" in branch_line[0].lower():
                    branch_condition.literals.append(branch_line[1])
                    continue
                branch_condition.expressions.append(branch_line[0])
        i = True
    index_token = text[branch_n:].find(_default_token) + branch_n
    branch_line = text_of_enter(text[branch_n:index_token]).split(" ")


    # Branch Statements
    branch_statements = []
    if branch_line[0] == "LCURL":
        no_line = False
        branch_n = index_token + len(_default_token)
        index_token = text[branch_n:].find(_default_token) + branch_n
        branch_line = text_of_enter(text[branch_n:index_token]).split(" ") 
        if branch_line[0] == "\\n":
            index_default_token = text[branch_n:].find(
                _default_token) + branch_n
            branch_n = index_default_token + len(_default_token)

        while i:
            j = True
            statement = Statement()
            while j:
                index_default_token = text[branch_n:].find(
                    _default_token) + branch_n
                line = text_of_enter(
                    text[branch_n:index_default_token]).split(" ")
                # Insert the line into statement
                branch_n = index_default_token + len(_default_token)
                # print("Branch Statements", line)

                if line[0] == "\\n" or line[0] == "RCURL":
                    j = False
                    if line[0] == "RCURL":
                        no_line = True
                        i = False
                else:
                    if line[0] == "VAR":
                        statement.declaration = Declaration.VAR
                        continue
                    if line[0] == "VAL":
                        statement.declaration = Declaration.VAL
                        continue
                    if line[0].lower() == "identifier":
                        statement.variables.append(line[1])
                        continue
                    if "literal" in line[0].lower() or "strtext" in line[0].lower():
                        statement.literals.append(line[1])
                        continue
                    if "return" in line[0].lower():
                        statement.is_return = True
                        continue
                    if "if" in line[0].lower():
                        new_count, branch_n, statement.branch_condition, statement.branch_expressions = if_statement(
                            text, branch_n)
                        branch *= new_count
                    if "else" in line[0].lower():
                        new_count, branch_n, statement.branch_condition, statement.branch_expressions = if_statement(
                            text, branch_n)
                        branch += new_count
                    if "when" in line[0].lower():
                        new_count, branch_n, statement.branch_condition, statement.branch_expressions = when_statement(
                            text, branch_n)
                        branch *= new_count
                    statement.expressions.append(line[0])
            branch_statements.append(statement)

            if not no_line:
                end_of_fun = text[branch_n:].find(_default_token) + branch_n
                end_of_fun_statement = text_of_enter(text[branch_n:end_of_fun]).split(" ")
                # print(end_of_fun_statement)
                if end_of_fun_statement[0] == "\\n":
                    branch_n = end_of_fun + len(_default_token)
                    end_of_fun = text[branch_n:].find(
                        _default_token) + branch_n
                    end_of_fun_statement = text_of_enter(
                        text[branch_n:end_of_fun]).split(" ")
            
                # print(end_of_fun_statement)
                if end_of_fun_statement[0] == 'RCURL':
                    branch_n = end_of_fun + len(_default_token)
                    end_of_fun = text[branch_n:].find(
                        _default_token) + branch_n
                    end_of_fun_statement = text_of_enter(text[branch_n:end_of_fun]).split(" ")
                    if end_of_fun_statement[0] == "\\n":
                        branch_n = end_of_fun + len(_default_token)
                    
                    i = False
    else:
        i = True
        statement = Statement()
        while i:
            index_default_token = text[branch_n:].find(
                _default_token) + branch_n
            line = text_of_enter(
                text[branch_n:index_default_token]).split(" ")
            # Insert the line into statement
            branch_n = index_default_token + len(_default_token)
            # print("Branch Statements IF", line)
            if line[0] == "\\n":
                i = False
            else:
                if line[0] == "VAR":
                    statement.declaration = Declaration.VAR
                    continue
                if line[0] == "VAL":
                    statement.declaration = Declaration.VAL
                    continue
                if line[0].lower() == "identifier":
                    statement.variables.append(line[1])
                    continue
                if "literal" in line[0].lower() or "strtext" in line[0].lower():
                    statement.literals.append(line[1])
                    continue
                statement.expressions.append(line[0])
        branch_statements.append(statement)

    return branch, branch_n, branch_condition, branch_statements


def text_of_enter(text: str) -> str:
    i = True
    return_text = text
    while i:
        return_text = return_text.lstrip()
        new_index = return_text.find("\n")
        if new_index == -1:
            i = False
        else:
            return_text = return_text[new_index:]
    return_text = return_text.replace("<", "").replace(">", "").strip()
    return return_text
