from django.contrib import admin

# Register your models here.
from .models import Attendees, Seminar, Talk

admin.site.register(Seminar)
admin.site.register(Talk)
admin.site.register(Attendees)
