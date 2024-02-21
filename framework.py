from sys import stderr, stdin
import os
import argparse
import multiprocessing as mp
from loader.encoder import XMLEncoder
from active_learning_model.framework import AL_Workflow

    
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
    model = AL_Workflow()

    #TODO: fill in exit condition
    exit_condition = True

    # Put data into the queue
    for item in data:
        multiprocessing_queue.put(item)

    while exit_condition == False:
        abm_outputs = evaluate(multiprocessing_queue,multiprocessing_queue_out )

    #TODO: implement active learning function
    params_to_evaluate.add(AL_Workflow.al_algorithm(abm_outputs))

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
        decoded_output = XMLEncoder.decode(multiprocessing_queue_out.get())
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
    return NotImplementedError

if __name__ == '__main__':
    main()
    