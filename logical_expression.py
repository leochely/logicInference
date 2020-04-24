#!/usr/bin/env python

# -------------------------------------------------------------------------------
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#
# Created:     09/25/2011
# Last Edited: 07/22/2013
# Notes:       *This contains code ported by Christopher Conly from C++ code
#               provided by Dr. Vassilis Athitsos
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so put it in a list which is
#               passed by reference. We can also now pass just one variable in
#               the class and the function will modify the class instead of a
#               copy of that variable. So, be sure to pass the entire list to a
#               function (i.e. if we have an instance of logical_expression
#               called le, we'd call foo(le.symbol,...). If foo needs to modify
#               le.symbol, it will need to index it (i.e. le.symbol[0]) so that
#               the change will persist.
#              *Written to be Python 2.4 compliant for omega.uta.edu
# -------------------------------------------------------------------------------

import sys
from copy import copy
from itertools import chain, product
from tt import BooleanExpression

# -------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos


class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.

    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []


def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print('\nINVALID\n')

    elif expression.symbol[0]:  # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else:  # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        # It's the beginning of a connective
        elif input_string[counter[0]] == '(':
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print('\nUnexpected end of input.\n')
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    word = ''
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                  (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                  (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and expression.connective[0].lower() != 'or' and expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
# -------------------------------------------------------------------------------

# Add all your functions here


def return_expression(expression):
    if expression == 0 or expression == None or expression == '':
        print('\nINVALID\n')

    elif expression.symbol[0]:  # If it is a base case (symbol)
        s = expression.symbol[0]

    else:  # Otherwise it is a subexpression
        s = '('
        if expression.connective[0] == 'or' or expression.connective[0] == 'and' or expression.connective[0] == 'xor':
            for i in range(len(expression.subexpressions)):
                s += ' '
                s += return_expression(expression.subexpressions[i])
                if i != len(expression.subexpressions) - 1:
                    s += ' '
                    s += expression.connective[0]
        elif expression.connective[0] == 'if' or expression.connective[0] == 'iff':
            s += return_expression(expression.subexpressions[0])
            s += ' '
            if expression.connective[0] == 'if':
                s += 'impl'
            else:
                s += expression.connective[0]
            s += ' '
            s += return_expression(expression.subexpressions[1])
        else:
            s += 'not '
            s += return_expression(expression.subexpressions[0])
        s += ')'
    return s


def extract_symbols(expression, symbols):
    if expression.symbol[0]:
        return expression.symbol[0]
    else:
        for substatement in expression.subexpressions:
            symbols.append(extract_symbols(substatement, symbols))


def clean_list(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list and num is not None:
            final_list.append(num)
    return final_list


def cleanNullTerms(d):
    return {
        k: v
        for k, v in d.items()
        if v is not None
    }


def populate_truth_table(knowledge_base, truth_table):
    for subexpression in knowledge_base.subexpressions:
        if subexpression.connective == ['not']:
            if subexpression.subexpressions[0].symbol[0]:
                truth_table[subexpression.subexpressions[0].symbol[0]] = False
        elif subexpression.connective == ['']:
            if subexpression.symbol[0]:
                truth_table[subexpression.symbol[0]] = True


def entail(knowledge_base, truth_table, statement):
    kb = BooleanExpression(knowledge_base)
    t = cleanNullTerms(truth_table)

    combinations = []
    with kb.constrain(**t):
         for c in kb.sat_all():
            combinations.append(c)
    # print(len(combinations))


    kb_true = '{} and {}'.format(knowledge_base, statement)
    kb_true = BooleanExpression(kb_true)


    combinations_true = []
    with kb_true.constrain(**t):
         for c in kb_true.sat_all():
            combinations_true.append(c)

    # print('True')
    # print(len(combinations_true))
    # for c in combinations_true:
    #     print(c)

    kb_false = '{} and (not {})'.format(knowledge_base, statement)
    kb_false = BooleanExpression(kb_false)

    combinations_false = []
    with kb_false.constrain(**t):
         for c in kb_false.sat_all():
            combinations_false.append(c)

    # print('False')
    # print(len(combinations_false))
    # for c in combinations_false:
    #     print(c)

    if len(combinations_true) == len(combinations) and len(combinations_false) == len(combinations):
        print('BTF')
        return 'BTF'
    elif len(combinations_true) == len(combinations) and len(combinations_false) != len(combinations):
        print('DT')
        return 'DT'
    elif len(combinations_true) != len(combinations) and len(combinations_false) == len(combinations):
        print('DF')
        return 'DF'
    else:
        print('PTF')
        return 'PTF'


def check_true_false(knowledge_base, truth_table, statement):
    case = entail(knowledge_base, truth_table, statement)
    with open('result.txt', 'w') as file:
        if case == 'BTF':
            file.write('both true and false')
        elif case == 'DT':
            file.write('definitely true')
        elif case == 'DF':
            file.write('definitely false')
        else:
            file.write('possibly true, possibly false')
