# Standard library imports
import json
import re
from io import StringIO

# Django and dependency related imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, HttpResponseRedirect
from django.template.context import RequestContext
from django.utils.crypto import get_random_string
from PIL import Image
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Application imports
from Atlas.models import *
from Atlas.serializers import *


# Views specify how requests are handled.  Views are called when
# an url pattern associated with a view is accessed by a user.
#
# -------------------DJANGO DOCUMENTATION------------------- #
# Documentation on Django views can be found at:
# https://docs.djangoproject.com/en/1.11/topics/http/views/
#
# Documentation on Django model querysets can be found at:
# https://docs.djangoproject.com/en/1.10/ref/models/querysets/
#
# Documentation on Django email sending can be found at:
# https://docs.djangoproject.com/en/1.10/topics/email/
#
# Documentation on Django REST Framework can be found at:
# http://www.django-rest-framework.org/#api-guide
# ---------------------------------------------------------- #
#
#
# home renders the home page of the website.
def home(request):
    try:  # if someone is logged in, utilize their profile information
        profile = Profile.objects.get(user=request.user)
    except:
        profile = "None"
    context = {'user': request.user, 'profile': profile}

    return render(request, 'home.html', context)


# howto renders the "How to use" page of the website.
def howto(request):
    try:  # if someone is logged in, utilize their profile information
        profile = Profile.objects.get(user=request.user)
    except:
        profile = "None"
    context = {'user': request.user, 'profile': profile}

    return render(request, 'howto.html', context)


# widgetinfo renders the widget information page of the website.
def widgetinfo(request):
    try:  # if someone is logged in, utilize their profile information
        profile = Profile.objects.get(user=request.user)
    except:
        profile = "None"
    context = {'user': request.user, 'profile': profile}

    return render(request, 'widgetinfo.html', context)


# confirmation renders the page containing the email confirmation form.
# It also handles the submission of the confirmation form, informing the
# user what errors were with their submission.
def confirmation(request):
    message = ""
    form = SubscriptionForm()

    try:  # if someone is logged in, utilize their profile information
        profile = Profile.objects.get(user=request.user)
    except:
        profile = "None"

    if request.method == 'POST':
        form = SubscriptionForm(data=request.POST)
        if form.is_valid():
            try:  # see if there is a notification item with the input email and passcode
                notifItem = NotificationWD.objects.get(email=request.POST["email"],
                                                       passcode=form.cleaned_data["passcode"])
                doorprofile = Profile.objects.get(user=notifItem.door)
                if "subbed" in request.POST:  # change its subscription status depending on input
                    notifItem.subbed = True
                    message = "You have been subscribed to " + doorprofile.firstname + " " + doorprofile.lastname + "'s office door email notifications."
                else:
                    notifItem.subbed = False
                    message = "You have been unsubscribed from " + doorprofile.firstname + " " + doorprofile.lastname + "'s office door email notifications."

                notifItem.save()

            except:  # inform the user they entered data that has no associated entry
                message = "Could not find an entry for the entered email and passcode."
        else:  # inform the user of invalid input if the form was invalid
            message = "Your input was invalid."

    context = {'user': request.user,
               'profile': profile,
               'form': form,
               'message': message}
    return render(request, 'confirmation.html', context)


# subscription changes the status of a user's subscription to a door
# based on the URL path parameters when the page is accessed.
def subscription(request, status, passcode):
    message = ""

    try:  # if someone is logged in, utilize their profile information
        profile = Profile.objects.get(user=request.user)
    except:
        profile = "None"

    try:  # see if there is a notification item with the URL passcode
        notifItem = NotificationWD.objects.get(passcode=passcode)
        doorprofile = Profile.objects.get(user=notifItem.door)
        if status == "s":  # change its subscription status depending on input
            notifItem.subbed = True
            message = "You have been subscribed to " + doorprofile.firstname + " " + doorprofile.lastname + "'s office door email notifications."
        elif status == "u":
            notifItem.subbed = False
            message = "You have been unsubscribed from " + doorprofile.firstname + " " + doorprofile.lastname + "'s office door email notifications."
        else:  #inform the user of bad input
            message = "Status unchanged.  Double check that the URL you "
            message += "entered matches the URL you received in your email."
        notifItem.save()

    except:  # inform the user they entered data that has no associated entry
        message = "Could not find an entry for the entered passcode."

    context = {'user': request.user,
               'profile': profile,
               'message': message}
    return render(request, 'subscription.html', context)


