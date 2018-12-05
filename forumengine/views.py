from django.views.generic import View
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from forumengine.models import *
from forumengine.utils import *
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.db.models import Count, Sum, Avg, Max
from django.db.models.functions import Length, Lower
import datetime
from django.utils import timezone

class CategoryDetail(View):

    def get(self, request, slug):
        obj = get_object_or_404(Category, slug__iexact=slug)
        context = {'category': obj,
                   'topic_list': Topic.objects.filter(category=obj)
                   }
        if request.user.is_authenticated:
            user = ForumUser.objects.get(username=request.user.username)
            context['user'] = user
        return render(request, 'forumengine/category_detail_template.html', context=context)


class TopicDetail(View):
    def get(self, request, slug):
        search_query = request.GET.get('search', '')
        page_number = request.GET.get('page', 1)
        obj = get_object_or_404(Topic, slug__iexact=slug)

        if search_query:
            messages = Message.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
        else:
            messages = Message.objects.filter(topic=obj)
        paginator = Paginator(messages, 5)

        page = paginator.get_page(page_number)
        prev_url = '?page={}'.format(page.previous_page_number()) if page.has_previous() else ''
        next_url = '?page={}'.format(page.next_page_number()) if page.has_next() else ''
        is_paginated = page.has_other_pages()

        if messages.count() != 0:
            last_message = messages.last().date_of_pub
            empty = False
        else:
            last_message = ''
            empty = True

        context = {
            'topic': obj,
            'messages_count': messages.count(),
            'empty': empty,
            'last_message': last_message,
            'page_object': page,
            'prev_url': prev_url,
            'next_url': next_url,
            'is_paginated': is_paginated,
            'user': None
        }
        if request.user.is_authenticated:
            user = ForumUser.objects.get(username=request.user.username)
            context['user'] = user
            voted = {}
            for i in messages:
                try:
                    i.voted_users.get(username=user.username)
                    voted[i.message_id] = True
                except forumengine.models.ForumUser.DoesNotExist:
                    voted[i.message_id] = False
            context['voted'] = voted
        return render(request, 'forumengine/topic_detail_template.html', context=context)


class VoteMessage(View):

    def post(self, request):
        slug = request.POST.get('slug', False)
        page = request.POST.get('page', 1)
        message_id = request.POST.get('message_id')
        message = Message.objects.get(message_id=message_id)
        current_user = ForumUser.objects.get(username=request.user.username)

        try:
            message.voted_users.get(username=current_user.username)
        except forumengine.models.ForumUser.DoesNotExist:
            if request.POST.get('plus'):
                message.vote(current_user, True)
            else:
                message.vote(current_user, False)
        finally:
            return redirect(reverse('topic_detail_view', kwargs={'slug': slug}) + '?page=' + page)


class BestMessages(View):

    def post(self, request):
        def time_range_to_date(time_range):

            if time_range == 'Daily':
                days_sub = 1
            elif time_range == 'Weekly':
                days_sub = 7
            elif time_range == 'Monthly':
                days_sub = 28
            else:
                days_sub = 1000
            date = datetime.datetime.now() + datetime.timedelta(days_sub * -1)

            return date

        def message_filter(user, time_range, lowest, highest, order):
            date_now = datetime.datetime.now()
            messages = Message.objects.all()
            if lowest is None:
                lowest = -100
            if highest is None:
                highest = 1000
            if user is not None:
                messages = messages.filter(author=user)
            messages = messages.filter(date_of_pub__range=(time_range, date_now))

            if lowest < highest:
                messages = messages.filter(rating__range=(lowest, highest))

            if order == 'Message':
                messages = messages.order_by(Length('body').asc())
            elif order == 'Author':
                messages = messages.order_by(Lower('author').asc())
            elif order == 'Topic':
                messages = messages.order_by('-topic')
            elif order == 'Rating':
                messages = messages.order_by('-rating')
            elif order == 'Date of pub':
                messages = messages.order_by('-date_of_pub')
            return messages

        form = MessageFilterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            time_range = time_range_to_date(form.cleaned_data['time_range'])
            lowest_rating = form.cleaned_data['lowest_rating']
            highest_rating = form.cleaned_data['highest_rating']
            order = form.cleaned_data['order']
            if lowest_rating is None:
                lowest_rating = -100
            if highest_rating is None:
                highest_rating = 1000

            try:
                user = ForumUser.objects.get(username=username)
            except forumengine.models.ForumUser.DoesNotExist:
                user = None
            messages = message_filter(user, time_range, lowest_rating, highest_rating, order)

            context = {
                'message_list': messages,
                'user': user,
                'form': form
            }

            return render(request, 'forumengine/best_messages_template.html', context=context)

        return render(request, 'forumengine/best_messages_template.html', context={})

    def get(self, request, time_range='2018-01-01'):
        form = MessageFilterForm()
        date_now = datetime.datetime.now().date()

        messages = Message.objects.filter(date_of_pub__range=(time_range, date_now)).order_by('-rating')
        if request.user.is_authenticated:
            user = ForumUser.objects.get(username=request.user.username)
        else:
            user = None
        context = {
            'message_list': messages,
            'user': user,
            'form': form
        }
        return render(request, 'forumengine/best_messages_template.html', context=context)


