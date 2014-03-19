from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name



# from taggit.managers import TaggableManager
class Post(models.Model):
    #head
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=20)
    url = models.URLField(blank=True, null=True)
    #body
    summary = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    #attribute
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    is_top = models.BooleanField(default=False)

    #time
    create_time = models.DateTimeField(auto_now_add=True)
    publish_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title
    
    

