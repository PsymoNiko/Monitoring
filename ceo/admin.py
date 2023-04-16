from django.contrib import admin

from .models import Course, DailyNote
from student.models import AdminPayment
# Register your models here.


admin.site.register(Course)
admin.site.register(DailyNote)
admin.site.register(AdminPayment)