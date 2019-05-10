"""
Contains all tasks about operations
"""
from netwark import celery_app


@celery_app.task(name='netwark.operation')
def run_operation(oper_id: str):
    print(
        "Hello boy this is a test message before writing the code of this task"
    )

    # TODO: Write the code for this task
