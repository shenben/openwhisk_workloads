import requests
import schedule
import time
import threading

# def crawl():
#   # Make a request to a website
#   response = requests.get('http://www.example.com')
#   # Do something with the response
#   print(response.text)

# # Schedule the crawl function to run every microsecond
# schedule.every(0.000001).seconds.do(crawl)

# # Create a list to store all of the threads
# threads = []

# # Create 10 threads
# for i in range(10):
#   # Create a new thread
#   thread = threading.Thread(target=crawl)
#   # Add the thread to the list
#   threads.append(thread)
#   # Start the thread
#   thread.start()



import requests
import threading
import time

# List of crawl targets
targets = ['http://www.example1.com', 'http://www.example2.com', 'http://www.example3.com',
           'http://www.example4.com', 'http://www.example5.com', 'http://www.example6.com',
           'http://www.example7.com', 'http://www.example8.com', 'http://www.example9.com',
           'http://www.example10.com']
def invoke(url = 'http://172.17.0.1:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/wsk_exp/base64'):
    # Set the headers
    headers = {'Content-Type': 'application/json'}
    # Set the payload
    payload = {"str1":"b1WM0Vx8Fegr2tu6jAmPJZ9aRcG4TEpYNyvfz5Q7DoqBUS3CHl","str2":"SwDLqvpr","TRIES":100 }
    response = requests.get(url, json=payload, headers=headers)
    # import json
    # json_data = json.dumps(payload)
    # response = requests.get(url, data=json_data, headers=headers)
    # Print the response
    print(response.text)

def crawl(target):
  # Make a request to a website
  response = requests.get(target)
  # Do something with the response
  print(response.text)

# # Create a new thread for each crawl target
# threads = []
# for target in targets:
#   thread = threading.Thread(target=crawl, args=(target,))
#   thread.start()
#   threads.append(thread)

# # Wait for all threads to finish
# for thread in threads:
#   thread.join()

# print("All threads have finished.")

# def run_schedule():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# def run_crawler_schedule():
#     channel_crawler(priority=1)
#     schedule.every(PRIORITY[1]["interval"]).minutes.do(channel_crawler, priority=1)
#     run_schedule(schedule)

# def run_fix():
#     schedule.every().day.at("17:30").do(distance_fixer)
#     run_schedule()


# def run_job()
#     p = Process(target=run_crawler_schedule)
#     c = Process(target=run_fix)
#     p.start()
#     c.start()
#     p.join()
#     c.join()

if __name__ == "__main__":

#     while True:
#   # Run the scheduled tasks
#         schedule.run_pending()
# #   time.sleep(1)
    invoke()