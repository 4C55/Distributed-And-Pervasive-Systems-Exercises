from multiprocessing import Process, Pipe
import time as tm

NUMBER_OF_DEVICES = 2

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