from Monitoring.monitoring.settings import MINIMUM_AMOUNT_OF_STUDY, COST_OF_PUNISHMENT_PER_HOUR
from celery import Celery

app = Celery('tasks', backend='redis://localhost', broker='redis://localhost:6379/0')


@app.tasks()
def max_amount_of_study(amount: str) -> str:
    return max(amount)


@app.tasks()
def min_amount_of_study(amount: str) -> str:
    return min(amount)


@app.tasks()
def expected_hour(amount: str) -> str:
    return str(len(amount) * MINIMUM_AMOUNT_OF_STUDY)


@app.tasks()
def sum_of_report(amount: str) -> str:
    return sum(amount)


@app.tasks()
def punishment_for_fraction_of_hour(amount) -> str:
    expected = int(expected_hour(amount))
    sum_report = int(sum_of_report(amount))
    if sum_report > expected:
        return "0"
    punishment = (expected - sum_report) * COST_OF_PUNISHMENT_PER_HOUR
    return str(punishment)


@app.tasks()
def average_of_amount_of_report(amount: str) -> str:
    average = int(sum_of_report(amount)) / len(amount)
    return str(average)