# bugreport renders the page containing the bug report form.
# It also handles the submission of the bug report form,
# informing the user of any invalid input.
def bugreport(request):
    message = ""
    form = BugreportForm()

    try:  # if someone is logged in, utilize their profile information
        profile = Profile.objects.get(user=request.user)
    except:
        profile = "None"

    if request.method == 'POST':
        form = BugreportForm(data=request.POST)
        if form.is_valid():
            form.save()
            # inform the user of their successful bug report
            message = "Your bug report was successful.  Thank you for your feedback."
            form = BugreportForm()
        else:  # inform the user of invalid input
            message = "Your input was invalid."

    context = {'user': request.user,
               'profile': profile,
               'form': form,
               'message': message}
    return render(request, 'bugreport.html', context)


# door renders the page with the associated office door.
# If no door is associated with the input door url, the user is
# redirected to a page informing them no door exists with the url.
def door(request, doorurl):
    try:  # if someone is logged in, utilize their profile information
        yourprofile = Profile.objects.get(user=request.user)
    except:
        yourprofile = "None"

    try:  # check if the door url belongs to a door
        profile = Profile.objects.get(doorurl=doorurl.lower())
        user = profile.user
    except:  # if it doesn't, take them to a page informing them it doesn't
        context = {'user': request.user,
                   'url': doorurl,
                   'profile': yourprofile}

        return render(request, 'doornotfound.html', context)

    layoutItems = Layout.objects.filter(door=user)
    if not layoutItems:
        layoutBoolean = False
    else:
        layoutBoolean = True

    context = {'doorowner': user,
               'doorurl': doorurl,
               'layoutboolean': layoutBoolean,
               'profile': profile,
               'yourprofile': yourprofile}
    return render(request, 'office-door.html', context)


# profile renders the page where a user can see their own profile information.
# The user must be logged in to access this page.
@login_required
def profile(request):
    try:  # if someone is logged in, utilize their profile information
        profile = Profile.objects.get(user=request.user)
    except:
        profile = "None"
    context = {'user': request.user, 'profile': profile}
    return render(request, 'profile.html', context)


# createprofile renders the page containing the profile creation form.
# If the user already has a profile, they are redirected to the profile page.
# The user must be logged in to access this page.
@login_required
def createprofile(request):
    try:  # check if they already have a profile
        profile = Profile.objects.get(user=request.user)
        return HttpResponseRedirect("../profile/")
    except:
        profile = "None"
        form = ProfileForm()

    if request.method == 'POST':
        form = ProfileForm(data=request.POST)
        breakout = False
        if form.is_valid():  # if the input form was valid
            temp = Profile(user=request.user)
            temp.firstname = form.cleaned_data['firstname']
            temp.lastname = form.cleaned_data['lastname']

            try:  # check to see if the input doorurl is already taken
                x = Profile.objects.get(doorurl=form.cleaned_data['doorurl'].lower())
                breakout = True  # if it is, break out of the profile creation
                form.add_error('doorurl', "This doorurl is already taken.")
            except:  # if the above raises a doesnotexist error, it is available
                temp.doorurl = form.cleaned_data['doorurl'].lower()

            if request.FILES:
                try:  # check to see if the uploaded file was an image
                    trial_image = Image.open(request.FILES['bgimage'])
                    trial_image.verify()  # and ensure that it is valid
                    temp.bgimage = request.FILES['bgimage']
                except:  # inform them if it was not an image or invalid
                    form.errors['bgimage'] = "Only valid image files are allowed."
                    breakout = True  # break out of profile creation
            if breakout is False:
                # breakout ensures that erroneous profiles aren't saved
                temp.repeat = False
                if 'repeat' in request.POST:
                    temp.repeat = True
                temp.save()
                return HttpResponseRedirect("../profile/")

    context = {'user': request.user,
               'form': form,
               'profile': profile}
    return render(request, 'createprofile.html', context)


