from django.core.management.base import BaseCommand
import mezzanine_events
import mezzanine_agenda
from django.core.exceptions import ValidationError
import logging
from mezzanine.utils.models import get_user_model

class Command(BaseCommand):
    help = 'Import Events from mezzanine-events'

    locations = {}
    user = get_user_model().objects.get(id=3)
    logger = logging.getLogger(__name__)

    def import_location(self, location):
        eventlocation = mezzanine_agenda.models.EventLocation(title=location.location, address=location.location, mappable_location=location.mappable_location, lat=location.lat, lon=location.lon)
        try:
            eventlocation.clean()
        except ValidationError:
            #Cannot geocode location
            self.logger.warning("Cannot geocode: %s" % location.location)
        eventlocation.save()
        self.locations[location.id] = eventlocation

    def import_locations(self):
        locations = mezzanine_events.models.EventLocation.objects.all()
        for location in locations:
            self.import_location(location)
        

    def import_event(self, event):
        if event.event_location:
            eventlocation = self.locations[event.event_location.id]
        else:
            eventlocation = None
        event = mezzanine_agenda.models.Event(publish_date=event.start_datetime, start=event.start_datetime, end=event.end_datetime, location=eventlocation, facebook_event=event.facebook_event, title=event.title, content=event.content, user=self.user)
        event.clean()
        event.save()

    def import_events(self):
        events = mezzanine_events.models.Event.objects.all()
        for event in events:
            self.import_event(event)

    def handle(self, *args, **options):
        self.import_locations()
        self.import_events()