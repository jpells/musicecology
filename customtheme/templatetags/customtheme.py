from __future__ import unicode_literals
from BeautifulSoup import BeautifulSoup
from datetime import datetime

from django.db.models import Q

from mezzanine_agenda.models import Event, EventLocation
from mezzanine.blog.models import BlogPost, BlogCategory
from mezzanine.generic.models import Keyword
from mezzanine.template import Library
from mezzanine.utils.models import get_user_model

User = get_user_model()

register = Library()


@register.as_tag
def recent_posts_and_upcoming_events(limit=5, tag=None, username=None, category=None, location=None):
    """
    Put a dictionary of 3 different wells containing recent posts and upcoming events
    into the template context. A tag title or slug, category title, location title or slug or author's
    username can also be specified to filter the recent posts and upcoming events returned.

    Usage::

        {% recent_posts_and_upcoming_events 5 as recent_posts_and_upcoming_events %}
        {% recent_posts_and_upcoming_events limit=5 tag="django" as recent_posts_and_upcoming_events %}
        {% recent_posts_and_upcoming_events limit=5 category="python" as recent_posts_and_upcoming_events %}
        {% recent_posts_and_upcoming_events limit=5 location="home" as recent_posts_and_upcoming_events %}
        {% recent_posts_and_upcoming_events 5 username=admin as recent_posts_and_upcoming_events %}

    """
    blog_posts = BlogPost.objects.published().select_related("user")
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)
    if tag is not None:
        try:
            tag = Keyword.objects.get(title_or_slug(tag))
            blog_posts = blog_posts.filter(keywords__keyword=tag)
        except Keyword.DoesNotExist:
            blog_posts = []
    if blog_posts and category is not None:
        try:
            category = BlogCategory.objects.get(title_or_slug(category))
            blog_posts = blog_posts.filter(categories=category)
        except BlogCategory.DoesNotExist:
            blog_posts = []
    if blog_posts and username is not None:
        try:
            author = User.objects.get(username=username)
            blog_posts = blog_posts.filter(user=author)
        except User.DoesNotExist:
            blog_posts = []
    events = Event.objects.published().select_related("user")
    #Get upcoming events/ongoing events
    events = events.filter(Q(start__gt=datetime.now()) | Q(end__gt=datetime.now()))
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)
    if tag is not None:
        try:
            tag = Keyword.objects.get(title_or_slug(tag))
            events = events.filter(keywords__keyword=tag)
        except Keyword.DoesNotExist:
            events = []
    if events and location is not None:
        try:
            location = EventLocation.objects.get(title_or_slug(location))
            events = events.filter(location=location)
        except EventLocation.DoesNotExist:
            events = []
    if events and username is not None:
        try:
            author = User.objects.get(username=username)
            events = events.filter(user=author)
        except User.DoesNotExist:
            events = []
    recent_posts_and_upcoming_events = []
    for blog_post in blog_posts:
        blog_post.sort_datetime = blog_post.publish_date
        recent_posts_and_upcoming_events.append(blog_post)
    for event in events:
        event.sort_datetime = event.start
        recent_posts_and_upcoming_events.append(event)
    recent_posts_and_upcoming_events.sort(key=lambda x: x.sort_datetime, reverse=True)
    well_1 = recent_posts_and_upcoming_events[::3]
    well_2 = recent_posts_and_upcoming_events[1::3]
    well_3 = recent_posts_and_upcoming_events[2::3]
    return {"well_1": well_1, "well_2": well_2, "well_3": well_3}


@register.filter(is_safe=True)
def get_img(content):
    """
    Generates a url to the first image in the content.
    """
    parsed_content = BeautifulSoup(content)
    img = parsed_content.find('img')
    return img.get("src")
