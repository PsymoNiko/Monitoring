from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin


from mentor.models import Mentor
from ceo.models import Course


class Student(models.Model):
    PERSONALITIES = (
        ('INTP', 'INTP'), ('INTJ', 'INTJ'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'),
        ('INFJ', 'INFJ'), ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('ESTP', 'ESTP'), ('ESFP', 'ESFP'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_course')
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    phone_number = models.CharField(max_length=13, unique=True)
    date_of_birth = models.DateField()
    identity_code = models.CharField(max_length=15, unique=True)
    personality = models.CharField(max_length=4, choices=PERSONALITIES)
    avatar = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    # objects = CustomUserManager()

    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['mentor', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'personality']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CurrentCourse(models.Model):
    belong_to = models.OneToOneField(Student, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=30)
    mentor = models.OneToOneField(Mentor, on_delete=models.CASCADE)
    course_length = models.IntegerField()
    completed = models.IntegerField()


class CompletedCourses(models.Model):
    course_name = models.CharField(max_length=50)
    mentor = models.OneToOneField(Mentor, on_delete=models.CASCADE)
    course_length = models.IntegerField()
    started_at = models.DateField()
    finished_at = models.DateField()

    def course_time(self):
        return f"{self.started_at} to {self.finished_at}"


class StudentSettings(models.Model):
    """
    For turn on/off the sms panel for each student
    """
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    installment_payment_due_date = models.BooleanField(default=False, editable=True)
    new_task = models.BooleanField(default=False, editable=True)
    new_message = models.BooleanField(default=False, editable=True)


class Report(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    report_text = models.TextField()
    report_number = models.PositiveIntegerField(default=1)
    amount_of_study = models.PositiveIntegerField()
    is_submitted = models.BooleanField(default=True)
    date_of_reporting = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


    # report_number = models.IntegerField(default=0)
    # report_text = models.TextField()
    # user = models.OneToOneField(Student, on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    # deadline = models.DateTimeField()
    # delayed = models.BooleanField(default=False)
    # study_amount = models.CharField(max_length=4)


class Payment(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    month_number = models.IntegerField()
    receipt = models.ImageField(upload_to='receipt_images/')
    status = models.CharField(max_length=20, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class AdminPayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='admin_payments')
    # payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='admin_payments')
    amount_of_receipt = models.CharField(max_length=9)
    receipt_count = models.IntegerField()
    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} you have to pay {self.amount_of_receipt} on {self.date}"

    @classmethod
    def create(cls, student, receipt_count, date):
        # Get the amount_of_receipt from the student
        amount_of_receipt = student.amount_of_receipt

        # Create a new AdminPayment object with the values passed as arguments
        admin_payment = cls(student=student, amount_of_receipt=amount_of_receipt, receipt_count=receipt_count, date=date)

        # Save the new AdminPayment object to the database
        admin_payment.save()

        # Return the new AdminPayment object
        return admin_payment