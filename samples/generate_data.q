/function to generate uniform
runif:{-.5 + x?1.}
weekday:{x where 1 < x mod 7}

/generate bid and ask quotes
gen_quotes:{[ticker;start_price;date;start_time;end_time;n]
 ts:date + start_time + "n"$("n"$end_time-start_time) * {x%last x}(+\)n?1.;
 bid:start_price + (+\)runif n;
 ask:bid + n?1.;
 flip `ticker`date`ts`bid`ask!(ticker;date;ts;bid;ask)
 }

/generate quotes for a day
/tbl:gen_quotes[`AAPL;100;2016.08.05;09:30;16:00;1000]

/generate quotes for multiple days (issue - start of day price is always 100)
/tbl:raze gen_quotes[`AAPL;100;;09:30;16:00;1000] each 15#weekday 2016.08.01 + til 21

/generate quotes for multiple days, seeding the first price of the day with the last bid of previous day
tbl:raze 1_{p:$[0 > type x;x;last[x]`bid];gen_quotes[`AAPL;p;y;09:30;16:00;1000]}\[100;15#weekday 2016.08.01 + til 21]

