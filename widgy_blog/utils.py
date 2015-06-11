import itertools
import datetime

from django.core import urlresolvers


class Year(list):
    def __init__(self, year, months):
        months = itertools.groupby(months, lambda d: d.month)
        super(Year, self).__init__(Month(year, *args) for args in months)
        self.date = datetime.date(year, 1, 1)

    @property
    def count(self):
        return sum(month.count for month in self)

    def get_absolute_url(self):
        return urlresolvers.reverse('blog_archive_year', kwargs={
            'year': self.date.year,
        })


class Month(list):
    def __init__(self, year, month, days):
        days = itertools.groupby(days, lambda d: d.day)
        super(Month, self).__init__(Day(year, month, *args) for args in days)
        self.date = datetime.date(year, month, 1)

    @property
    def count(self):
        return sum(day.count for day in self)

    def get_absolute_url(self):
        return urlresolvers.reverse('blog_archive_month', kwargs={
            'year': self.date.year,
            'month': '{0:02}'.format(self.date.month),
        })


class Day(datetime.date):
    def __new__(cls, year, month, day, posts):
        obj = super(Day, cls).__new__(cls, year, month, day)
        obj.count = sum(1 for _ in posts)
        return obj


def date_list_to_archive_list(values):
    years = itertools.groupby(values, lambda d: d.year)
    return [Year(*args) for args in years]
