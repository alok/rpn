#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Reverse Polish Notation calculator. Uses Python's builtin capabilities to do all parsing. """

import ast
import inspect
import sys
from operator import (add, and_, eq, ge, gt, le, lt, mul, ne, neg, not_, or_,
                      sub, truediv)

stack = []


def push(*args, stack=stack) -> None:
    for arg in args:
        stack.append(arg)


def pop(n=1, stack=stack):
    '''Pop `n` elements. Stateful.'''
    # TODO should this be a list instead of a generator?
    return [stack.pop() for _ in range(n)]


input = sys.argv[1:]

UNARY_OPS = {
    'abs': abs,
    '|': abs,
    '~': not_,
    'neg': neg, }

BINARY_OPS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '^': pow,
    '=': eq,
    '>': gt,
    '>=': ge,
    '<=': le,
    '<': lt, }

# merge dicts with ** op
ops = {**UNARY_OPS, **BINARY_OPS}


def get_num_args(f: str) -> int:
    '''Find how many arguments a function takes. Uses `eval()`.'''
    # XXX uses eval()
    return len(inspect.signature(eval(f)).parameters)


def is_float(x: str) -> bool:
    '''  Return True if x can be cast to a float'''
    try:
        float(x)
        return True
    except:
        return False


def rpn(input, stack=stack):
    for token in input:
        # skip whitespace
        if token.isspace():
            continue
        if token.isdigit():
            push(int(token))
        elif is_float(token):
            push(float(token))
        elif token in UNARY_OPS:
            push(UNARY_OPS[token](*pop(n=1)))
        elif token in BINARY_OPS:
            push(BINARY_OPS[token](*pop(n=2)))
        else:
            # To handle bools and such. Order matters, for now.
            push(ast.literal_eval(token))
            # XXX Security vulnerability here, but it does make the calculator more general.
            # push(eval(token + '(*pop(n=' + str(get_num_args(token)) + '))'))
    return stack


if __name__ == '__main__':
    result = rpn(sys.argv[1:], stack)
    if len(result) == 1:
        print(result.pop())
    else:
        print(f'Error in evaluation. Eval stack is {stack}', file=sys.stderr)
