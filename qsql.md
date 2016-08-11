# Q-SQL

One of the main reasons kdb works so well as a database language is because it has its own version of sql (qsql).  The basic syntax and logic is very similar to general sql, however there are some differences that make kdb sql more compact and efficient

## Select
`select` statements are used to query for data from a particular table.  They are composed of four components:
- the table to select on
- the aggregate clause (either which columns to take, or any aggregations to be done on the columns)
- the groupby clause (which columns to group on, and any logic to group them)
- the constraint clause (what are the constraints to filter rows on)

Some examples:
```
tbl:([]sym:1000?`aapl`twtr`fb;side:1000?`bid`ask;val:1000?1.)                 /generate a table
select from tbl                                                               /select all items from the table
select from tbl where sym=`aapl                                               /select aapl only
select from tbl where sym in `aapl`fb                                         /select aapl and fb
select sym, val from tbl                                                      /select sym and val columns only
select sym, val from tbl where sym=`twtr, side=`bid, val>0.5                  /multiple constraints
select by sym from tbl                                                        /gets last row for each sym
select agg_val:sum val by sym from tbl                                        /sums vals for each sym
select agg_val:sum val by ?[sym in `aapl`fb;`large_cap;`small_cap] from tbl   /custom logic in groupby clause
select distinct sym from tbl                                                  /distinct syms
```

The above is great for adhoc querying, however it's not very conducive when used in functions, as it's essentially string parsing.  kdb also has a second form for querying, called "functional select", that looks like `?[table;constraint;groupby;aggregates]`.  The above examples in functional form are below:
```
?[tbl;();0b;()]                                                                       /select all items from the table
?[tbl;enlist (=;`sym;enlist`aapl);0b;()]                                              /select aapl only
?[tbl;enlist (in;`sym;enlist`aapl`fb);0b;()]                                          /select aapl and fb
?[tbl;();0b;`sym`val!`sym`val]                                                        /select sym and val columns only
?[tbl;((=;`sym;enlist`twtr);(=;`side;enlist`bid);(>;`val;0.5));0b;`sym`val!`sym`val]  /multiple constraints
?[tbl;();(enlist`sym)!enlist`sym;()]                                                  /gets last row for each sym
?[tbl;();(enlist`sym)!enlist`sym;(enlist`agg_val)!enlist(sum;`val)]                   /sums vals for each sym
?[tbl;();
  (enlist`x)!enlist(?;(in;`sym;enlist`aapl`fb);enlist`large_cap;enlist`small_cap);
  (enlist`agg_val)!enlist(sum;`val)]                                                  /custom logic in groupby clause
?[tbl;();1b;(enlist`sym)!enlist`sym]                                                  /distinct syms
```


## Update
Update behave very similarly to `select`, and all the above rules apply:
```
update new_col:1 from tbl               /adds a new column
update val:0 from tbl where sym=`twtr   /error - we cannot update a float column with an integer
update val:0. from tbl where sym=`twtr  /all rows with twtr now set to zero
update mean:avg val by sym from tbl     /creates a new column called mean with the average values by sym
```

Also as above, there is a functional version of update:
```
![tbl;();0b;(enlist`new_col)!enlist 1]                              /adds a new column
![tbl;enlist(=;`sym;enlist`twtr);0b;(enlist`val)!enlist 0]          /error - we cannot update a float column with an integer
![tbl;enlist(=;`sym;enlist`twtr);0b;(enlist`val)!enlist 0.]         /all rows with twtr now set to zero
![tbl;();(enlist`sym)!enlist`sym;(enlist`mean)!enlist (avg;`val)]   /creates a new column called mean with the average values by sym
```


## Insert/upsert
kdb has multiple ways to insert new rows into a table, and they depend on use cases.  Some methods are robust while others are much more performant.

`insert`
: insert will only insert into global tables and is the most standard way of updating tables.  `insert` requires that the data inserted needs to match the table (e.g. if it's a list, the order and type of the data needs to be correct, or if it's a dictionary or table the column names must match exactly).

In addition, on a keyed table, insert will not replace existing rows, but instead will throw an error.
```
`tbl insert (`fb;`ask;0.4)                                                      /this will insert a row
`tbl insert (`fb`twtr;`ask`bid;0.4 0.2)                                         /this will insert two more rows
`tbl insert `val`sym`side!(0.8;`aapl;`ask)                                      /this will also insert a row
`tbl insert ([]side:enlist `buy;sym:enlist `twtr;val:enlist 2.)                 /this will also insert a row
`tbl insert ([]side:enlist `buy;sym:enlist `twtr;val:enlist 2.;val2:enlist 1.)  /the insert has a new column, and will error
```

`upsert`
: blah blah

`,`
: blah blah


## Joins
For most data operations, joins are as important as the ability to query.  kdb provides the standard join logic (inner join, outer join, left join) along with some more advanced logic for online updates (plus join) and time-based joins (asof join, window join).

`uj`
: union join does an outer join on two tables if the tables are unkeyed, otherwise if the tables are keyed it does a left join on keys present in the left table and appends all missing keys.  For uj to work both tables need to be either keyed or unkeyed.
```
tbl1:([]sym:10#`aapl`twtr;ts:10#2000.01.01 + 2 * til 5;val1:10?100;val2:10?100)
tbl2:([]sym:20#`aapl;ts:2000.01.01+til 20;val2:300)
uj[tbl1;tbl2]         /joins two tables together (essentially a row bind)
tbl1 uj tbl2          /same as above, a more natural way of expressing joins
uj[2!tbl1;2!tbl2]     /joins two keyed tables together (left join on existing key items, append on all others)
```

`lj`
: left join will take join on the keys of the right table.  The returned table will have the same type as the left table (keyed if the left table is keyed, unkeyed if it's not), and will always have the same number of rows as the left table.
```
lj[tbl1;2!tbl2]   /replaces values in table1 with values in table2 that match table2 keys
tbl1 lj 2!tbl2    /same as above, more natural way to express joins
```

`ij`
: standard inner join, will only return rows where keys of the right table match rows in the left table.  The returned table will have the same type as the left table.
```
ij[tbl1;2!tbl2] /will only return joined rows that are in both tbl1 and tbl2
```

`pj`
: plus join is a join specifically for numeric tables.  The join operation is similar to a left join, however instead of replacing elements in the left table with the right table, it will add to the left table values.  This is especially useful when the right table is some online update (e.g. a counter), while the left table stores the running totals.
```
pj[tbl1;2!tbl2]
```

`aj`
: asof join is a left join that joins the last observed value from the right table, based on columns defined in the first argument.  It's very useful for joining quote and trade tables, where you want to see the last market quote associated with the trade.
```
aj[`sym`ts;tbl2;tbl1]
```

`wj`
: window join is a more generalized, complex version of an asof join.  The join will take a set of window ranges that's the same size as the left table, and execute any aggregations on the right table, e.g.
```
wj[(tbl1.ts;tbl1.ts+til count tbl1);`sym`ts;tbl1;(tbl2;(sum;`val2))]  /gets the window of dates around tb1 rows, and sums them
```


