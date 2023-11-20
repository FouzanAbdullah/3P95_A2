# 3P95_A2

In order to run the code, open the Assign2 folder as a project in the IDE of your choice. Ensure all packages are installed on your system.

For Question 1:
Run server_side.py, then once all files have been generated, run client_side.py.

For Question 2:
Run delayed_server.py, then once all files have been generated, run client_side.py.
The parameters that can be changed within the delayed_server.py is the probabilty_sampling variable. 0.4 represents a probability of 40%, 1.00 represents 100%, and so on. 

To run Prometheus, ensure prometheus is installed properly on your system and run it using the command "prometheus --config.file=prometheus.yml" Once this is done, run the server_side.py, and client_side.py or delayed_server.py for question 2, and open localhost:9090 for viewing the graph with the different queries.
