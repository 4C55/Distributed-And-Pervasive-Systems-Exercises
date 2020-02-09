from multiprocessing import Process, Pipe
import time as tm


LAMPORT = True


def calculate_time_on_receive_event(received_time, local_time):
    if LAMPORT:
        return max(received_time, local_time) + 1
    else:
        return local_time + 1


def event(process_id, time):
    tm.sleep(0.5)
    time = time + 1
    print('Event in {} at {}'.format(process_id, time))
    return time


def send_message(pipe, process_id, time):
    tm.sleep(0.5)
    time += 1
    pipe.send(('Empty shell', time))
    print('Message sent from {} at time {}'.format(process_id, time))
    return time


def recv_message(pipe, process_id, time):
    tm.sleep(0.5)
    message, received_time = pipe.recv()
    time = calculate_time_on_receive_event(received_time, time)
    print('Message received at {} at time {}'.format(process_id, time))
    return time


def process_1_action(pipe_1_3, pipe_1_2):
    tm.sleep(0.5)
    process_id = 1
    time = 0
    time = event(process_id, time)
    time = event(process_id, time)
    time = recv_message(pipe_1_3, process_id, time)
    time = recv_message(pipe_1_2, process_id, time)
    time = send_message(pipe_1_2, process_id, time)
    time = send_message(pipe_1_3, process_id, time)


def process_2_action(pipe_2_1):
    tm.sleep(0.5)
    process_id = 2
    time = 0
    time = send_message(pipe_2_1, process_id, time)
    time = recv_message(pipe_2_1, process_id, time)
    time = event(process_id, time)


def process_3_action(pipe_3_1):
    tm.sleep(0.5)
    process_id = 3
    time = 0
    time = send_message(pipe_3_1, process_id, time)
    time = recv_message(pipe_3_1, process_id, time)


if __name__ == '__main__':
    pipe_1_2, pipe_2_1 = Pipe()
    pipe_1_3, pipe_3_1 = Pipe()

    process_1 = Process(target=process_1_action, args=(pipe_1_3, pipe_1_2,))
    process_2 = Process(target=process_2_action, args=(pipe_2_1,))
    process_3 = Process(target=process_3_action, args=(pipe_3_1,))

    process_1.start()
    process_2.start()
    process_3.start()

    process_1.join()
    process_2.join()
    process_3.join()