# editprofile renders the page containing the profile editing form.
# If the user has no profile, they are redirected to the create profile page.
# The user must be logged in to access this page.
@login_required
def editprofile(request):
    try:  # check if they already have a profile
        thisprofile = Profile.objects.get(user=request.user)
    except:
        return HttpResponseRedirect("../profile/create")

    form = ProfileForm(instance=thisprofile)
    breakout = False
    if request.method == 'POST':
        form = ProfileForm(data=request.POST)
        if form.is_valid():  # ensure that the submitted form was valid
            thisprofile.firstname = form.cleaned_data['firstname']
            thisprofile.lastname = form.cleaned_data['lastname']
            thisprofile.doorurl = form.cleaned_data['doorurl']

            try:  # check to see if the input doorurl is already taken
                x = Profile.objects.get(doorurl=form.cleaned_data['doorurl'].lower())

                if x.user == request.user:  # if the door url owner didn't change anything, do nothing
                    print("\tDoor url not changed.")
                else:  # if the requester is not the door url owner, they can't use the new url
                    breakout = True  # break out of the profile update
                    form.add_error('doorurl', "This doorurl is already taken.")
            except:  # if the above raises a doesnotexist error, it is available
                thisprofile.doorurl = form.cleaned_data['doorurl'].lower()

            if request.FILES:
                try:  # check to see if the uploaded file was an image
                    trial_image = Image.open(request.FILES['bgimage'])
                    trial_image.verify()  # and ensure that it is valid
                    thisprofile.bgimage = request.FILES['bgimage']
                except:  # inform them if it was not an image or invalid
                    form.errors['bgimage'] = "Only valid image files are allowed."
                    breakout = True  # break out of profile creation
            if 'bgimage-clear' in request.POST:
                # reset the background image to default if requested
                thisprofile.bgimage = 'atlas/static/default.png'
            if breakout is False:
                # breakout ensures that erroneous profiles aren't saved
                thisprofile.repeat = False
                if 'repeat' in request.POST:
                    thisprofile.repeat = True
                thisprofile.save()
                return HttpResponseRedirect("../profile/")

    context = {'user': request.user,
               'form': form,
               'profile': thisprofile}
    return render(request, 'editprofile.html', context)


"""####################### APIs #######################"""


# ChangelogAPI is the API to get all changes made to a door since
# the last notification email was sent out.
class ChangelogAPI(APIView):
    def get(self, request, pk, format=None):  # returns all changes for the primary key (door owner)
        try:  # ensure that there is a user for the associated primary key
            user = User.objects.get(username=pk)
        except:
            return Response({"error": "user does not exist"})

        try:  # if any change logs for the pk exists, get them
            changes = Changelog.objects.filter(door=user)
        except:  # otherwise return none
            changes = Changelog(user=user, description='None')
        serializer = ChangelogSerializer(changes, many=True)
        return Response(serializer.data)


