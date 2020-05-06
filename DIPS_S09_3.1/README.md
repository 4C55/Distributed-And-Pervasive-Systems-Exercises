# Prototype

##Task:
Implement the Bully algorithm in Python and document it works.
##Solution:
Implementation is available in **main.py**. Implementation has 3 configurable parameters:
1. NODES - array containing the ids of the nodes to be simulated.
2. DEAD_NODES - ids of the nodes that will not communicate to other nodes.
3. NODE_STARTING_ELECTION - id of the node that will start the election.

These parameters can be modified to simulate different scenarios.

**BestCase.png** shows a scenario where system contains nodes [1, 2, 3, 4, 5], nodes [3, 5] are non responsive and node
4 starts the election. This is the simplest case and requires the least amount of messages. At the end, node 4 wins the election.

**WorstCase.png** shows a scenario where system contains nodes [1, 2, 3, 4, 5], nodes [3, 5] are non responsive and node
1 starts the election. This is the worst case and requires the most amount of messages. At the end, node 4 wins the election.