class HotTopics(View):
    def get(self, request):
        form = TopicFilterForm()
        topic_list = Topic.objects.all()
        count = []
        for topic in topic_list:
            count.append(Message.objects.filter(topic=topic).count())

        context = {
            'topic_list': topic_list,
            'count': count,
            'form': form,
        }
        if request.user.is_authenticated:
            user = ForumUser.objects.get(username=request.user.username)
            context['user'] = user
        return render(request, 'forumengine/hot_topics_template.html', context=context)

    def post(self, request):
        def topic_filter(title, username, lowest, highest, order):
            topics = Topic.objects.all()

            topics = topics.filter(title__icontains=title)

            if username is not None:
                users = ForumUser.objects.filter(Q(username__icontains=username) | Q(username=username))
                topics = topics.filter(author__in=users)

            if lowest < highest:
                topics = topics.filter(rating__range=(lowest, highest))

            if order == 'Author':
                topics = topics.order_by('-author')
            elif order == 'Rating':
                topics = topics.order_by('-rating')
            elif order == 'Date of pub':
                topics = topics.order_by('-date_of_pub')
            elif order == 'Category':
                topics = topics.order_by('-category')
            elif order == 'Count of messages':
                topics = topics.annotate(msg_count=Count('message')).order_by('-msg_count')
            return topics

        form = TopicFilterForm(request.POST)

        user = ForumUser.objects.get(username=request.user.username) if request.user.is_authenticated else None

        if form.is_valid():
            title = form.cleaned_data['title']
            username = form.cleaned_data['username']
            lowest_rating = form.cleaned_data['lowest_rating']
            highest_rating = form.cleaned_data['highest_rating']
            order = form.cleaned_data['order']

            if lowest_rating is None:
                lowest_rating = -100
            if highest_rating is None:
                highest_rating = 1000

            topic_list = topic_filter(title, username, lowest_rating, highest_rating, order)
            count = []
            for topic in topic_list:
                count.append(Message.objects.filter(topic=topic).count())
            context = {
                'topic_list': topic_list,
                'user': user,
                'form': form,
                'count': count,
            }

            return render(request, 'forumengine/hot_topics_template.html', context=context)


class UserCreate(ObjectCreateMixin, View):
    model = ForumUser
    model_form = UserForm
    template = 'forumengine/user_sign_up_form.html'

    def post(self, request):
        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            password = request.POST.get('password', False)
            new_object = bound_form.save()
            ForumUser.set_password(new_object, password)
            new_object.save()

            return redirect('category_list_view')
        return render(request, self.template, context={'form': bound_form})


class UserDetail(View):

    def get(self, request, id):
        obj = get_object_or_404(ForumUser, id=id)
        return render(request, 'forumengine/user_detail_template.html', context={
            'user': obj,
            'admin_object': obj,
            'detail': True}
                      )


class UserUpdate(LoginRequiredMixin, View):
    model = ForumUser
    model_form = UserForm
    template = 'forumengine/user_update_form.html'
    raise_exception = True

    def get(self, request, id):
        obj = get_object_or_404(ForumUser, id=id)
        bound_form = self.model_form(instance=obj)

        user = ForumUser.objects.get(username=request.user.username)
        if user == obj:
            return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})
        else:
            raise PermissionDenied


def post(self, request, id):
    obj = self.model.objects.get(id=id)
    bound_form = self.model_form(request.POST, instance=obj)

    if bound_form.is_valid():
        new_obj = bound_form.save()
        ps = request.POST.get('password')
        new_obj.set_password(ps)
        new_obj.save()
        return redirect(new_obj)
    return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})


