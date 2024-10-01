import schedule
import time
from backup import backup_files

def run_backup():
    print("Starting backup process...")
    backup_files()

schedule.every().day.at("02:00").do(run_backup)  # Schedule to run at 2 AM every day

def start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait 1 minute between checks
