# Table types

One major use of kdb is as a database, and there are five types of tables that suit different different use cases.  The details mostly have to do with persistence, and from an access/usage standpoint there is very little differences (i.e. the user does not need to be aware of the underlying structure).

## In-memory table
This is the simplest table, and can be created on the fly.  The table itself is fully in memory and will be lost if the process exists.
```
tbl:([]sym:10#`aapl`twtr;ts:10#2000.01.01 + 2 * til 5;val1:10?100;val2:10?100)
```


## Single-file table
Stores the table as a single binary file on disk.  This is particularly useful for small tables and for quickly saving data sets.  The usual way to save a single-file table is to use `set`, with the left hand argument as a file path
```
(`$":/tmp/on_disk_table") set tbl
\l /tmp/on_disk_table
```


## Splayed table
Stores the table as columns on disk (i.e. each column is its own file).  The main advantage of a splayed table over a single-file table is that only queried columns are stored in memory, making the querying and loading process a lot more efficient.  This is useful for medium-sized tables with a lot of columns.
```
(`$":/tmp/splayed_table/tbl") set .Q.en[`$":/tmp/splayed_table/";tbl]
\l /tmp/splayed_table
```


## Partitioned table
Takes the splayed-column concept further, and also allows for partitioning.  The most common use case here is storing historical quote and trade data - by partitioning the data physically across dates.  The partition index can be anything that resolves to an integer value.
```
.Q.dpft[`$":/tmp/partitioned_table";2016.08.02;`sym;`tbl]
```


## Segmented table
Segmented tables take the concept of partitioned tables one step further, and allows you to distribute your data set across machines.  We won't go over this in detail, more detail can be found [here](http://code.kx.com/wiki/JB:KdbplusForMortals/segments#1.4.1_Segmented_Tables).
