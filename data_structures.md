# Data structures

Atoms are the basic building blocks of kdb, and represent single numbers, characters, dates and timestamps.

Other than atoms (integer, long, floats, boolean, char, etc.) kdb has four key collection-based data structures.  These structures make up the majority of data storage, and a lot of real-world applications involve transforming and manipulating them.


## Atoms and types
Atoms are single values, and in kdb all atoms have a type.  Every single atom has both a string and a numeric representation for its type.  For the numeric representation atoms will have a negative value (e.g. `-7h`) while typed lists will have a positive value (e.g. `7h`)

Other than the usual data types, kdb also has a set of useful atoms specifically for time series:
```
ts:.z.P       /get current date and time as a timestamp type (value has up to nanosecond precision, and stored as a long)
dt:"z"$ts     /convert timestamp to a datetime (value has up to millisecond precision, and stored as a float)
m:"m"$ts      /convert timestamp to a month type (month precision)
d:"d"$ts      /convert timestamp to date type (day precision)
u:"u"$ts      /convert timestamp to minute precision (no date, precision rounded to hh:mm)
v:"v"$ts      /convert timestamp to second precision (no date, precision rounded to hh:mm:ss)
t:"t"$ts      /convert timestamp to millisecond precision (no date, precision rounded to hh:mm:ss.000)
n:.z.P - ts   /calculate different between two timestamps (hh:mm:ss.000000000)
.z.Z - ts     /generates an error because we are doing datetime - timestamp
```

More information can be found [here](http://code.kx.com/wiki/Reference/Datatypes)


## Lists
Lists are a collection of values (either atoms or other data structures).  Lists are generally created using `(...)`, but single-valued lists can also be created using `enlist`, e.g.:
```
jlst:(1;2;3;4)        /integer list
olst:(1;"a";`a`b!1 2) /untyped list
slst:enlist 1         /typed list with a single item
slst~1                /0b - single item list is not same as an atom
```

Accessing elements in lists is very similar to other languages, and there are some additional helper functions to get the first and last elements:
```
lst:til 10
lst[0]      /returns the 1st element
lst[4]      /returns the 5th element
lst[12]     /returns 0N (null) - kdb will return a null if the index is out of bounds instead of an error
lst 0       /returns the 1st element (brackets are optional)
first lst   /returns the 1st element
last lst    /returns the last element
lst[1]:12   /assigns 12 to 2nd element - kdb will generate 'length error if the index is out of bounds
```

List operators are just as easy (some common examples):
```
count lst     /gets length of lst
reverse lst   /reverse a list
asc lst       /sort a list ascending
desc lst      /sort a list descending
2 cut lst     /cuts list every 2 elements, returns list of lists
2_lst         /drop first 2 items from list
2#lst         /takes first 2 items from the list
lst _2        /drops the 3rd item from the list
```

There's two type of lists, typed and untyped.  If all members of a list are the same type, the list will be typed, which allows certain efficiencies in terms of calcuations.  At the very least, a typed list needs to be type checked only once, while an untyped list will need a type check for every element.  There are also calculation efficiencies associated with numeric lists, as well as cache advantages.

Lists are the fundamental data structure in kdb (the structures below are composed of lists) and most functions will work on both atoms and lists.  In general most functions will work on atom vs list or equal length lists, e.g.:
```
lst1:10?10
lst2:10?10
lst1 - lst2 /subtracts lst2 from lst1
10 + lst2   /adds 10 to every item of the list
lst2 > 4    /checks every element to see if it's greater than 4
```


## Dictionaries
Like other languages, kdb dictionaries map keys to values.  Unlike most other languages however, kdb uses two lists of the same size, one for keys and one for values.  All the rules of lists (typed/untyped) apply to keys and values in a dictionary, which allows for the following:
```
d1:`a`b!1 2                     /standard way of creating a dictionary using ! and using symbols as keys
d2:1 2!`a`b                     /using integer as keys
d3:`a`b!("hello world";.z.P)    /values can be untyped lists
d4:("hello world";`a)!1 2       /keys can also be untyped lists
lst2:lst1:til 10
lst1!lst2                       /use preassigned lists to generate a dictionary
```

Accessing elements of a dictionary is very similar to lists.  In addition, dictionaries have `key` and `value` functions to extract the key and value lists:
```
d1:(-10?`3)!til 10  /randomly generate a 3-letter key, and assign values to it
d1 `nhk             /access key `nhk (will return a null if `nhk doesn't exist)
d1[`nhk]:12         /assigns 12 to the value of `nhk - if `nhk doesn't exist this will be added to the dictionary
first d1            /returns first value
first key d1        /returns first key
reverse d1          /reverse both key and value
2_d1                /drops first two key/value pairs
2#d1                /takes first two key/value pairs
```


## Tables
Tables are dictionaries that have the following set of rules:
- values are lists of the same length
- keys are symbols

There are three ways of create a dictionary, either by using `flip` on a dictionary that follows the above rules, creating a table using the table syntax, or using `enlist` on a dictionary where keys are symbols and values are a list of atoms
```
d1:`a`b!(1 2;3 4)
t1:flip d1            /create a table by flipping a dictionary
t2:([]a:1 2;b:3 4)    /create a table with table initialization syntax
t1 ~ t2               /1b
enlist `a`b!1 2
```

Once we have a table, we can access data either by row or by column.  We can access rows by index number, and columns by the column name, i.e.
```
t1 `a           /returns column a as a list
t1 0            /returns the first row as a dictionary
t1[0;`a]        /returns the first item of column a as an atom
t1[0 1;`a]      /returns the first two items of column a as a list
t1[0 1;`a`b]    /returns the values of the table as a list of list (i.e. a matrix)
(enlist `a)#t1  /returns a table that's only column a
```

Finally we can access the column names using `cols`.


## Keyed tables
A keyed table is a dictionary where the key is a table of the key columns and the value is a table of the value columns.  They are especially useful for join operations.

All the rules above apply, but there's a few other ways to create a keyed table:
```
t1:flip`a`b`c!(-10?10;10?10;10?10)    /create a regular table
kt1:`a xkey t1                        /convert a regular table to a keyed table with `a being the key
kt2:1!t1                              /convert a regular table to a keyed table with the first column as the key
kt3:((enlist`a)#t1)!`b`c#t1           /create a keyed table from two tables
```