# NotifyAPI is the API that dispatches the notification emails to
# all subscribers of a door upon a POST request by the door owner.
class NotifyAPI(APIView):
    def post(self, request, format=None):
        try:  # check if there's a door for the user making the request
            door = Profile.objects.get(user=request.user)
        except:  # if there wasn't return a bad response
            return Response({"error": "You do not have a door!"}, status=status.HTTP_400_BAD_REQUEST)

        try:  # get all of the users subscribed to their door
            subscribers = NotificationWD.objects.all().filter(door=request.user, subbed=True)
        except:  # if there are no subscribers, return an error message and bad response
            return Response({"error": "You do not have any subscribers!"}, status=status.HTTP_400_BAD_REQUEST)

        body = 'This is an email to let you know that ' + door.firstname + ' ' + door.lastname + '\'s Office Door has been updated.\n'

        changes = Changelog.objects.filter(door=request.user)
        for change in changes:
            body = body + '\t - ' + change.description + '\n'
        for subscriber in subscribers:
            fullbody = body + "To unsubscribe, visit http://virtualdoor.ddns.net/subscription/u/" + subscriber.passcode
            fullbody += '\n--------DO NOT REPLY TO THIS EMAIL!--------\n'
            send_mail(
                      'Virtual Office Door - Update ' + door.firstname + ' ' + door.lastname + '\'s Office Door Update',  # subjectline
                      fullbody,
                      'Automated@virtualdoor.ddns.net',  # from line
                      [subscriber.email],  # recipient list
                      fail_silently=False,
                      )
        changes.delete()  # delete all change entries, they're no longer needed
        return Response({"succes": "Emails have been sent!"},
                        status=status.HTTP_200_OK)


# StickyAPI is the API to retrieve and update sticky note contents.
# GET requests return the serialized sticky note text for the associated door.
# POST requests allow a door owner to modify the sticky note widget contents
# for their office door.
class StickyAPI(APIView):
    def get(self, request, pk, format=None):
        try:  # ensure that there is a user for the associated primary key
            user = User.objects.get(username=pk)
        except:
            return Response({"error": "user does not exist"})

        try:  # if a sticky item for the pk exists, return that
            stickyItem = StickyWD.objects.get(door=user)
        except:  # otherwise return an empty sticky item
            stickyItem = StickyWD()
        serializer = StickySerializer(stickyItem)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        try:  # ensure that there is a user for the associated primary key
            user = User.objects.get(username=pk)
        except:
            return Response({"error": "user does not exist"})

        try:  # check if there's already a sticky item
            stickyItem = StickyWD.objects.get(door=user)
        except:  # if not, start with a blank new one
            stickyItem = StickyWD()
            stickyItem.door = user

        parsedjson = json.loads(request.data['data'])
        # turn the POSTed JSON into a serializer object
        serializer = StickySerializer(data=parsedjson)

        # ensure that the sticky note can only be changed by the door owner
        # with valid input
        if serializer.is_valid() and request.user == user:
            stickyItem.notedata = serializer.data["notedata"]
            stickyItem.save()
            Changelog(door=user, description="Sticky note updated.").save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PictureAPI is the API to retrieve and update Picture widget contents.
