### Assignment report


## Part 1

# Question 1

1. *mysimbdp_coredms* contains the database. It provides an API to manipulate the database. *mysimbdp-dataingest* uses this API to send data to be inserted in the database
2. *mysimbdp_daas* communicates with *mysimbdp_coredms* to execute the orders of the client

# Question 2

We use MongoDB as a database technology. In its minimal configuration, *mysimbdp_coredms* requires 2 nodes: one for MongoDB, and one for the API. However, in order to obtain better performances, we will duplicate the API so that one is dedicated to *mysimbdp_dataingest*, and the other to *mysimbdp_daas*.

*mysimbdp_coredms* will run on three nodes.

# Question 3

We use containers for mysimbdp. It allows better performances than VMs by using less resources. In addition, it is easily scalable, and the containers can be integrated continuously in a cluster.

# Question 4

I would increase the number of instances of *mysimbdp_coredms* running. It means:
1. create shards, so that parallel writings can happen. Each shard contains only the data selected according to one criteria
2. We would create multiple APIs within *mysimbdp_coredms*: each one would be able to manipulate data in all shards. This way, the communication of data could happen faster by writing simultaneously in the different shards.
3. I would run several instances of *mysimbdp_dataingest*. Each client would be associated with a different instance. When an instance of *mysimbdp_dataingest* would start communicating with *mysimbdp_coredms*, it wuld first ask a service of *mysimbdp_coredms* which API is least busy, and connect with it. This implies adding ane more container to *mysimbdp_coredms* for this service.

# Question 5

We choose Google Cloud Services as a cloud provider because:
1. We work with the water quality database. Therefore, the ingestion of new data i very regular and limited. The most important use will be to read the data, so that it is always available. Google Cloud Services offer low prices adapted to a low use of this resource in writing.
2. We can run Docker containers with NoSQL databases (which is used by MongDB).
3. We have access to Kubernetes


## Part 2

# Question 1

We will create 3 shards in order to have enough flexibility. Each shard will take care of the requests associated to one geographical area. A shard has 2 nodes; one for MongoDB, another for the API allowing access to the data. The 3 databases contain different elements. In addition, there is another node running, which takes care of the disribution of the clients to each shard (it is the distributor node). A writing operation is performed in a single shard, whereas a reading operation requires the intervention of all 3 shards.

Inserting image

# Question 2

The data is partitioned geographically: it takes into account that most reading requests will be based on geographical criterias.

# Question 3

We perform this with 3 shards, and 1 to 50 clients requesting to ingest data. Each request asks to ingest 10000 entries in the atabase.

# Question 4

The result shows:
1. on a local machine, each request takes 2 to 3 seconds to be validated
2. the 3 shards work in parallel thanks to the service distributing the requests between the shards. So that there are 3 requests being answered at the same time: the performance is therefore tripled
3. on a local machine, all requests are satisfied. This has been tested for 1 to 50 simultaneus requests.

# Question 5

Because all requests ingest the same amount of data, the distribution of the tasks to each hard is easy. Clients with requests of different sizes would require a better distribution of the tasks between the shards.

We would be likely to face failures if we were on a real network. The test is on a local machine, so there is no loss or damaging of packets.

On a real network, we would have to find the optimal amount of data to send over one request (balance between head overload and failure risk) and choose it as amount of data to send in one request. In addition, we should save each data in 2 diifferent tables for consistency validation.

The main time-consuming task is to insert data into the database (and not to read the csv files). To speed up this process, we should have in each shard several threads inserting the data concurrently, and a main thread reading the data from the packets and transfrring it to the threads.

## Part 3

# Question 1
