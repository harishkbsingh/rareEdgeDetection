# Rare Edge Detection Algorithm

## Next steps Implementation:

1. The current parameters are the source, the destination, and the the starting time and ending time. However, the should be only starting and ending time (e.g. one hour range), that way we can collect more data by analyzing all edges of within an hour. 
2. In the present, the values (i.e. stats) are not persisted in the database.
3. The algo uses the standard deviation the previous week to analyze the current expected entry. For this reason, we need to store the values those entries. However, not sure if there is a better way, TBD.  
4. Code refactoring needed.
