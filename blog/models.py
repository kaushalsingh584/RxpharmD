from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    text = RichTextField(blank=True ,null = True)
    # text = models.CharField(max_length=5000)
    # img = models.ImageField()
    snippet = models.CharField(max_length=200,default="click on title to view full blog")
    created_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank = True,null= True) 

    # it will be used when i press the publish button
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment = True)

    def get_absolute_url(self):
        return reverse('post_detail',kwargs={'pk': self.pk})

    # it is always good to have string representation of it
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.post',related_name = 'comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.CharField(max_length=5000)
    created_date = models.DateTimeField(default = timezone.now)
    approved_comment = models.BooleanField(default = False)


    def approve(self):
        self.approved_comment = True
        self.save()
    def get_absolute_url(self):
        return reverse('post_detail')
    def __str__(self):
        return self.text