import multiprocessing
import os
import time

def search_keywords_in_file(filename, keywords, result_queue):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            local_result = {}
            for keyword in keywords:
                if keyword in content:
                    if keyword not in local_result:
                        local_result[keyword] = []
                    local_result[keyword].append(filename)
            if local_result:
                result_queue.put(local_result)
    except Exception as e:
        print(f"Error reading {filename}: {e}")

def process_worker(files, keywords, result_queue):
    for file in files:
        search_keywords_in_file(file, keywords, result_queue)

def main_multiprocessing(files, keywords):
    processes = []
    result_queue = multiprocessing.Queue()
    num_processes = 4
    files_per_process = len(files) // num_processes

    start_time = time.time()

    for i in range(num_processes):
        start_index = i * files_per_process
        end_index = None if i == num_processes - 1 else (i + 1) * files_per_process
        process_files = files[start_index:end_index]
        process = multiprocessing.Process(target=process_worker, args=(process_files, keywords, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    print(f"Multiprocessing approach took {end_time - start_time:.2f} seconds")

    results = {}
    while not result_queue.empty():
        result = result_queue.get()
        for keyword, files in result.items():
            if keyword not in results:
                results[keyword] = []
            results[keyword].extend(files)

    return results

if __name__ == "__main__":
    files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt"]
    keywords = ["keyword1", "keyword2"]
    results = main_multiprocessing(files, keywords)
    print(results)
