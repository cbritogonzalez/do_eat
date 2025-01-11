import schedule
import time
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_trigger_task():
    try:
        logger.info("Running task.py...")
        subprocess.run(['python', 'task.py'], check=True)
        logger.info("Successfully ran task.py.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running task.py: {e}")

# schedule.every().sunday.at("06:00").do(run_trigger_task)
schedule.every(10).minutes.do(run_trigger_task)

def run_scheduler():
    logger.info("Scheduler is running...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