# GET requests retrieve the url of the picture widget for the associated door.
# POST requests allow a door owner to upload a valid image file, it then is
# resized to have a maximum width and height of 800 pixels, maintaining the
# aspect ratio, before saving it on the server and associating it with the
# uploader's door and picture widget.
class PictureAPI(APIView):
    def get(self, request, pk, format=None):
        try:  # ensure that there is a user for the associated primary key
            user = User.objects.get(username=pk)
        except:
            return Response({"error": "user does not exist"})
        try:  # if a picture item for the pk exists, return that
            pictureItem = PictureWD.objects.get(door=user)
        except:  # otherwise return an empty picture item
            pictureItem = PictureWD()
        serializer = PictureSerializer(pictureItem)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        try:  # ensure that there is a user for the associated primary key
            user = User.objects.get(username=pk)
        except:
            return Response({"error": "user does not exist"})
        try:  # check if there's already a picture item
            pictureItem = PictureWD.objects.get(door=user)
        except:  # if not, start with a blank new one
            pictureItem = PictureWD()
            pictureItem.door = user

        if request.user == user:  # ensure that the uploader is the door owner
            try:  # check to see if the uploaded file is valid and an image
                trial_image = Image.open(request.FILES['upload'])
                trial_image.verify()
            except:  # uploaded file was not valid
                return Response({"error": "Invalid image file or format."}, status=status.HTTP_400_BAD_REQUEST)

            trial_image = Image.open(request.FILES['upload'])

            w, h = trial_image.size  # check to see if it exceeds 800x800
            if h > 800 or w > 800:  # and resize it if it does
                if h > w:
                    w = (int)((w/h)*800)
                    h = 800
                else:
                    h = (int)((h/w)*800)
                    w = 800
            else:  # don't touch it if it doesn't need to be resized
                print("\tImage does not require resizing.")

            trial_image = trial_image.resize((w, h), Image.ANTIALIAS)  # perform the resizing

            filename = get_random_string(length=16)  # generate a filename for it
            filename = 'atlas/static/PictureWidget/' + filename + str(request.FILES['upload'])  # add the proper path and suffix
            trial_image.save(filename)   # save the file so it can be used
            pictureItem.image = filename  # and point the database record to the file

            pictureItem.save()
            Changelog(door=user, description="New picture uploaded.").save()
            serializer = PictureSerializer(pictureItem)
            return Response(serializer.data)
        return Response({"error": "You do not own this door."}, status=status.HTTP_400_BAD_REQUEST)