class MessageUpdate(LoginRequiredMixin, View):
    model = Message
    model_form = MessageForm
    template = 'forumengine/message_update_form.html'
    raise_exception = True

    def get(self, request, message_id):
        user = ForumUser.objects.get(username=request.user.username)
        message = Message.objects.get(message_id=message_id)
        bound_form = self.model_form(instance=message)

        if message.author == user or user.is_staff:
            return render(request, self.template, context={'form': bound_form, 'message': message, 'user': user})

        else:
            return redirect('topic_detail_view', slug=message.topic.slug)

    def post(self, request, message_id):
        message = self.model.objects.get(message_id=message_id)
        bound_form = self.model_form(request.POST, instance=message)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj.topic)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): message})


class Statistics(View):
    def get(self, request):
        users_count = ForumUser.objects.all().count()
        topics_count = Topic.objects.all().count()
        messages_count = Message.objects.all().count()
        rating_count = Message.objects.all().aggregate(Sum('rating'))
        date_of_create = datetime.datetime.now() - datetime.datetime.strptime('2018 10 15', '%Y %m %d')

        max_rating = ForumUser.objects.all().aggregate(Max('rating'))['rating__max']
        best_user = ForumUser.objects.get(rating=max_rating)
        msg_written = Message.objects.filter(author=best_user).count()
        topics_created = Topic.objects.filter(author=best_user).count()

        max_rating_topic = Topic.objects.all().aggregate(Max('rating'))['rating__max']
        best_topic = Topic.objects.get(rating=max_rating_topic)
        msg_written_topic = Message.objects.filter(topic=best_topic).count()
        best_topic_lifetime = timezone.now()- best_topic.date_of_pub

        max_rating_message = Message.objects.all().aggregate(Max('rating'))['rating__max']
        best_message = Message.objects.get(rating=max_rating_message)
        best_message_lifetime = timezone.now()- best_message.date_of_pub

        context = {
            'users_count': users_count,
            'topics_count': topics_count,
            'messages_count': messages_count,
            'rating_count': rating_count['rating__sum'],
            'date_of_create': date_of_create.days,
            'max_rating': max_rating,
            'best_user': best_user,
            'msg_written': msg_written,
            'topics_created': topics_created,
            'best_topic':best_topic,
            'max_rating_topic':max_rating_topic,
            'msg_written_topic':msg_written_topic,
            'best_topic_lifetime':best_topic_lifetime.days,
            'max_rating_message':max_rating_message,
            'best_message':best_message.body,
            'best_message_lifetime':best_message_lifetime.days,
            "best_message_author": best_message.author
        }
        return render(request, 'forumengine/statistics_template.html', context=context)


def users_list(request):
    users = ForumUser.objects.order_by('-rating')
    context = {
        'users': users,
        'user': None
    }
    if request.user.is_authenticated:
        user = ForumUser.objects.get(username=request.user.username)
        context['user'] = user
    return render(request, 'forumengine/users_list_template.html', context=context)


def category_list(request):
    context = {
        'category_list': Category.objects.all(),
        'user': None
    }
    if request.user.is_authenticated:
        user = ForumUser.objects.get(username=request.user.username)
        context['user'] = user
    return render(request, 'forumengine/index.html', context=context)


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'forumengine/user_sign_in_form.html')
    else:
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('category_list_view')
        else:
            return render(request, 'forumengine/user_sign_in_form.html')


def logout_view(request):
    logout(request)
    return redirect('category_list_view')


def delete_message(request, message_id):
    msg = Message.objects.get(message_id=message_id)
    topic = Topic.objects.get(topic_id=msg.topic.topic_id)
    Message.objects.get(message_id=message_id).delete()

    return redirect('topic_detail_view', slug=topic.slug)


def create_message(request):
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id', False)
        topic = Topic.objects.get(topic_id=topic_id)

        message = Message()
        message.author = ForumUser.objects.get(username=request.user.username)
        message.body = request.POST.get('body', False)
        message.topic = topic
        message.save()

        return redirect('topic_detail_view', slug=topic.slug)


def create_topic(request):
    if request.method == 'POST':
        title = request.POST.get('title', False)
        category_id = request.POST.get('category_id', False)
        cat = Category.objects.get(category_id=category_id)
        user = ForumUser.objects.get(username=request.user.username)
        obj = Topic(title=title, category=cat, author=user)
        obj.save()

        return redirect('topic_detail_view', slug=obj.slug)
    return redirect('category_list_view')
