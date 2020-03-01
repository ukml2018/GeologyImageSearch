import os

workers = int(os.environ.get('', '3'))GUNICORN_PROCESSES
threads = int(os.environ.get('GUNICORN_THREADS', '1'))

forwarded_allow_ips = '*'
secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }
