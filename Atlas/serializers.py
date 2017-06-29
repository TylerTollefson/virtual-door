from rest_framework import serializers
from Atlas.models import *


# Serializer specify what data to parse between JSON and database
# entries.  The format is as follows:
#   {
#       "database model field" : [data]
#   }
# Serializers easily allow turning JSON into database entries or
# database entries into JSON.
#
# -----------DJANGO REST FRAMEWORK DOCUMENTATION------------ #
# Documentation on Django REST Framework can be found at:
# http://www.django-rest-framework.org/#api-guide
#
# Documentation on Django REST Framework's serializers:
# http://www.django-rest-framework.org/api-guide/serializers/
#
# Documentation on Django REST Framework's serializer fields:
# http://www.django-rest-framework.org/api-guide/fields/
# ---------------------------------------------------------- #
#
#
# StickySerializer specifies the JSON format of Sticky widget data
# to pass around in GET and POST requests.
class StickySerializer(serializers.ModelSerializer):
    class Meta:
        model = StickyWD
        fields = ('notedata',)


# PictureSerializer specifies the JSON format of Picture widget data
# to pass around in GET and POST requests.
class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureWD
        fields = ('image',)


# NotificationSerializer specifies the JSON format of notification
# subscriptions to a door, created when a new email subscription
# is requested via a POST request.
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationWD
        fields = ('email',)


# CalendarSerializer specifies the JSON format of calendar events
# when:
#       All calendar events for a door are requested via GET requests
#       Creating a new calendar event via a POST request
#       Deleting existing calendar events via a POST request
class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarWD
        fields = ('message', 'e_date', 'd_time')


# EditCalendarSerializer specifies the JSON format of a calendar event
# that is to be updated through a POST request.
# oldmessage, olde_date, and oldd_time are used to find an existing calendar
# event, and the existing message, e_date, and d_time fields are updated
# with the new information posted.
class EditCalendarSerializer(serializers.ModelSerializer):
    oldmessage = serializers.CharField()
    olde_date = serializers.DateField()
    oldd_time = serializers.TimeField()

    class Meta:
        model = CalendarWD
        fields = ('message', 'e_date', 'd_time',
                  'oldmessage', 'olde_date', 'oldd_time')


# LayoutSerializer specifies the JSON format of widget layouts
# to pass around in GET and POST requests.
class LayoutSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='none')

    class Meta:
        model = Layout
        fields = ('x', 'y', 'width', 'height', 'type')


# ChangelogSerializer specifies the JSON format of changes in
# a door's changelog to return through GET requests.
class ChangelogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Changelog
        fields = ('description',)
