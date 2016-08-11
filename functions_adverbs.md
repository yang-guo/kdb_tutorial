# Functions and adverbs

## Functions and projections
kdb is a functional language, and thus one of the main concepts is arity.  Arity describes the number of arguments a function, and is a core concept.  

The main limit on functions in kdb is that functions can only take a maximum of 8 arguments, however the most common ones are:
- monadic/unary: the function only takes one argument
- dyadic/binary: the function only takes two arguments

The above two types are extremely important because most adverbs (described below) work specifically on monadic or dyadic functions, and thus these functions are particularly powerful.

By default, if no arguments are specified, kdb will accept up to three arguments of `x`, `y` and `z`, in order .e.g:
```
{x+x}   /by default accepts x, function is a monad
{x+y}   /by default accepts x, y, function is a dyad
{y}     /by default accepts x, y, function is a dyad
```

Often in real-world situations a function will have more than one or two arguments, making them ineligible for adverbs.  However we can resolve this by using a concept called projection, which allows you to partially set certain arguments to effectively create functions with a smaller number or arguments.
```
fn:{[a;b;c;d] a+b+c+d}  /function with 4 arguments - we cannot use any adverbs
fn2:fn[1;2]             /we set a=1, b=2, making fn2 a dyadic
fn2[1] each 1 2 3       /we continue to use projection to create a monad so we can use each
```

## Adverbs
Adverbs are a integral part of what makes kdb so powerful.  

`each`
: takes a monad and applies a collection to the function.
```
fn:{x*x}
fn each til 10                                  /takes each element of the list and squares it
{value x} each ([]a:til 10;b:reverse til 10)    /extracts the data from a table row by row
```

`\:`
: takes a dyad `fn[x;y]` and applies each element of `x` to `fn` and `y`. 
```
(til 5),\:1                                         /joins each element in the left list with 1
([]a:til 10;b:reverse til 10) {y value x}\: sum     /sums each row of the left table
```

`/:`
: takes a dyad `fn[x;y]` and applies each element of `y` to `fn` and `x`.
```
1,/:til 5                                           /joins each element in the left list with 1
sum {x value y}/: ([]a:til 10;b:reverse til 10)     /sums each row of the left table
```

`'`
: takes a dyad `fn[x;y]` and applies each element of `x` and `y` to `fn`.  This allows you to turn a dyad that works on atoms to work on lists very easily.  The adverb allows for both atom/collection or two collections of the same length
```
1,'til 10                   /joins 1 to each element of the list
(til 10),'til 10            /joins the lists element by element
([]a:10?`3),'([]b:til 10)   /joins the two tables row by row
```

`':`
: takes a dyad `fn[x;y]` and a collection and applies it along the collection.  If no initial value is specified, the first value is 0N by default
```
({(x;y)}':) til 10 /returns ((0;0N);(1;0);(2;1);(3;2);...)
```

`/`
: over

`\`
: scan
