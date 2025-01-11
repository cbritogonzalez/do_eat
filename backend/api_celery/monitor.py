# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# import subprocess
# import os


# class JSONFileHandler(FileSystemEventHandler):
#     def __init__(self, queue_name):
#         self.queue_name = queue_name

#     def on_created(self, event):
#         if event.is_directory:
#             return

#         # Check if the created file is a JSON file
#         if event.src_path.endswith(".json"):
#             print(f"New JSON file detected: {event.src_path}")
#             subprocess.run(["python", "send.py"], check=True)


# if __name__ == "__main__":
#     path_to_watch = "api_celery/data"
#     queue_name = "json_files"

#     event_handler = JSONFileHandler(queue_name=queue_name)
#     observer = Observer()
#     observer.schedule(event_handler, path=path_to_watch, recursive=False)
#     print(' [*] Monitoring started. To exit press CTRL+C')
#     observer.start()

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()

import subprocess
import os
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".json"):
            print(f"New JSON file detected: {event.src_path}")
            # Get the directory of this script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            send_script_path = os.path.join(current_dir, "send.py")
            
            # Call send.py with the correct path
            subprocess.run(["python", send_script_path], check=True)

if __name__ == "__main__":
    folder_to_watch = "/data"
    event_handler = Watcher()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    print(' [*] Monitoring started. To exit press CTRL+C')
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
