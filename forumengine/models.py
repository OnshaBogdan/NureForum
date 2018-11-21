from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80, blank=False, null=False, default='test')
    description = models.TextField(max_length=300, blank=True, default='default description')
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail_view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = str('cat_') + str(self.category_id)
            self.save()


class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=80, blank=False, null=False, default='unnamed')
    date_of_pub = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    rating = models.IntegerField(blank=False, null=False, default=0)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Topic, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = str('topic_') + str(self.topic_id)
            self.save()


class ForumUser(User):
    user_id = models.AutoField(primary_key=True)
    rating = models.IntegerField(blank=False, null=False, default=0)


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    body = models.TextField(blank=False, null=False)
    date_of_pub = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(blank=False, null=False, default=0)
    author = models.ForeignKey(ForumUser, on_delete=models.CASCADE, blank=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=False)
