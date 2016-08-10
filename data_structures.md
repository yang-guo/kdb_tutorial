# Data structures

Other than atomic values (integer, long, floats, boolean, char, etc.) kdb has four key collection-based data structures.  These structures make up the majority of data storage, and a lot of real-world applications involve transforming and manipulating them.

## Lists
Lists are a collection of values (either atoms or other data structures).  Lists are generally created using ```(...)```, but single-valued lists can also be created using ```enlist```, e.g.:
```
jlst:(1;2;3;4)        /integer list
olst:(1;"a";`a`b!1 2) /untyped list
slst:enlist 1         /typed list with a single item
slst~1                /0b - single item list is not same as an atom
```

There's two type of lists, typed and untyped.  If all members of a list are the same type, 

## Dictionaries

## Tables

## Keyed tables
