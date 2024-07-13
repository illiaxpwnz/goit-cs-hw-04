import threading
import os
import time

def search_keywords_in_file(filename, keywords, result):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    if keyword not in result:
                        result[keyword] = []
                    result[keyword].append(filename)
    except Exception as e:
        print(f"Error reading {filename}: {e}")

def thread_worker(files, keywords, result):
    for file in files:
        search_keywords_in_file(file, keywords, result)

def main_threading(files, keywords):
    threads = []
    results = {}
    num_threads = 4
    files_per_thread = len(files) // num_threads

    start_time = time.time()

    for i in range(num_threads):
        start_index = i * files_per_thread
        end_index = None if i == num_threads - 1 else (i + 1) * files_per_thread
        thread_files = files[start_index:end_index]
        thread = threading.Thread(target=thread_worker, args=(thread_files, keywords, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Threading approach took {end_time - start_time:.2f} seconds")

    return results

if __name__ == "__main__":
    files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt"] 
    keywords = ["keyword1", "keyword2"]
    results = main_threading(files, keywords)
    print(results)
