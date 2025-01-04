# from celery import Celery

# BROKER_URL = 'pyamqp://guest@localhost//'
# BACKEND_URL = 'rpc://'

# app_celery = Celery('celery_app', broker=BROKER_URL, backend=BACKEND_URL)

# app_celery.conf.update(
#     task_serializer='json',
#     accept_content=['json'],
#     result_serializer='json',
#     beat_schedule={
#         'fetch_albert_heijn_data_every_30_seconds': {
#             'task': 'celery_app.tasks.fetch_albert_heijn_data',
#             'schedule': 30.0,
#         },
#         'fetch_jumbo_data_every_30_seconds': {
#             'task': 'celery_app.tasks.fetch_jumbo_data',
#             'schedule': 30.0,
#         },
#     },
# )

from celery import Celery

BROKER_URL = 'redis://localhost:6379/0' 
BACKEND_URL = 'redis://localhost:6379/0'

celery_app = Celery('celery_app', broker=BROKER_URL, backend=BACKEND_URL)
# celery_app.autodiscover_tasks(['code'])

# celery_app.conf.beat_schedule = {
#     'fetch_albert_heijn_data_every_30_seconds': {
#         'task': 'tasks.fetch_albert_heijn_data',
#         'schedule': 30.0,
#     },
#     'fetch_jumbo_data_every_30_seconds': {
#         'task': 'tasks.fetch_jumbo_data',
#         'schedule': 30.0,
#     },
# }
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    beat_schedule={
        'fetch_albert_heijn_data_every_30_seconds': {
            'task': 'tasks.fetch_albert_heijn_data',  
            'schedule': 30.0, 
        },
        'fetch_jumbo_data_every_30_seconds': {
            'task': 'tasks.fetch_jumbo_data',  
            'schedule': 30.0, 
        },
    },
)
