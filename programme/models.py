from django.db import models
from .utils import process_code_blocks


class Seminar(models.Model):
    """Seminar"""
    date = models.DateField('seminar date')
    time = models.TimeField('seminar time', default='12:15')
    place = models.CharField(max_length=500, default="TBA")
    link = models.CharField(max_length=500, default=None, blank=True,
                            null=True)
    private_link = models.CharField(max_length=500, default=None,
                                    null=True, blank=True)
    capacity = models.IntegerField('Capacity', default=200, null=True)

    def __str__(self):
        return (f"Seminar {self.date:%d-%m-%Y} -- {self.place}"
                f" -- {self.attendees_set.count()} participants")

    def render(self):
        from django.template import loader
        template = loader.get_template("programme/items/seminar.html")
        return template.render({"seminar": self})


class Talk(models.Model):
    """Talks linked ot a given seminar"""
    # Link to the seminar
    seminar = models.ForeignKey(Seminar, null=True,
                                on_delete=models.SET_NULL)

    # Information on the speaker
    speaker = models.CharField(max_length=256)
    site = models.CharField(max_length=500, default='/')

    # Information on the talk
    title = models.CharField(max_length=500, default="TBA")
    abstract = models.TextField(default="TBA")
    short_description = models.CharField(max_length=500, default="TBA")

    # ref to slides or recordings of the talk
    slide = models.CharField(max_length=500, default="/")
    video = models.CharField(max_length=500, default="/")

    def __str__(self):
        return f"{self.speaker} - {self.title}"

    def render(self, date=None, place=None):
        from django.template import loader
        template = loader.get_template("programme/items/talk.html")

        return template.render({
            "talk": self, "date": date, "place": place,
            "title": process_code_blocks(self.title),
            "desc": process_code_blocks(self.short_description),
            "abstract": process_code_blocks(self.abstract),
            })


class Attendees(models.Model):
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256, default='')
    institution = models.CharField(max_length=256)
    seminar = models.ForeignKey(Seminar, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.surname} - {self.institution}"
