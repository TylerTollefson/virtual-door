from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models


# Models specify how data is stored in the database, offering
# an abstraction of SQL queries.  Each model class corresponds
# to a table in a database, and each model class's field corresponds
# to a column in its model's table.
#
# ----------------------IMPORTANT NOTE---------------------- #
# If you intend to ever add any widgets to this application, #
# you must first determine how many entries correspond to    #
# any given door for that widget.  If it has one database    #
# entry per door, no special cases need to be considered.    #
# If the widget has many entries corresponding to it per     #
# door, it is necessary to create an associated LABEL model  #
# in order to properly store that widget's layout entry on   #
# any door indefinitely.                                     #
# ---------------------------------------------------------- #
#
#
# -------------------DJANGO DOCUMENTATION------------------- #
# Documentation on Django's models can be found at:
# https://docs.djangoproject.com/en/1.10/ref/models/
#
# Information on model fields can be found at:
# https://docs.djangoproject.com/en/1.10/ref/models/fields/
#
# Information on model queries can be found at:
# https://docs.djangoproject.com/en/1.10/ref/models/querysets/
# ---------------------------------------------------------- #
#
#
# The Bugreport model contains information for any user or guest
# submitted bug report, allowing categorization, titling, and description.
class Bugreport(models.Model):
    categories = (
        ('w', 'General Website'),
        ('p', 'Profile'),
        ('d', 'Office Door'),
        ('n', 'Notifications'))
    category = models.CharField(max_length=1, choices=categories, default='1')
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1000)


# BugreportForm is the form that appears to someone entering a bugreport
class BugreportForm(forms.ModelForm):
    class Meta:
        model = Bugreport
        fields = ('category', 'title', 'description',)


# Changelog is the model that holds changes associated with a door
# All changes associated with a door are wiped when a notification email
# is sent.
class Changelog(models.Model):
    door = models.ForeignKey(User)
    description = models.CharField(max_length=128)


# Profile is the model where a user's personal information relating
# to their door is stored, such as the background image or door url.
class Profile(models.Model):
    urlvalidator = RegexValidator(r'^([a-z]|[A-Z]|[0-9])\w+$', 'Only Alphanumeric characters and _ are allowed.  Must be at least 2 characters long.')
    imagevalidator = RegexValidator(r'^.+(\.png|\.jpg|\.jpeg)$', 'Only image files are allowed.')
    user = models.OneToOneField(User)
    firstname = models.CharField(max_length=32)
    lastname = models.CharField(max_length=32)
    doorurl = models.CharField(max_length=32, validators=[urlvalidator])
    bgimage = models.ImageField('img',
                                upload_to='atlas/static/backgrounds',
                                blank=True,
                                null=True,
                                validators=[imagevalidator],
                                default='atlas/static/default.png')
    doorowner = models.BooleanField(default=False)
    repeat = models.BooleanField(default=False)


# ProfileForm is the form that appears to users when creating or
# editing their profile.
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'doorurl': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('firstname', 'lastname', 'doorurl', 'bgimage', 'repeat',)


# Layout is the model that stores all layout information of widgets on
# a door.  It stores the widget's location, what type of widget is in
# the layout entry, and which user's door it is associated with.
class Layout(models.Model):
    door = models.ForeignKey(User)
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    row = models.IntegerField(blank=True, null=True)
    col = models.IntegerField(blank=True, null=True)
    # type stores what widget model to access
    type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id stores the associated widget model entry's pk
    object_id = models.PositiveIntegerField()
    # content_object lets us have an fk to multiple different models
    content_object = GenericForeignKey('type', 'object_id')


# NotificationWD is the model where subscriptions to a door are stored.
# Only verified subscriptions will receive emails from the door owner.
class NotificationWD(models.Model):
    door = models.ForeignKey(User)
    email = models.EmailField(default="")
    # Passcode is a long generated string that a user is emailed when
    # they try to subscribe to someone's door.  Verification of this
    # passcode to update their "subbed" status is done through a form.
    passcode = models.CharField(max_length=32)
    subbed = models.BooleanField(default=False)


# SubscriptionForm is the form where someone can update the status
# of their subscription to a door, housed at the following url:
# http://[root url]/confirmation/
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = NotificationWD
        fields = ('email', 'passcode', 'subbed')


# StickyWD stores the text that appears in a user's sticky note
# widget on their office door.
class StickyWD(models.Model):
    door = models.ForeignKey(User)
    notedata = models.CharField(max_length=256)


# CalendarWD stores the calendar events that appear in a user's
# calendar widget on their office door.
class CalendarWD(models.Model):
    door = models.ForeignKey(User)
    e_date = models.DateField()
    d_time = models.TimeField()
    message = models.CharField(max_length=32)


# PictureWD stores the location of the picture that appears on a
# user's office door.
class PictureWD(models.Model):
    door = models.ForeignKey(User)
    image = models.ImageField('img', upload_to='atlas/static/PictureWidget')
    # if we do this, it requires Pillow (i.e. pip install Pillow)
    # validates image, has height/width attributes


# NotificationLABEL is necessary to bind a Layout database entry
# with a user's notification widget placement.  Since any given door
# that has a notification widget has 0-Numerous subscriptions to it,
# it needs some fixed database entry to bind the notification widget
# to the door, which the NotificationLABEL serves to do.
class NotificationLABEL(models.Model):
    door = models.ForeignKey(User)


# CalendarLABEL serves the same purpose as NotificationLABEL, but for
# calendar events.
class CalendarLABEL(models.Model):
    door = models.ForeignKey(User)
