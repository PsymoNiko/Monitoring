from django.core.management.base import BaseCommand
from datetime import datetime, time, timedelta
from django.db.models import Q
from student.models import Student, Report


class Command(BaseCommand):
    help = 'Create missing reports for students who did not submit a report on the current day'

    def handle(self, *args, **options):
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        target_time = time(hour=11, minute=0, second=0)  # 10 pm

        if current_time < target_time:
            # It's not yet 10 pm, so we don't create any reports
            return

        # Get the list of all students who have submitted a report for the current day
        submitted_students = Report.objects.filter(
            time_of_submit__date=current_date
        ).values_list('student', flat=True).distinct()

        # Get the list of all students who have not submitted a report for the current day
        missing_students = Student.objects.exclude(
            Q(id__in=submitted_students) | Q(report__create_at__date=current_date)
        )

        # Create a new report for each missing student
        for student in missing_students:
            existing_report_count = Report.objects.filter(student=student).count()
            report = Report.objects.create(
                student=student,
                report_number=existing_report_count + 1,
                report_text='not_submitted',
                study_amount=0,
                created_through_command=True

            )

            self.stdout.write(f"Created missing report for student {student}: {report}")
# class Command(BaseCommand):
#     help = 'Create missing reports for students who did not submit a report on the current day'
#
#     def handle(self, *args, **options):
#         result = create_missing_reports.delay()
#         self.stdout.write(f"Task ID: {result.task_id}")