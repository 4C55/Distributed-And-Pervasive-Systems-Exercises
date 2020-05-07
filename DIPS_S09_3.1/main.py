from multiprocessing import Process, Pipe
from datetime import datetime
from random import random
import time
import itertools

NODES = [1, 2, 3, 4, 5]
DEAD_NODES = [3, 5]
NODE_STARTING_ELECTION = 1

ELECTION_TIMEOUT_S = 3
MAX_ID = max(NODES)


class PairNode:
    def __init__(
            self,
            owner_id,
            pair_id,
            pipe):

        self.owner_id = owner_id
        self.pair_id = pair_id
        self.pipe = pipe

    def has_message(self):
        time.sleep(random()/10)
        return self.pipe.poll()

    def receive_message(self):
        time.sleep(random()/10)
        message = self.pipe.recv()
        print('Node %d received ''%s'' message from %d' % (self.owner_id, message, self.pair_id), end='\n', flush=True)
        return message

    def send_message(self, message):
        time.sleep(random()/10)
        print('Node %d sent ''%s'' message to %d' % (self.owner_id, message, self.pair_id), end='\n', flush=True)
        self.pipe.send(message)


def node_process_start_election(id, channels):
    run_election_again = False

    if id == MAX_ID:
        # This node has the highest id
        for channel in channels:
            channel.send_message('Victory')

        # This node won the election - done
        run_election_again = False
        return run_election_again
    else:
        # Broadcast election request to all nodes with higher ids
        for channel in [c for c in channels if c.pair_id > id]:
            channel.send_message('Election')

        # Wait for incoming messages
        start = datetime.now()
        while (datetime.now() - start).total_seconds() < ELECTION_TIMEOUT_S:
            for channel in channels:
                if channel.has_message():
                    message = channel.receive_message()

                    if channel.pair_id > id:
                        # Received a reply from a node with higher id - this node is not the leader. Done
                        run_election_again = False
                        return run_election_again
                    elif message == 'Election' and channel.pair_id < id:
                        # Received an election message from a node with lower id - send a reply and continue with the
                        # election
                        channel.send_message('ElectionReply')
                    elif message == 'Victory':
                        # Received a victory message - follow that node
                        print('Node %d follows node %d' % (id, channel.pair_id))
                        run_election_again = False
                        return run_election_again

        # Timed out, meaning no reply was received
        for channel in channels:
            channel.send_message('Victory')

        run_election_again = False
        return run_election_again


def node_process_wait_and_listed(id, channels):
    while True:
        for channel in channels:
            if channel.has_message():
                message = channel.receive_message()
                if message == 'Victory':
                    print('Node %d follows node %d' % (id, channel.pair_id))
                if message == 'Election' and channel.pair_id < id:
                    # Received an election message from a node with lower id - send reply and restart election
                    channel.send_message('ElectionReply')
                    return True


def node_process(id, channels, start_election, dead):
    while True and not dead:
        if start_election:
            start_election = node_process_start_election(id, channels)
        else:
            start_election = node_process_wait_and_listed(id, channels)
    print('Node %d died' % (id, ), end='\n', flush=True)


if __name__ == '__main__':
    # Prepare node ids and their combinations
    node_pairs = list(itertools.combinations(NODES, 2))

    # For each combination, create a channel
    channel_pairs = []
    for pair in node_pairs:
        end_1, end_2 = Pipe()
        channel_pairs.append({'Node1': pair[0], 'Node1End': end_1, 'Node2': pair[1], 'Node2End': end_2})

    # Get a list of nodes together with all the pair channels associated with the node
    nodes = []
    for node_id in NODES:
        channels = []
        for channel_pair in channel_pairs:
            if channel_pair['Node1'] == node_id:
                channels.append(PairNode(
                    owner_id=node_id,
                    pair_id=channel_pair['Node2'],
                    pipe=channel_pair['Node1End']))
            elif channel_pair['Node2'] == node_id:
                channels.append(PairNode(
                    owner_id=node_id,
                    pair_id=channel_pair['Node1'],
                    pipe=channel_pair['Node2End']))
        nodes.append({'Id': node_id, 'Channels': channels})

    # Create processes passing as argument the node id and associated channels
    processes = []
    for node in nodes:
        processes.append(
            Process(
                target=node_process,
                args=(node['Id'], node['Channels'], node['Id'] == NODE_STARTING_ELECTION, node['Id'] in DEAD_NODES)
            ))

    for process in processes:
        process.start()

    for process in processes:
        process.join()