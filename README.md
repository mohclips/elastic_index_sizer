# ElasticSearch Daily Index size

A docker image to work out the daily size of each index

# Summary

I could never find a decent way to forecast the index sizes.  In the Kibana GUI you can see the total index size
which you need to divide by the number of nodes that the data is stored on, and that gives you an idea, buy you can't visualise it.

So, to get some sort of rough average, the following is done.

- Pick an index
- Work out the average size of a document in that index
- Count the number of documents in the previous day
- daily index size = (number of docs that day) x (average doc size)

It's not 100% but it's going to allow you to see the index sizes and forecast some trends.

# Code

The is all based on a few lines of Python.

You will need to run the code/docker image once a day.


# Kibana

By saving the results back to an index, you can then use kibana to visualise the data.






