from evaluator import eval_s_expression
from errors import SchemeTypeError, RedefinedVariable, SchemeSyntaxError, UndefinedVariable
from utils import safe_len, safe_iter
from parser import Atom
from copy import deepcopy

primitives = {}

# a decorator for giving a name to built-in
def name_function(function_name):
    def name_function_decorator(function):
        primitives[function_name] = function

        # we return the function too, so we can use multiple decorators
        return function

    return name_function_decorator


@name_function('define')
def define(arguments, environment):
    if safe_len(arguments) != 2:
        raise SchemeTypeError("Need to pass exactly two arguments to "
                              "`define` (you passed %d)." % safe_len(arguments))

    if isinstance(arguments.head, Atom):
        return define_variable(arguments, environment)
    else:
        return define_function(arguments, environment)


def define_variable(arguments, environment):
    if arguments.head.type != 'SYMBOL':
        raise SchemeTypeError("Tried to assign to a %s, which isn't a symbol." % arguments.head.type)

    if arguments.head.value in environment:
        raise RedefinedVariable("Cannot define %s, as it has already been defined." % arguments.head.value)

    variable_name = arguments.head.value
    variable_value_expression = arguments.tail.head

    result, environment = eval_s_expression(variable_value_expression, environment)
    environment[variable_name] = result

    return (None, environment)


def define_function(arguments, environment):
    function_name_with_parameters = arguments[0]
    function_name = function_name_with_parameters[0]

    if function_name.type != "SYMBOL":
        raise SchemeTypeError("Function names must be symbols, not a %s." % function_name.type)

    # check that all our arguments are symbols:
    function_parameters = function_name_with_parameters.tail

    for parameter in safe_iter(function_parameters):
        if parameter.type != "SYMBOL":
            raise SchemeTypeError("Function arguments must be symbols, not a %s." % parameter.type)

    # check if this function can take a variable number of arguments
    is_variadic = False

    for parameter in safe_iter(function_parameters):
        if parameter.value == '.':
            if is_variadic:
                raise SchemeSyntaxError("May not have . more than once in a parameter list.")
            else:
                is_variadic = True

    if is_variadic:
        return define_variadic_function(arguments, environment)
    else:
        return define_normal_function(arguments, environment)


def define_normal_function(arguments, environment):
    function_name_with_parameters = arguments[0]
    function_name = function_name_with_parameters.head
    function_parameters = function_name_with_parameters.tail

    function_body = arguments.tail[0]
    
    # a function with a fixed number of arguments
    def named_function(_arguments, _environment):
        if safe_len(_arguments) != safe_len(function_parameters):
            raise SchemeTypeError("%s takes %d arguments, %d given." % \
                                      (function_name, safe_len(function_parameters), safe_len(_arguments)))

        local_environment = {}

        # evaluate arguments
        _arguments = deepcopy(_arguments)
        for i in range(safe_len(_arguments)):
            (_arguments[i], _environment) = eval_s_expression(_arguments[i], _environment)

        # assign to parameters
        for (parameter_name, parameter_value) in zip(safe_iter(function_parameters),
                                                          safe_iter(_arguments)):
            local_environment[parameter_name.value] = parameter_value

        # create new environment, where local variables mask globals
        new_environment = dict(_environment, **local_environment)

        # evaluate the function block
        result, final_environment = eval_s_expression(function_body, new_environment)

        # update any global variables that weren't masked
        for variable_name in _environment:
            if variable_name not in local_environment:
                _environment[variable_name] = final_environment[variable_name]

        return (result, _environment)

    # assign this function to this name
    environment[function_name.value] = named_function

    return (None, environment)


