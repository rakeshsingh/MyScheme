# To Do

### Unimplemented features

-[ ] Hygenic R5RS Macros
-[ ] Tail call optimisation
-[ ] Variadic lambdas
-[ ] Nested define statements
-[ ] File I/O
-[ ] Closures

### Known bugs

-[ ] `(eq? 1 1.0)`
-[ ] Error checking in `exact` and `inexact`
-[ ] `/` doesn't check type of arguments
-[ ] `car` crashes on non-lists
-[ ] No external representations for defmacro
-[ ] String literals are mutable (so string-set! violates specification)
-[ ] List literals are mutable (so set-car! would violate specification)
-[ ] Using set-cdr! to make a circular list crashes
-[ ] Remainder is not defined for floating point numbers
-[ ] Interpreter is case sensitive
-[ ] Complex returns true on real numbers
-[ ] `cond` doesn't allow multiple statements after a conditional

### Cleanup tasks

-[ ] Add slice support for our linked list, then clean up variadic
  function stuff
-[ ] Remove `eval_program` -- it's just  `map(eval_s_expression, s_expressions)`
-[ ] Rename `internal_result` to `actual_result` in tests.py
-[ ] Fix width of evaluator.py
-[ ] Distinguish between incorrect type errors and incorrect arity  errors, printing accordingly
-[ ] Need a check_type() function
-[ ] Move the more complex maths operations (`exp`, `log` etc) to library.scm
-[ ] Add a base class for Nil and Cons
-[ ] Add assertions to atoms to make sure they only hold the correct type
-[ ] Add tests for type checking on built-ins and primitives
-[ ] Test type coercion for arithmetic (e.g. `(+ 1 2.0)`)
-[ ] Test external representations

### Future ideas

-[ ] Compare with other Scheme interpreters written in Python for
  elegance of approach, error friendliness, performance, test coverage
-[ ] Stack traces on error with line numbers
-[ ] Add documentation via [docco](https://github.com/jashkenas/docco)
-[ ] Remove PLY dependency
-[ ] Explore R5RS compliance with http://sisc-scheme.org/r5rs_pitfall.php
