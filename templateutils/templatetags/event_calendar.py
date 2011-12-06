from datetime import date, datetime, timedelta
import calendar
from django import template
from django.db import models
Event = models.get_model('agenda', 'event')

register = template.Library()

def event_calendar(context=None, year=None, month=None):
    if context:
        if context.has_key('year'):
            year = context['year']
        if context.has_key('month'):
            month = context['month'].month
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month
    if month == 1:
        prev_month = 12
        prev_year = year - 1
        next_month = '%02d' % (month + 1)
        next_year = year
    elif month == 12:
        prev_month = '%02d' % (month - 1)
        prev_year = year
        next_month = "01"
        next_year = year + 1
    else:
        prev_month = '%02d' % (month - 1)
        prev_year = year
        next_month = '%02d' % (month + 1)
        next_year = year

    event_list = Event.objects.filter(event_date__year=year, event_date__month=month)

    first_day_of_month = date(year, month, 1)
    last_day_of_month = date(year, month, calendar.monthrange(year, month)[1])
    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())
    last_day_of_calendar = last_day_of_month + timedelta(7 - last_day_of_month.weekday())

    month_cal = []
    week = []
    week_headers = []

    i = 0
    day = first_day_of_calendar
    while day <= last_day_of_calendar:
        if i < 7:
            week_headers.append(day)
        cal_day = {}
        cal_day['day'] = day
        cal_day['event'] = False
        for event in event_list:
            if day >= event.event_date and day <= event.event_date:
                cal_day['event'] = event
        if day.month == month:
            cal_day['in_month'] = True
        else:
            cal_day['in_month'] = False  
        week.append(cal_day)
        if day.weekday() == 6:
            month_cal.append(week)
            week = []
        i += 1
        day += timedelta(1)

    return {'calendar': month_cal, 'headers': week_headers, 'year': year, 'month': month, 'month_name': calendar.month_name[month], 'month_abbr': calendar.month_abbr[month], 'prev_year': prev_year, 'prev_month': prev_month, 'next_year': next_year, 'next_month': next_month}

register.inclusion_tag('agenda/event_calendar.html', takes_context=True)(event_calendar)
