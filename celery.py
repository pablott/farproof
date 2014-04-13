from __future__ import absolute_import

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farproof.settings')
app = Celery('farproof',
			 include=['farproof.process.process'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()