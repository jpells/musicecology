from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from agenda.sitemaps import EventSitemap
from agenda.feeds import EventFeed

from django.contrib.comments.feeds import LatestCommentFeed

from agenda.models import Event

from django.views.generic.simple import direct_to_template
from contact_form.views import contact_form
from contact_form.forms import AkismetContactForm

sitemaps = { 'events' : EventSitemap }

feeds = { 'events'   : EventFeed,
          'comments' : LatestCommentFeed }

agenda_index_info_dict = {
    'queryset'                  : Event.published.all(),
    'date_field'                : 'event_date',
    'template_object_name'      : 'event',
    'template_name'             : 'agenda/event_index.html',
}

agenda_detail_info_dict = {
    'queryset'                  : Event.published.all(),
    'date_field'                : 'event_date',
    'template_object_name'      : 'event',
    'template_name'             : 'agenda/event_detail.html',
}

urlpatterns = patterns('',
    (r'^admin/filebrowser/', include('filebrowser.urls')),

    # Examples:
    # url(r'^$', 'musicecology.views.home', name='home'),
    # url(r'^musicecology/', include('musicecology.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^grappelli/', include('grappelli.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),

    url(r'^contact/$', contact_form, {'form_class': AkismetContactForm}, name='contact_form'),
    url(r'^contact/sent/$', direct_to_template, { 'template': 'contact_form/contact_form_sent.html' }, name='contact_form_sent'),

    url(r'^event_calendar_json/(?P<year>\d{4})/(?P<month>\d{2})/$', 'musicecology.views.event_calendar_json', name='event-calendar-json'),

    url(r'^$', 'musicecology.views.index', agenda_index_info_dict, name='agenda-index'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 'agenda.views.date_based.object_detail', agenda_detail_info_dict,  name='agenda-detail'),
    (r'^', include('agenda.urls')),
)

if settings.DEBUG:
   urlpatterns += patterns('',
      url(r'', include('debug_toolbar_user_panel.urls')),
   )
