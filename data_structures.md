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
first lst   /returns the 1st element
last lst    /returns the last element
```

List length is just as easy:
```
count lst   /gets length of lst
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

## Tables

## Keyed tables