def define_variadic_function(arguments, environment):
    function_name_with_parameters = arguments[0]
    function_name = function_name_with_parameters.head
    function_parameters = function_name_with_parameters.tail

    function_body = arguments.tail[0]
    
    dot_position = function_parameters.index(Atom('SYMBOL', '.'))

    if dot_position < len(function_parameters) - 2:
        raise SchemeSyntaxError("You can only have one improper list "
                                "(you have %d parameters after the '.')." % (len(function_parameters) - 1 - dot_position))
    if dot_position == len(function_parameters) - 1:
        raise SchemeSyntaxError("Must name an improper list parameter after '.'.")

    def named_variadic_function(_arguments, _environment):
        # a function that takes a variable number of arguments
        if dot_position == 0:
            explicit_parameters = None
        else:
            explicit_parameters = deepcopy(function_parameters)

            # create a linked list holding all the parameters before the dot
            current_head = explicit_parameters

            # find the position in the list just before the dot
            for i in range(dot_position - 2):
                current_head = current_head.tail

            # then remove the rest of the list
            current_head.tail = None

        improper_list_parameter = function_parameters[dot_position + 1]

        # check we have been given sufficient arguments for our explicit parameters
        if safe_len(_arguments) < safe_len(explicit_parameters):
            raise SchemeTypeError("%s takes at least %d arguments, you only provided %d." % \
                                      (function_name.value, safe_len(explicit_parameters),
                                       safe_len(_arguments)))

        local_environment = {}

        # evaluate arguments
        _arguments = deepcopy(_arguments)
        for i in range(safe_len(_arguments)):
            (_arguments[i], _environment) = eval_s_expression(_arguments[i], _environment)

        # assign parameters
        for (parameter, parameter_value) in zip(safe_iter(explicit_parameters),
                                                safe_iter(_arguments)):
            local_environment[parameter] = parameter_value

        # put the remaining arguments in our improper parameter
        remaining_arguments = _arguments
        for i in range(safe_len(explicit_parameters)):
            remaining_arguments = remaining_arguments.tail

        local_environment[improper_list_parameter.value] = remaining_arguments

        new_environment = dict(_environment, **local_environment)

        # evaluate our function_body in this environment
        (result, final_environment) = eval_s_expression(function_body, new_environment)

        # update global variables that weren't masked by locals
        for variable_name in _environment:
            if variable_name not in local_environment:
                _environment[variable_name] = final_environment[variable_name]

        return (result, _environment)

    # assign this function to this name
    environment[function_name.value] = named_variadic_function

    return (None, environment)


@name_function('set!')
def set_variable(arguments, environment):
    if safe_len(arguments) != 2:
        raise SchemeTypeError("Need to pass exactly two arguments to `set!`.")

    variable_name = arguments.head

    if variable_name.type != 'SYMBOL':
        raise SchemeTypeError("Tried to assign to a %s, which isn't a symbol." % variable_name.type)

    if variable_name.value not in environment:
        raise UndefinedVariable("Can't assign to undefined variable %s." % variable_name.value)

    variable_value_expression = arguments.tail.head
    result, environment = eval_s_expression(variable_value_expression, environment)
    environment[variable_name.value] = result

    return (None, environment)

@name_function('if')
def if_function(arguments, environment):
    if safe_len(arguments) not in [2,3]:
        raise SchemeTypeError("Need to pass either two or three arguments to `if`.")

    condition, environment = eval_s_expression(arguments.head, environment)

    # everything except an explicit false boolean is true
    if not (condition.type == 'BOOLEAN' and condition.value == False):
        then_expression = arguments[1]
        return eval_s_expression(then_expression, environment)
    else:
        if safe_len(arguments) == 3:
            else_expression = arguments[2]
            return eval_s_expression(else_expression, environment)


@name_function('lambda')
def make_lambda_function(arguments, environment):
    if safe_len(arguments) != 2:
        raise SchemeTypeError("Need to pass exactly two arguments to `lambda`.")

    parameter_list = arguments.head
    function_body = arguments.tail.head

    if isinstance(parameter_list, Atom):
        raise SchemeTypeError("The first argument to `lambda` must be a list of variables.")

    for parameter in safe_iter(parameter_list):
        if parameter.type != "SYMBOL":
            raise SchemeTypeError("Parameters of lambda functions must be symbols, not %s." % parameter.type)

    def lambda_function(_arguments, _environment):
        if safe_len(_arguments) != safe_len(parameter_list):
            raise SchemeTypeError("Wrong number of arguments for this "
                                  "lambda function, was expecting %d, received %d" % (safe_len(parameter_list), safe_len(_arguments)))

        local_environment = {}

        for (parameter_name, parameter_expression) in zip(safe_iter(parameter_list),
                                                          safe_iter(_arguments)):
            local_environment[parameter_name.value], _environment = eval_s_expression(parameter_expression, _environment)

        new_environment = dict(_environment, **local_environment)

        # now we have set up the correct scope, evaluate our function block
        (result, final_environment) = eval_s_expression(function_body, new_environment)

        # update any global variables that weren't masked
        for variable_name in _environment:
            if variable_name not in local_environment:
                _environment[variable_name] = final_environment[variable_name]

        return (result, _environment)

    return (lambda_function, environment)


@name_function('quote')
def return_argument_unevaluated(arguments, environment):
    if safe_len(arguments) != 1:
        raise SchemeTypeError("Quote takes exactly one argument, received %d" % safe_len(arguments))

    return (arguments.head, environment)


@name_function('begin')
def evaluate_sequence(arguments, environment):
    result = None

    for argument in arguments:
        result, environment = eval_s_expression(argument, environment)

    return (result, environment)