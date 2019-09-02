from django.db import models
from datetime import datetime

# Create your models here.


class Talk(models.Model):
    """Article and other publication fields"""
    title = models.CharField(max_length=500)
    speaker = models.CharField(max_length=256)

    place = models.CharField(max_length=500)

    pub_date = models.DateField('date published')

    site = models.CharField(max_length=500, default='/')
    slide = models.CharField(max_length=500, default="/")
    video = models.CharField(max_length=500, default="/")

    abstract = models.TextField(default="")
    short_description = models.CharField(max_length=500, default="")

    def __str__(self):
        return f"{self.speaker} -- {self.title}"

    def render(self):
        from django.template import loader
        template = loader.get_template("programme/items/talk.html")
        return template.render({"talk": self})
