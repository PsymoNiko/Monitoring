from django.db.models import Sum
from django.utils import timezone
from student_panel.models import Report
from .celery import app


@app.task
def add_unsubmitted_report(student_id):
    # Get the unsubmitted reports for the given student
    unsubmitted_reports = Report.objects.filter(student_id=student_id, is_submitted=False)

    # Calculate the number of unsubmitted reports
    num_unsubmitted = unsubmitted_reports.count()

    # Calculate the total delay
    total_delay = timezone.now().date() - unsubmitted_reports.latest('created_at').created_at.date()

    # Send a notification to the student
    # (Replace this with your own code to send a notification)
    print(f"You have {num_unsubmitted} unsubmitted reports with a total delay of {total_delay.days} days.")


@app.task
def calculate_total_study_time():
    # Calculate the total amount of study time for all reports
    queryset = Report.objects.all()
    total_amount_of_study = queryset.aggregate(total_amount=Sum('amount_of_study'))['total_amount'] or 0

    # Send a notification with the total study time
    # (Replace this with your own code to send a notification)
    print(f"The total amount of study time for all reports is {total_amount_of_study} hours.")


from django.utils import timezone
from student_panel.models import Student


@app.task
def set_daily_deadline():
    # Set the daily deadline for all students
    students = Student.objects.all()
    for student in students:
        student.daily_deadline = timezone.now().replace(hour=23, minute=59, second=59)
        student.save()

    # Send a notification that the daily deadline has been set
    # (Replace this with your own code to send a notification)
    print("Daily deadline has been set for all students.")


# @shared_task
def submit_un_submitted_reports(report_number):
    pass
