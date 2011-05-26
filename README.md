Minimal scheme: a toy scheme interpreter written in Python

Targetting R5RS
([HTML copy of spec](http://people.csail.mit.edu/jaffer/r5rs_toc.html)),
or at least an interesting subset of it.

Currently working towards running all the
[code in SICP](http://mitpress.mit.edu/sicp/code/index.html).

All functionality is implemented with corresponding tests. Functions
are generally thorough with their error messages, and we strive to
give informative error messages.

### Terminology

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

`cond`

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
`pair?`, `map` (unary only)

### Strings

`string?`, `make-string`, `string-length`, `string-ref`, `string-set!`

### Macros

`defmacro`

### Other

Comments work too!

## Bugs and tasks

### Unimplemented features

* Hygenic R5RS Macros
* Tail call optimisation
* Variadic lambdas
* Nested define statements
* I/O (so no hello world yet)
* Closures

### Known bugs

* `(eq? 1 1.0)`
* Error checking in `exact` and `inexact`
* `/` doesn't check type of arguments
* `car` crashes on non-lists
* No external representations for defmacro
* String literals are mutable (so string-set! violates specification)
* List literals are mutable (so set-car! would violate specification)
* Using set-cdr! to make a circular list crashes
* Remainder is not defined for floating point numbers
* Interpreter is case sensitive

### Cleanup tasks

* Add slice support for our linked list, then clean up variadic
  function stuff
* Remove eval_program -- it's just map(eval_s_expression,
  s_expressions)
* Rename internal_result to actual_result in tests.py
* Fix width of evaluator.py
* Distinguish between incorrect type errors and incorrect arity
  errors, printing accordingly
* Need a check_type() function
* Move the more complex maths operations (`exp`, `log` etc) to library.scm
* Add a base class for Nil and Cons
* Add assertions to atoms to make sure they only hold the correct type
* Add tests for type checking on built-ins and primitives
* Test type coercion for arithmetic (e.g. `(+ 1 2.0)`)
* Test external representations

### Future ideas

* Compare with other Scheme interpreters written in Python for
  elegance of approach, error friendliness, performance, test coverage
* Stack traces on error with line numbers
* Add documentation via [docco](https://github.com/jashkenas/docco)
* Remove PLY dependency
* Explore R5RS compliance with http://sisc-scheme.org/r5rs_pitfall.php
