from app import celery_app
from tasks import fetch_albert_heijn_data, fetch_jumbo_data

if __name__ == "__main__":
    celery_app.worker_main(argv=['worker', '--pool=solo', '--loglevel=info'])
