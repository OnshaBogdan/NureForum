from django.views.generic import View
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from forumengine.models import *
from forumengine.utils import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import *


class CategoryDetail(View):

    def get(self, request, slug):
        obj = get_object_or_404(Category, slug__iexact=slug)
        context = {'category': obj,
                   'topic_list': Topic.objects.filter(category=obj)
                   }

        return render(request, 'forumengine/category_detail_template.html', context=context)


def messages_list(request, slug):
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
        'is_paginated': is_paginated
    }

    return render(request, 'forumengine/topic_detail_template.html', context=context)


class TopicDetail(View):

    def get(self, request, slug):
        obj = get_object_or_404(Topic, slug__iexact=slug)
        context = {'topic': obj,
                   'message_list': Message.objects.filter(topic=obj)
                   }
        return render(request, 'forumengine/topic_detail_template.html', context=context)


class UserDetail(View):

    def get(self, request, id):
        obj = get_object_or_404(ForumUser, id=id)
        return render(request, 'forumengine/user_detail_template.html', context={
            'user': obj,
            'admin_object': obj,
            'detail': True}
                      )


class UserCreate(ObjectCreateMixin, View):
    model = ForumUser
    model_form = UserForm
    template = 'forumengine/user_sign_up_form.html'

    def post(self, request):
        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            password = request.POST.get('password', False)
            new_object = bound_form.save()
            User.set_password(new_object, password)
            new_object.save()

            return redirect('category_list_view')
        return render(request, self.template, context={'form': bound_form})





def users_list(request):
    users = ForumUser.objects.order_by('-rating')[:10]
    return render(request, 'forumengine/users_list_template.html', context={'users': users})


def category_list(request):
    content = {
        'category_list': Category.objects.all(),
    }

    return render(request, 'forumengine/index.html', context=content)


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


def create_message(request):
    if request.method == 'POST':
        title = request.POST.get('title', False)
        topic = Topic.objects.get(title=title)

        message = Message()
        message.author = ForumUser.objects.get(username=request.user.username)
        message.body = request.POST.get('body', False)
        message.topic = topic
        message.save()

        return redirect('topic_detail_view', slug=topic.slug)
