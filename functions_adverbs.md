# Functions and adverbs

## Functions and projections
kdb is a functional language, and thus one of the main concepts is arity.  Arity describes the number of arguments a function, and is a core concept.  

The main limit on functions in kdb is that functions can only take a maximum of 8 arguments, however the most common ones are:
- monadic/unary: the function only takes one argument
- dyadic/binary: the function only takes two arguments

The above two types are extremely important because most adverbs (described below) work specifically on monadic or dyadic functions, and thus these functions are particularly powerful.

Often in real-world situations a function will have more than one or two arguments, making them ineligible for adverbs.  However we can resolve this by using a concept called projection, which allows you to partially set certain arguments to effectively create functions with a smaller number or arguments.

## Adverbs
Adverbs are a integral part of what makes kdb so powerful.  

`each`
: each monad

`\:`
: each left

`/:`
: each right

`'`
: each both

`':`
: each prior

`/`
: over

`\`
: scan
