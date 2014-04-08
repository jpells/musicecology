from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import os
import csv
from mezzanine_events.models import EventLocation, Event, EventContainer
from django.core.exceptions import ValidationError
import datetime
from BeautifulSoup import BeautifulSoup
import urllib
from mezzanine.conf import settings
import urlparse
import logging

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--import_event_file',
            dest='import_event_file',
            default=None,
            help='Use specified import event csv file.'),
        make_option('--import_eventlocation_file',
            dest='import_eventlocation_file',
            default=None,
            help='Use specified import eventlocation csv file.'),
        make_option('--eventcontainer_id',
            dest='eventcontainer_id',
            default=None,
            help='Import events to specified event container.'),
    )

    help = 'Import Events from Django-Agenda'

    image_host = "http://musicecologyboston.com"
    event_image_save_path = os.path.join(settings.STATIC_ROOT, "media/uploads/events")
    location_headings = []
    locations = {}
    event_headings = []
    logger = logging.getLogger(__name__)

    def import_location(self, event_location_data):
        eventlocation = EventLocation(location="%s %s" % (event_location_data['title'], event_location_data['address']))
        try:
            eventlocation.clean()
        except ValidationError:
            #Cannot geocode location
            self.logger.warning("Cannot geocode: %s %s" % (event_location_data['title'], event_location_data['address']))
        eventlocation.save()
        self.locations[event_location_data['id']] = eventlocation

    def map_eventlocation_row(self, event_location_row):
        return dict(zip(self.location_headings, event_location_row))

    def import_locations(self, import_eventlocation_file):
        with open(import_eventlocation_file, 'rb') as eventlocation_file:
            event_locations = csv.reader(eventlocation_file)
            iter_eventlocations = iter(event_locations)
            self.location_headings = next(iter_eventlocations)
            for event_location_row in iter_eventlocations:
                self.import_location(self.map_eventlocation_row(event_location_row))

    def create_event_image_save_path(self):
        try:
            os.stat(self.event_image_save_path)
        except:
            os.mkdir(self.event_image_save_path)

    def resolve_images(self, content):
        parsed_content = BeautifulSoup(content)
        imgs = parsed_content.findAll('img')
        for img in imgs:
            try:
                #get image via src
                image = urllib.urlopen(img.get("src"))
            except:
                #get image via image_host + src
                image = urllib.urlopen(urlparse.urljoin(self.image_host, img.get("src")))
            if image.headers.maintype == 'image':
                new_image_path = os.path.join(self.event_image_save_path, os.path.basename(img.get("src")))
                f = open(new_image_path,'wb')
                f.write(image.read())
                f.close()
                content = content.replace(img.get("src"), new_image_path.replace(settings.PROJECT_ROOT, ""))
            else:
                #image can no longer be found
                content = content.replace(str(img), "")
        return content

    def import_event(self, event_data, eventcontainer_id):
        if event_data['location_id'] != "\N":
            eventlocation = self.locations[event_data['location_id']]
        else:
            eventlocation = None
        #eventlocation = EventLocation.objects.get(id=1)
        if event_data['start_time'] != "\N":
            start_datetime = datetime.datetime.combine(datetime.datetime.strptime(event_data['event_date'], "%Y-%m-%d"), datetime.datetime.strptime(event_data['start_time'],'%H:%M:%S').time())
        else:
            start_datetime = datetime.datetime.strptime(event_data['event_date'], "%Y-%m-%d")
        if event_data['end_time'] != "\N":
            end_datetime = datetime.datetime.combine(datetime.datetime.strptime(event_data['event_date'], "%Y-%m-%d") + datetime.timedelta(days=1), datetime.datetime.strptime(event_data['end_time'],'%H:%M:%S').time())
        else:
            end_datetime = None
        if event_data['facebook_event'] != "\N":
            facebook_event = event_data['facebook_event']
        else:
            facebook_event = None
        title = event_data['title'].decode('utf-8')
        content = event_data['description'].decode('utf-8')
        content = self.resolve_images(content)
        event_container = EventContainer.objects.get(page_ptr_id=eventcontainer_id)
        event = Event(start_datetime=start_datetime, end_datetime=end_datetime, event_location=eventlocation, facebook_event=facebook_event, parent=event_container, title=title, content=content)
        event.clean()
        event.save()

    def map_event_row(self, event_row):
        return dict(zip(self.event_headings, event_row))

    def update_event_order(self):
        #set order of events via start_datetime
        events = Event.objects.order_by('-start_datetime')
        i = 1
        for event in events:
            event._order = i
            event.save()
            i += 1

    def import_events(self, import_event_file, eventcontainer_id):
        with open(import_event_file, 'rb') as event_file:
            events = csv.reader(event_file)
            iter_events = iter(events)
            self.event_headings = next(iter_events)
            for event_row in events:
                self.import_event(self.map_event_row(event_row), eventcontainer_id)
        self.update_event_order()

    def handle(self, *args, **options):
        if not options.get('import_event_file'):
            raise CommandError('Option `--import_event_file=...` must be specified.')
        if not options.get('import_eventlocation_file'):
            raise CommandError('Option `--import_eventlocation_file=...` must be specified.')
        if not options.get('eventcontainer_id'):
            raise CommandError('Option `--eventcontainer_id=...` must be specified.')
        if not os.path.isfile(options.get('import_event_file')):
            raise CommandError("%s does not exist at the specified path." % options.get('import_event_file'))
        if not os.path.isfile(options.get('import_eventlocation_file')):
            raise CommandError("%s does not exist at the specified path." % options.get('import_eventlocation_file'))
        self.import_locations(options.get('import_eventlocation_file'))
        self.create_event_image_save_path()
        self.import_events(options.get('import_event_file'), options.get('eventcontainer_id'))