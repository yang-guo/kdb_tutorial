# Basic syntax and conventions

## Assignment
The most common way of assigning a value to a variable is `:`. e.g.
```
a:1             /assigns 1 to a
fn:{x+y}        /assigns the function to fn
lst:enlist "a"  /creates a list with a single value "a"
```

The other way to assign a value is to use the `set` keyword.  This can be useful for assigning values to dynamic names, e.g.:
```
k:`a
k set 1
a /displays 1
```


## Operator precedence
kdb's order of operation runs right to left, and there is no concept of precedence, e.g.
```
3*4+5     /27
(3*4)+5   /17
5+3*4     /17
```
The motivation is to reduce the number of parenthesis that needs to be used as most formulas can be repositioned in a way that does not use parentheses.  This is also useful for creating very dense statements, e.g.:
```
/create a matrix, transposes it, assigns it to mat
/counts the columns of mat and assigns the count to n
/then checks if it's less than 10
10 > n:count mat:flip (1 2 3 4;5 6 7 8;9 10 11 12)

/randomly selects 10 values, assigns it to x
/square x, assign it to y, then add 10 to y
10+y:x*x:10?10
```


## Comparisons
kdb has 7 general comparison functions, `=, <>, <, >, <=, >=, ~`.  First 6 are fairly obvious (equals, not equals, less than, greater than, less than or equal to, greater than or equal to respectively).  The last comparison `~` requires a little more explanation.

The match operator `~` compares if two values are identical, with identical defined as:
- same data type
- same value within tolerance (when data type is float)
- same enumeration (when data type is symbol)
- same order (if it's a list)

In addition, it will also return a single boolean.  The operator is very useful when multiple data types can return from a function (which can generate an error if using `=`).  e.g.
```
1~1                         /returns 1b (true)
1~1.                        / return 0b (false)
([]a:til 10; b:til 10)~"a"  /returns 0b (false) - comparisons of one data type to another is valid with match
```

The other comparison functions will compare either an atom with a list or equal-lengthed lists element by element, and error otherwise  e.g.
```
1=1 2 3       /returns 100b
1 2 3=1 2 3   /returns 111b
1 2=1 2 3     /'length error
```

## Binary operators
kdb also generalizes and/or/xor (`&,|,<>`) - in fact they are treated as a special case of `min/max/<>` respectively for binary values.  As with the above, these comparisons work on atom vs list or equal-lengthed lists, e.g.:
```
111b & 001b     /returns 001b
111b | 001b     /returns 111b
111b <> 001b    /returns 110b

5 5 5 & 10 3 3    /returns 5 3 3
5 5 5 | 10 3 3    /returns 10 5 5
5 5 5 <> 10 3 3   /returns 000b
```


## Char lists vs symbols
kdb comes with two "versions" of strings, char lists (commonly called strings) and symbols (interned strings).  Char lists are treated as a list of characters, and work like a regular list in every way.  symbols are used for more efficient storage and lookup, as the values are interned, and symbols can also be enumerated (i.e. internally represented as a long).  The general guideline is to use strings when the text is free form (e.g. news articles, descriptions), and use symbols for highly repeated values (e.g. ticker symbols, category names, etc.)

Symbols are declared by using the ``` ` ``` symbol.  Since spaces will break the declaration, the way to declare symbols with spaces is by casting a char list, e.g.:
```
c:"hello world" /char list
s:`hello /symbol
s:`$"hello world" /symbol
```

A symbol is enumerated when it gets cast with a symbol list.  This will convert a symbol list to integers underneath (very similar to the concept of factors in R)
```
e:`a`b`c
val:`a`b`c`b`a`b`c`c`c`c`c`c`c
enum:`e$val
"i"$enum   /returns 1 2 1 0 1 2 2 2 2 2 2 2i
"i"$val    /errors 'type
```


## Leading whitespace
One particular quirk that's a very common source of bugs is making sure a leading whitespace exists in multi-line declarations.  The leading whitespace is a line continuation symbol, and kdb will parse statements only when it reaches a line without a space (this includes an empty line).  Also note that this means that the parser will treat a multi-line definition as one line, so if it's a function, you have to add semi-colons between statements otherwise it will generate an error.
```
fn:{[a;b] a+b}  /this is okay
fn:{[a;b]
 a+b}           /this is okay
fn:{[a;b]
a+b}            /this will generate an error
fn:{[a;b]
 a+b;
 a-b}           /this is okay
fn:{[a;b]
 a+b
 a-b}           /this will generate an error
```

