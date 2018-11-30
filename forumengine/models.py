from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


class ForumUser(User):
    user_id = models.AutoField(primary_key=True)
    rating = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_detail_url', kwargs={'id': self.id})


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
            self.slug = str(self.category_id)
            self.save()


class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=80, blank=False, null=False, default='unnamed')
    date_of_pub = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    rating = models.IntegerField(blank=False, null=False, default=0)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(ForumUser, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Topic, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = str(self.topic_id)
            self.save()

    def get_absolute_url(self):
        return reverse('topic_detail_view', kwargs={'slug': self.slug})


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    body = models.TextField(blank=False, null=False)
    date_of_pub = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(blank=False, null=False, default=0)
    author = models.ForeignKey(ForumUser, on_delete=models.CASCADE, blank=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=False)
    voted_users = models.ManyToManyField(ForumUser, blank=True, default=None, related_name='voted_users')

    def __str__(self):
        return self.author.__str__() + ' in ' + self.topic.__str__() + ' at ' + self.date_of_pub.ctime().__str__()

    def vote(self, user, isPlus):
        if isPlus:
            self.rating += 1
            self.author.rating += 1
            self.topic.rating +=1
        else:
            self.rating -= 1
            self.author.rating -= 1
            self.topic.rating -= 1
        self.voted_users.add(user)
        self.topic.save()
        self.author.save()
        self.save()

    def get_update_url(self):
        return reverse('message_update_url', kwargs={'message_id': self.message_id})
