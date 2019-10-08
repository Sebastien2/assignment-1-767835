## Design of the code

Here are the containers present in the code:
- containers A: 3 containers in *coredms*, each one working on a different table of a same database. Each one can write and read data.
- container B: 1 container in *coredms* to provide a client request / ingest request to one of the 3 containers managing the database. For simplicity, alternates between each of the three container to balance their load.
- container C: 1 container in *ingest* to provide an API allowing the ingestion of data from a file
- container D: 1 container with a mongoDB instance

## Communication of the containers

A client sends a request for ingestion through container C API. C communicates with B to know which container it should send the data. C obtains the container's name, and sends the data to the corresponding container A.

## Test results

We perform testing by ingesting data as packets of 10000 entries at a time. There is also the psossibility of injecting one data at a time in the *coredms* containers. We obtain a performance of between 2 and 3 seconds for 10000 entries. Considering that we have 3 shards, 3 ingestions can be performed in parallel.

The tests are performed on local machine, so that there is no packet loss, and no delay from the network. 
