import django_rq


def enqueue_task(name_queue, process, data_task):

    # Se genera tarea que ejecutara valoracion sobre el producto
    queue = django_rq.get_queue(name_queue, default_timeout=3600)
    job = queue.enqueue(process, data_task)
    return job.id


def cron_job(name_queue, process, cron_string):
    scheduler = django_rq.get_scheduler(name_queue)
    scheduler.cron(
        cron_string,                # A cron string (e.g. "0 0 * * 0")
        func=process,               # Function to be queued
        repeat=None,                # Repeat this number of times (None
                                    # means repeat forever)
        queue_name=name_queue       # In which queue the job should be put in
    )
