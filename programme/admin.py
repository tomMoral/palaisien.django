from django.contrib import admin
from django.http import HttpResponse

# Register your models here.
from .models import Attendees, Seminar, Talk


HEADER = "\t\t\t{}\nSurname\tName\tInstitution\n"


class SeminarAdmin(admin.ModelAdmin):
    list_display = ['date', 'place', 'number_attendees']
    ordering = ['date']
    actions = ['list_attendees']

    def number_attendees(self, obj):
        return obj.attendees_set.count()

    def list_attendees(self, request, queryset):
        seminar = queryset.first()
        if seminar is None:
            return

        attendees = seminar.attendees_set.iterator()
        header = HEADER.format(seminar)
        serialize_csv = header + "\n".join([
            '\t'.join([a.surname, a.name, a.institution])
            for a in attendees])

        response = HttpResponse(serialize_csv, content_type='text/csv')

        return response

    list_attendees.short_description = "List attendees"


admin.site.register(Seminar, SeminarAdmin)
admin.site.register(Talk)
admin.site.register(Attendees)
