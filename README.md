Minimal scheme: a toy scheme interpreter written in Python

[![Build Status](https://secure.travis-ci.org/Wilfred/Minimal-scheme.png?branch=master)](http://travis-ci.org/Wilfred/Minimal-scheme)

# Interpreter

This is a from-scratch Scheme implementation written for pleasure and
education purposes only. It is targetting R5RS
([HTML copy of spec](http://people.csail.mit.edu/jaffer/r5rs_toc.html)),
or at least an interesting subset of it. I'd also like it to run the
[code in SICP](http://mitpress.mit.edu/sicp/code/index.html).

All functionality is implemented with corresponding tests. Functions
are generally thorough with their error messages, and we strive to
give informative error messages.

### Installation

    $ virtualenv ~/.py_envs/scheme -p python3
    $ . ~/.py_envs/scheme/bin/activate
    (scheme)$ pip install -r requirements.pip
    
### Interactive usage
    
    (scheme)$ ./repl
    Welcome to Minimal Scheme 0.1 alpha.
    scheme> (+ 1 1)
    2
    
### Script usage

    (scheme)$ python interpreter/main.py examples/hello-world.scm
    hello world

### Running the tests

    (scheme)$ nosetests interpreter/tests.py

## Terminology

The terms `primitive`, `built-in` and `standard function` are used to
refer to different things in minimal scheme.

A `primitive` is written in Python and controls whether or not it
evaluates its arguments.

A `built-in` is written in Python but has all its arguments evaluated
automatically.

A `standard function` is written in Scheme.

## Functionality implemented

### Primitives

`define`, `lambda`, `if`, `begin`, `quote`, `eqv?`, `eq?`,
`quasiquote`, `unquote`, `unquote-splicing`

### Binding

`let`

### Conditionals

`cond`, `not`, `and` (binary only), `or` (binary only)

### Integers and floats

`number?`, `complex?`, `rational?`, `real?`, `exact?`, `inexact?`,
`+`, `-`, `*`, `/`, `<`, `<=`, `>`, `>=`, `=`, `zero?`, `positive?`,
`negative?`, `odd?`, `even?`, `abs`, `quotient`, `modulo`,
`remainder`, `exp`, `log`

No support for exact fractions or complex numbers.

### Characters

`char?`, `char=?`, `char<?`, `char>?`, `char<=?`, `char>=?`

### Lists

`car`, `cdr`, `caar`, `cadr`, `cdar`, `cddr`, `cons`, `null?`,
`pair?`, `list`, `length`, `set-car!`, `set-cdr!`

### Control

`map` (unary only), `for-each` (unary only), `procedure?`, `apply`

### Vectors

`make-vector`, `vector?`, `vector-ref`, `vector-set!`,
`vector-length`, `vector`, `vector->list`, `list->vector`,
`vector-fill!`

No distinction between constant vectors and normal vectors.

### Strings

`string?`, `make-string`, `string-length`, `string-ref`, `string-set!`

### Macros

`defmacro`

### I/O

`display`, `newline` (both stdout only)

### Other

Comments work too!

# Code Organization
```
├── README.md
├── examples
│   └── hello-world.scm
├── interpreter
│   ├── built_ins
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── chars.py
│   │   ├── control.py
│   │   ├── equivalence.py
│   │   ├── io.py
│   │   ├── lists.py
│   │   ├── numbers.py
│   │   ├── strings.py
│   │   └── vectors.py
│   ├── data_types.py
│   ├── errors.py
│   ├── evaluator.py
│   ├── lexer.py
│   ├── main.py
│   ├── primitives.py
│   ├── scheme_parser.py
│   ├── tests.py
│   └── utils.py
├── repl
├── requirements.txt
└── standard_library
    └── library.scm
```
