## Execution of the code

1. Here are the commands from the directory assignment-1-767835/code/mongo-database-1/. to execute the code:

docker-compose build
docker-compose up

2. In order to ingest data:

wget -qO- http://localhost:3010/ingest/<batch_no>

where <batch_no> is a number corresponding to the index of the data file to use. It must be between 1 and 9. The data files used are in assignment-1-767835/code/mongo-database-1/ingest/data/. .

3. The file assignment-1-767835/code/mongo-database-1/script-testing.sh provides a bash script to perform 50 simultaneous client requests
To execute it:

bash script-testing.sh
