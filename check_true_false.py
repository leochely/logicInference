#!/usr/bin/env python

# -------------------------------------------------------------------------------
# Name:        check_true_false
# Purpose:     Main entry into logic program. Reads input files, creates
#              base, tests statement, and generates result file.
#
# Created:     09/25/2011
# Last Edited: 07/22/2013
# Notes:       *Ported by Christopher Conly from C++ code supplied by Dr.
#               Vassilis Athitsos.
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so I put it in a list, which
#               is passed by reference.
#              *Written to be Python 2.4 compliant for omega.uta.edu
# -------------------------------------------------------------------------------

import sys
from logical_expression import *
from tt import BooleanExpression


def main(argv):
    symbols = []

    if len(argv) != 4:
        print(
            'Usage: %s [wumpus-rules-file] [additional-knowledge-file] [input_file]' % argv[0])
        sys.exit(0)

    # Read wumpus rules file
    try:
        input_file = open(argv[1], 'r')
    except:
        print('failed to open file %s' % argv[1])
        sys.exit(0)

    # Create the knowledge base with wumpus rules
    print('\nLoading wumpus rules...')
    knowledge_base = logical_expression()
    knowledge_base.connective = ['and']
    for line in input_file:
        # Skip comments and blank lines. Consider all line ending types.
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        # A mutable counter so recursive calls don't just make a copy
        counter = [0]
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        knowledge_base.subexpressions.append(subexpression)
    input_file.close()

    # Read additional knowledge base information file
    try:
        input_file = open(argv[2], 'r')
    except:
        print('failed to open file %s' % argv[2])
        sys.exit(0)

    # Add expressions to knowledge base
    print('Loading additional knowledge...')
    for line in input_file:
        # Skip comments and blank lines. Consider all line ending types.
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        counter = [0]  # a mutable counter
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        knowledge_base.subexpressions.append(subexpression)
    input_file.close()

    # Verify it is a valid logical expression
    if not valid_expression(knowledge_base):
        sys.exit('invalid knowledge base')

    # I had left this line out of the original code. If things break, comment out.
    # print_expression(knowledge_base, '\n')

    extract_symbols(knowledge_base, symbols)
    symbols = clean_list(symbols)
    truth_table = {k: None for _, k in enumerate(symbols)}
    populate_truth_table(knowledge_base, truth_table)


    knowledge_base = return_expression(knowledge_base)
    print(knowledge_base)


    # Read statement whose entailment we want to determine
    try:
        input_file = open(argv[3], 'r')
    except:
        print('failed to open file %s' % argv[3])
        sys.exit(0)
    print('Loading statement...')
    statement = input_file.readline().rstrip('\r\n')
    input_file.close()

    # Convert statement into a logical expression and verify it is valid
    statement = read_expression(statement)
    if not valid_expression(statement):
        sys.exit('invalid statement')

    # Show us what the statement is
    print('\nChecking statement: ')
    print_expression(statement, '')
    print('\n')

    statement = return_expression(statement)

    # Run the statement through the inference engine
    check_true_false(knowledge_base, truth_table, statement)

    sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
