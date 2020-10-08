import urllib

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse, path
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
    list_display = ['date', 'place_', 'number_attendees', 'create_email']
    ordering = ['-date']

    def number_attendees(self, obj):
        n_attendees = obj.attendees_set.count()
        return format_html(
            '{n_attendees} (<a href="{href}">list</a>)',
            n_attendees=n_attendees,
            href=reverse('admin:list-attendees', args=[obj.pk]),
        )

    def place_(self, obj):

        if obj.private_link is not None:
            return format_html(
                '{place} (<a href={href}>admin link</a>)',
                place=obj.place, href=obj.private_link
            )
        return obj.place

    def list_attendees(self, request, seminar_id):
        seminar = self.get_object(request, seminar_id)
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

    # Make the seminar's action available as URL to allow for link to action
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                r'<int:seminar_id>/list_attendees/',
                self.admin_site.admin_view(self.list_attendees),
                name='list-attendees',
            ),
        ]
        return custom_urls + urls

    # Format the name of the columns
    create_email.short_description = "Announcement email"
    list_attendees.short_description = "List attendees"
    list_attendees.place_ = "Place"


admin.site.register(Seminar, SeminarAdmin)
admin.site.register(Talk)
admin.site.register(Attendees)
