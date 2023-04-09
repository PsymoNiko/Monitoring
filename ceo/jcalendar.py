import datetime
import jdatetime
from datetime import datetime
from jdatetime import datetime as jdatetime_datetime

from rest_framework import serializers


class JalaliDateField(serializers.ReadOnlyField):
    def to_representation(self, value):
        return jdatetime.date.fromgregorian(date=value).strftime('%Y/%m/%d')


def convert_jalali_to_gregorian(jalali_date):
    jalali_date = jdatetime_datetime.strptime(jalali_date, '%Y-%m-%d').date()
    gregorian_date = jalali_date.togregorian()
    return datetime.combine(date=gregorian_date, time=datetime.min.time()).date()