# CalendarAPI is the API to get calendar events for a door and add new ones.
# GET requests get all calendar events associated with a corresponding door.
# POST requests allow a door owner to create a new calendar event.
class CalendarAPI(APIView):
    def get(self, request, pk, format=None):  # returns all calendar event for the associated primary key (door owner)
        try:  # ensure that there is a user for the associated primary key
            user = User.objects.get(username=pk)
        except:
            return Response({"error": "user does not exist"})

        try:  # if any calendar events for the pk exists, get them
            calendarEvents = CalendarWD.objects.filter(door=user).order_by('e_date', 'd_time')
        except:  # otherwise return an empty picture item
            calendarEvents = CalendarWD()
        serializer = CalendarSerializer(calendarEvents, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):  # creates one calendar event at a time
        try:  # ensure that there is a user for the associated primary key
            user = User.objects.get(username=pk)
        except:
            return Response({"error": "user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        parsedjson = json.loads(request.data['data'])
        # turn the POSTed JSON into a serializer object
        serializer = CalendarSerializer(data=parsedjson)

        # ensure that the calendar event can only be created by the door owner
        # with valid input
        if serializer.is_valid() and request.user == user:
            try:  # ensure that they are not creating a duplicate event
                calendarEvent = CalendarWD.objects.get(door=user,
                                                       message=serializer.data["message"],
                                                       e_date=serializer.data["e_date"],
                                                       d_time=serializer.data["d_time"])
                return Response({"error": "Event already exists!"}, status=status.HTTP_304_NOT_MODIFIED)
            except:
                newCalendarEvent = CalendarWD()
                newCalendarEvent.door = user
                newCalendarEvent.message = serializer.data["message"]
                newCalendarEvent.e_date = serializer.data["e_date"]
                newCalendarEvent.d_time = serializer.data["d_time"]
                newCalendarEvent.save()
                Changelog(door=user, description="New calendar event added.").save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CalendarDeleteAPI is the API to delete an existing calendar event for their
# door via a POST request of the event to delete.
class CalendarDeleteAPI(APIView):
    def post(self, request, pk, format=None):
        try:  # ensure that there is a user for the associated primary key
            user = User.objects.get(username=pk)
        except:
            return Response({"error": "user does not exist"})

        parsedjson = json.loads(request.data['data'])
        # turn the POSTed JSON into a serializer object
        serializer = CalendarSerializer(data=parsedjson)

        # ensure that the calendar event can only be deleted by the door
        # owner with valid input
        if serializer.is_valid() and request.user == user:
            try:  # ensure that there is a calendar event to delete
                calendarEvent = CalendarWD.objects.get(door=user,
                                                       message=serializer.data["message"],
                                                       e_date=serializer.data["e_date"],
                                                       d_time=serializer.data["d_time"])
            except:
                return Response({"error": "event does not exist!"})

            serializer = CalendarSerializer(calendarEvent)
            calendarEvent.delete()
            Changelog(door=user, description="Calendar event deleted.").save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CalendarEditAPI is the API to modify an existing calendar event for their
# door via a POST request of the event to modify and the contents to change
# it to.
class CalendarEditAPI(APIView):
    def post(self, request, pk, format=None):
        try:  # ensure that there is a user for the associated primary key
            user = User.objects.get(username=pk)
        except:
            return Response({"error": "user does not exist"})

        parsedjson = json.loads(request.data['data'])
        # turn the POSTed JSON into a serializer object
        serializer = EditCalendarSerializer(data=parsedjson)

        # ensure that the calendar event can only be edited by the door
        # owner with valid input
        if serializer.is_valid() and request.user == user:
            try:  # ensure that they are not creating a duplicate event
                calendarEvent = CalendarWD.objects.get(door=user,
                                                       message=serializer.data["message"],
                                                       e_date=serializer.data["e_date"],
                                                       d_time=serializer.data["d_time"])
                return Response({"error": "Event already exists!"}, status=status.HTTP_304_NOT_MODIFIED)
            except:
                print("\tClear for editing")

            try:  # ensure that there is a calendar event to delete
                calendarEvent = CalendarWD.objects.get(door=user,
                                                       message=serializer.data["oldmessage"],
                                                       e_date=serializer.data["olde_date"],
                                                       d_time=serializer.data["oldd_time"])
            except:
                return Response({"error": "event does not exist!"}, status=status.HTTP_304_NOT_MODIFIED)
            calendarEvent.message = serializer.data["message"]
            calendarEvent.e_date = serializer.data["e_date"]
            calendarEvent.d_time = serializer.data["d_time"]
            calendarEvent.save()
            Changelog(door=user, description="Calendar event edited.").save()
            serializer = CalendarSerializer(calendarEvent)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# NotificationAPI is the API to handle door notification subscriptions.
# If a valid email is POSTed to it for a valid door, it sends that user
# an email with instructions on how to subscribe or unsubscribe, depending
# on if an entry for their email address is in the database with the
# associated door.
class NotificationAPI(APIView):
    def post(self, request, pk, format=None):
        try:  # ensure that there is a user for the associated primary key
            user = User.objects.get(username=pk)
            thisprofile = Profile.objects.get(user=user)
        except:
            return Response({"error": "user does not exist"})

        parsedjson = json.loads(request.data['data'])
        # turn the POSTed JSON into a serializer object
        serializer = NotificationSerializer(data=parsedjson)
        if serializer.is_valid():
            try:  # check if there's already an entry for the email address for that door
                notifItem = NotificationWD.objects.get(email=serializer.data["email"],
                                                       door=user)
                body = 'Here are the links to discontinue or reinitiate your subscription to '
                body += thisprofile.firstname + ' ' + thisprofile.lastname + '\'s office door. \n\n'
                body += 'To unsubscribe, visit http://virtualdoor.ddns.net/subscription/u/' + notifItem.passcode
                body += '\nTo subscribe, visit http://virtualdoor.ddns.net/subscription/u/' + notifItem.passcode
                body += '\n--------DO NOT REPLY TO THIS EMAIL!--------\n'
                send_mail(
                        'Virtual Office Door - Subscription to ' + thisprofile.firstname + ' ' + thisprofile.lastname + '\'s Office Door',  # subjectline
                        body,
                        'Automated@virtualdoor.ddns.net',  # from line
                        [notifItem.email],  # recipient list
                        fail_silently=False,
                        )
                return Response({"success": "An email has been sent to the provided address to continue."}, status=status.HTTP_200_OK)

            except:  # otherwise make a new entry for that email and door
                notifItem = NotificationWD(email=serializer.data["email"],
                                           door=user,
                                           passcode=get_random_string(length=32))
                notifItem.subbed = False
                notifItem.save()
                body = 'Visit this link to confirm your subscription to '
                body += thisprofile.firstname + ' ' + thisprofile.lastname + '\'s office door. \n\n'
                body += 'http://virtualdoor.ddns.net/subscription/s/' + notifItem.passcode
                body += '\n--------DO NOT REPLY TO THIS EMAIL!--------\n'
                send_mail(
                            'Virtual Office Door Subscription Confirmation',  # subjectline
                            body,
                            'Automated@virtualdoor.ddns.net',  # from line
                            [notifItem.email],  # recipient list
                            fail_silently=False,
                         )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# LayoutAPI is the API for layout retrieval and updating.
# GET requests return the layout of each entry for the associated door.
# POST requests create or modify layout entries for each submitted layout
# object and delete any layout objects not posted in the valid request,
# only usable by a door owner.
class LayoutAPI(APIView):
    def get(self, request, pk, format=None):
        try:  # ensure that there is a user for the associated primary key
            user = User.objects.get(username=pk)
        except:
            return Response({"error": "user does not exist"})
        layoutRecords = Layout.objects.filter(door=user)
        # get all of the layout entries for the door and serialize them
        serializer = LayoutSerializer(layoutRecords, many=True)
        for item in serializer.data:  # remove the suffixes from model names
            if item['type'].endswith(" wd"):
                item['type'] = item['type'][0:-3]
            if item['type'].endswith(" label"):
                item['type'] = item['type'][0:-6]
        # and return the serialized layout data
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        try:  # ensure that there is a user for the associated primary key
            user = User.objects.get(username=pk)
        except:
            return Response({"error": "user does not exist"})

        parsedjson = json.loads(request.data['data'])
        serializer = LayoutSerializer(data=parsedjson, many=True)
        # turn the POSTed JSON into a serializer object
        # and check to see if it is valid and is from the door owner
        if serializer.is_valid() and request.user == user:
            deleteStickyFlag = True
            deletePictureFlag = True
            deleteCalendarFlag = True
            deleteNotificationFlag = True
            for item in serializer.data:  # for each item in the JSON

                # handle the sticky widget
                if (item['type'] == 'sticky'):
                    deleteStickyFlag = False  # since this widget layout was posted, don't delete it

                    # get the corresponding widget for foreign key id
                    try:
                        stickywidget = StickyWD.objects.get(door=user)
                    except:  # make a new one if none exists
                        stickywidget = StickyWD(door=user, notedata="Edit me!")
                        stickywidget.save()

                    # get the layout of the current widget
                    try:
                        stickylayout = Layout.objects.get(door=user, type=ContentType.objects.get(model='stickywd'))
                    except:  # create a new one if none exists
                        stickylayout = Layout(door=user, type=ContentType.objects.get(model='stickywd'))

                    stickylayout.x = item['x']
                    stickylayout.y = item['y']
                    stickylayout.width = item['width']
                    stickylayout.height = item['height']
                    stickylayout.object_id = stickywidget.id
                    stickylayout.save()

                # handle the picture widget
                elif (item['type'] == 'picture'):
                    deletePictureFlag = False  # since this widget layout was posted, don't delete it

                    # get the corresponding widget for foreign key id
                    try:
                        picturewidget = PictureWD.objects.get(door=user)
                    except:  # make a new one if none exists
                        picturewidget = PictureWD(door=user, image="atlas/static/placeholder.png")
                        picturewidget.save()

                    # get the layout of the current widget
                    try:
                        picturelayout = Layout.objects.get(door=user, type=ContentType.objects.get(model='picturewd'))
                    except:  # create a new one if none exists
                        picturelayout = Layout(door=user, type=ContentType.objects.get(model='picturewd'))

                    picturelayout.x = item['x']
                    picturelayout.y = item['y']
                    picturelayout.width = item['width']
                    picturelayout.height = item['height']
                    picturelayout.object_id = picturewidget.id
                    picturelayout.save()

                # handle the calendar widget
                elif (item['type'] == 'calendar'):
                    deleteCalendarFlag = False  # since this widget layout was posted, don't delete it

                    # get the corresponding widget for foreign key id
                    try:
                        calendarwidget = CalendarLABEL.objects.get(door=user)
                    except:  # make a new one if none exists
                        calendarwidget = CalendarLABEL(door=user)
                        calendarwidget.save()

                    # get the layout of the current widget
                    try:
                        calendarlayout = Layout.objects.get(door=user, type=ContentType.objects.get(model='calendarlabel'))
                    except:  # create a new one if none exists
                        calendarlayout = Layout(door=user, type=ContentType.objects.get(model='calendarlabel'))

                    calendarlayout.x = item['x']
                    calendarlayout.y = item['y']
                    calendarlayout.width = item['width']
                    calendarlayout.height = item['height']
                    calendarlayout.object_id = calendarwidget.id
                    calendarlayout.save()
                # handle the notification widget
                elif (item['type'] == 'notification'):
                    deleteNotificationFlag = False  # since this widget layout was posted, don't delete it

                    # get the corresponding widget for foreign key id
                    try:
                        notificationwidget = NotificationLABEL.objects.get(door=user)
                    except:  # make a new one if none exists
                        notificationwidget = NotificationLABEL(door=user)
                        notificationwidget.save()

                    # get the layout of the current widget
                    try:
                        notificationlayout = Layout.objects.get(door=user, type=ContentType.objects.get(model='notificationlabel'))
                    except:  # create a new one if none exists
                        notificationlayout = Layout(door=user, type=ContentType.objects.get(model='notificationlabel'))

                    notificationlayout.x = item['x']
                    notificationlayout.y = item['y']
                    notificationlayout.width = item['width']
                    notificationlayout.height = item['height']
                    notificationlayout.object_id = notificationwidget.id
                    notificationlayout.save()
            # end of for loop
            # delete the layout entries for widget layouts not posted
            if deleteStickyFlag:
                try:  # deletes sticky widget layout and widget data from the door if the layout was not posted
                    sticky = Layout.objects.get(door=user, type=ContentType.objects.get(model='stickywd'))
                    sticky.delete()
                    StickyWD.objects.get(door=user).delete()
                except:
                    print("\tSticky note layout flagged for deletion yet not deleted.")
            if deletePictureFlag:
                try:  # same as for before, but for the picture widget
                    picture = Layout.objects.get(door=user, type=ContentType.objects.get(model='picturewd'))
                    picture.delete()
                    PictureWD.objects.get(door=user).delete()
                except:
                    print("\tPicture layout flagged for deletion yet not deleted.")
            if deleteCalendarFlag:
                try:  # same as for before, but for the calendar widget
                    calendar = Layout.objects.get(door=user, type=ContentType.objects.get(model='calendarlabel'))
                    calendar.delete()
                    CalendarLABEL.objects.get(door=user).delete()
                    CalendarWD.objects.filter(door=user).delete()
                except:
                    print("\tCalendar layout flagged for deletion yet not deleted.")
            if deleteNotificationFlag:
                try:  # same as for before, but for the notification widget
                    notification = Layout.objects.get(door=user, type=ContentType.objects.get(model='notificationlabel'))
                    notification.delete()
                    NotificationLABEL.objects.get(door=user).delete()
                    NotificationWD.objects.filter(door=user).delete()
                except:
                    print("\tNotification layout flagged for deletion " +
                          "yet not deleted.")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
