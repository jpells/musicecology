from datetime import datetime
from django.template import loader
from agenda.views.date_based import archive
from agenda.models import Event
from django.shortcuts import render_to_response
from musicecology.templateutils.templatetags.event_calendar import event_calendar

def index(request, queryset, date_field,
          template_name=None, template_object_name='object', template_loader=loader,
          num_objects=5, extra_context=None,
          mimetype=None, context_processors=None):

    now = datetime.now()
    queryset = queryset.filter(event_date__gte=now)

    return archive(request, queryset, date_field,
                   now.year, None, None,
                   template_name, template_object_name, template_loader,
                   num_objects, extra_context, True,
                   mimetype, context_processors)

def event_calendar_json(request, year, month):
    return render_to_response('agenda/event_calendar.html', event_calendar(None, int(year), int(month)))
