from django.db.models import Sum
from monitoring.settings import MINIMUM_AMOUNT_OF_STUDY, COST_OF_PUNISHMENT_PER_HOUR
from celery import Celery
from celery import shared_task
from django.utils import timezone
from .models import Report

# app = Celery('tasks', backend='redis://localhost', broker='redis://localhost:6379/0')


def max_amount_of_study(amount: str) -> str:
    return max(amount)


def min_amount_of_study(amount: str) -> str:
    return min(amount)


def expected_hour(amount: str) -> str:
    return str(len(amount) * MINIMUM_AMOUNT_OF_STUDY)


def sum_of_report(amount: str) -> str:
    return sum(amount)


def punishment_for_fraction_of_hour(amount) -> str:
    expected = int(expected_hour(amount))
    sum_report = int(sum_of_report(amount))
    if sum_report > expected:
        return "0"
    punishment = (expected - sum_report) * COST_OF_PUNISHMENT_PER_HOUR
    return str(punishment)


def average_of_amount_of_report(amount: str) -> str:
    average = int(sum_of_report(amount)) / len(amount)
    return str(average)


from celery import shared_task
from django.utils import timezone
from student_panel.models import Report


@shared_task
def add_unsubmitted_report(student_id):
    # Calculate the number of unsubmitted reports
    num_unsubmitted = Report.objects.filter(student_id=student_id, is_submitted=False).count()

    # Calculate the total delay
    delay = timezone.now().date() - timezone.now().date()

    # Send a notification to the student
    # (Replace this with your own code to send a notification)
    print(f"You have {num_unsubmitted} unsubmitted reports with a total delay of {delay.days} days.")


@shared_task
def calculate_total_study_time():
    # Calculate the total amount of study time for all reports
    queryset = Report.objects.all()
    total_amount_of_study = queryset.aggregate(total_amount=Sum('amount_of_study'))['total_amount'] or 0

    # Send a notification with the total study time
    # (Replace this with your own code to send a notification)
    print(f"The total amount of study time for all reports is {total_amount_of_study} hours.")

