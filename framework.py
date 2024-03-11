from sys import stderr, stdin
import os
import argparse
import multiprocessing as mp
from loader.encoder import XMLEncoder
from active_learning_model import EMEWS_active_learning_sampling

    
def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--input", metavar="xml", default="input.xml",
        help="The 25 random parameter samples")
    
    args = parser.parse_args()

    #TODO: Define 25 randomly generated param sets
    data = XMLEncoder.encode(args.input)
    multiprocessing_queue = mp.JoinableQueue()
    multiprocessing_queue_out = mp.Queue()
    abm_outputs = []
    params_to_evaluate = data

    #TODO: replace with actual parameters
    max_iter = 100
    obj_function = False
    coo_metric = False


    #TODO: fill in exit condition
    exit_condition = True

    # Put data into the queue
    for item in data:
        multiprocessing_queue.put(item)

    while exit_condition == False:
        abm_outputs = evaluate(multiprocessing_queue,multiprocessing_queue_out)

    model = EMEWS_active_learning_sampling(abm_outputs, obj_function, max_iter, coo_metric)
    params_to_evaluate.add(model.query(abm_outputs, 20))

def evaluate(multiprocessing_queue, multiprocessing_queue_out):
    abm_outputs = []
    # Create and start worker processes
    num_processes = mp.cpu_count()  # Use the number of available CPU cores
    processes = []
    for _ in range(num_processes):
        process = mp.Process(target=worker, args=(multiprocessing_queue,))
        processes.append(process)
        process.start()

    # Wait for all items in the queue to be processed
    multiprocessing_queue.join()

    # Terminate worker processes
    for process in processes:
        process.terminate()
    
    # Retrieve and print the processed results from the output queue
    while not multiprocessing_queue_out.empty():
        decoded_output = multiprocessing_queue_out.get()
        abm_outputs.add(decoded_output)
    
    return abm_outputs

def worker(queue, queue_out ):
    # Define the worker function that retrieves items from the queue and processes them
    while True:
        try:
            item = queue.get_nowait()  # Get an item from the queue
            result = process_queue_item(item)   # Process the item
            queue_out.put(result)  # Put the processed result into the output queue
            queue.task_done()          # Mark the item as processed
        except queue.Empty:
            break

### TODO: replace this with calling abm
def process_queue_item(item):
    XMLEncoder.encode(item)
    #abm_outputs = XMLEncoder.decode(abm_call)
    return NotImplementedError

if __name__ == '__main__':
    main()
    