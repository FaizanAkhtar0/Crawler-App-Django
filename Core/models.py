import uuid

from django.db import models

from Crawler.settings import MEDIA_SAVE_PATH

# Create your models here.


class Content(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    image_name = models.TextField()


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    file = models.TextField()


class Thumbnail(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    image_name = models.ImageField()


class MasterURL(models.Model):
    id = models.AutoField(primary_key=True)
    master_url = models.TextField()
    page_depth = models.IntegerField()

    def __str__(self):
        return "URL ID: -> (" + str(self.id) + ') Depth: -> (' + str(self.page_depth) + ')'


class SubURL(models.Model):
    id = models.AutoField(primary_key=True)
    master_url = models.ForeignKey(MasterURL, on_delete=models.CASCADE)
    sub_url = models.TextField()
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.master_url) + ' |-> SubLink: (' + str(self.sub_url) + ')'


