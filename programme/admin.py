import urllib
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html


# Register your models here.
from .models import Attendees, Seminar, Talk


HEADER = "\t\t\t{}\nSurname\tName\tInstitution\n"


EMAIL_BODY_TEMPLATE = """
Dear all,


We hope to see you soon,
Best regards,
Victor-Emmanuel & Thomas for the "Séminaire Palaisien"

============================================================
{title_and_abstracts}
============================================================
"""


class SeminarAdmin(admin.ModelAdmin):
    list_display = ['date', 'place', 'number_attendees', 'create_email']
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

    def create_email(self, obj):
        to = "palaisien@inria.fr"
        subject = f"[Séminaire Palaisien] {obj.date:%A %d/%m/%y} - {obj.place}"
        subject = urllib.parse.quote(subject)

        talks = obj.talk_set.iterator()
        title_and_abstracts = []
        time_slots = ["16h-16h40", "16h40-17h20"] + ["00h-00h"] * 10
        for talk, slot in zip(talks, time_slots):
            speaker = f"[{talk.speaker}]({talk.site})"
            abstract = f"Abstract: {talk.abstract}"
            description = f"{slot} - {speaker} - {talk.title}\n\n{abstract}\n"
            title_and_abstracts.append(description)

        title_and_abstracts = ("-"*80 + '\n').join(title_and_abstracts)
        body = urllib.parse.quote(EMAIL_BODY_TEMPLATE.format(
            title_and_abstracts=title_and_abstracts))

        href = f"mailto:{to}?subject={subject}&body={body}"

        return format_html('<a href="{href}">send announcement</a>',
                           href=href)

    create_email.short_description = "Announcement email"
    list_attendees.short_description = "List attendees"


admin.site.register(Seminar, SeminarAdmin)
admin.site.register(Talk)
admin.site.register(Attendees)
