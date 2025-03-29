from tasks.routes import get_task, get_tasks, update_task, delete_task

import time

t1 = time.time()
print(get_tasks())
print(time.time() - t1)
