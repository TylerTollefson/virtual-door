from django.contrib import admin
from Atlas.models import *

# Register your models here.
# class SeatsAdmin(admin.ModelSeats):
#     pass
#     admin.site.register(Seats, SeatsAdmin)

# The following are models that can be accessed and manipulated through
# the admin interface at http://[root website url]/admin/

admin.site.register(Bugreport)
admin.site.register(Profile)
admin.site.register(Layout)
admin.site.register(NotificationWD)
admin.site.register(StickyWD)
admin.site.register(CalendarWD)
admin.site.register(PictureWD)
admin.site.register(NotificationLABEL)
admin.site.register(CalendarLABEL)
