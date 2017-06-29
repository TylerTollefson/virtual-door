"""ApplicationBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from Atlas import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Base website URL patterns
    url(r'^$', views.home, name='home'),
    url(r'^howto/$', views.howto, name='howto'),
    url(r'^widgetinfo/$', views.widgetinfo, name='widgetinfo'),
    url(r'^confirmation/$', views.confirmation, name='confirmation'),
    url(r'^subscription/(?P<status>\w+)/(?P<passcode>\w+)$', views.subscription, name='subscription'),
    url(r'^bugreport/$', views.bugreport, name='bugreport'),
    url(r'^door/(?P<doorurl>\w+)$', views.door, name='door'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/create$', views.createprofile, name='createprofile'),
    url(r'^profile/edit$', views.editprofile, name='editprofile'),

    # Google+ authentication URL patterns
    url("^soc/", include("social_django.urls", namespace="social")),
    url('', include('django.contrib.auth.urls', namespace='auth')),

    # API URL patterns
    url(r'^api/notify/$', views.NotifyAPI.as_view()),
    url(r'^api/changelog/(?P<pk>\w+)/$', views.ChangelogAPI.as_view()),
    url(r'^api/sticky/(?P<pk>\w+)/$', views.StickyAPI.as_view()),
    url(r'^api/picture/(?P<pk>\w+)/$', views.PictureAPI.as_view()),
    url(r'^api/notification/(?P<pk>\w+)/$', views.NotificationAPI.as_view()),
    url(r'^api/calendar/(?P<pk>\w+)/$', views.CalendarAPI.as_view()),
    url(r'^api/calendardelete/(?P<pk>\w+)/$', views.CalendarDeleteAPI.as_view()),
    url(r'^api/calendaredit/(?P<pk>\w+)/$', views.CalendarEditAPI.as_view()),
    url(r'^api/layout/(?P<pk>\w+)/$', views.LayoutAPI.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

"""
    # Urls that handle Page objects and its API
    url(r'^page/$', views.PageList.as_view()),
    url(r'^page/(?P<pk>[0-9]+)/$', views.PageDetail.as_view()),

    # Urls that handle User objects and its API
    url(r'^user/$', views.UserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

    # Urls that handle Wiget objects and its API
    url(r'^widget/$', views.WidgetList.as_view()),
    url(r'^widget/(?P<pk>[0-9]+)/$', views.WidgetDetail.as_view()),
"""
