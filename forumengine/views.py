from django.views.generic import View
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from forumengine.models import *
from forumengine.utils import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse


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

    context = {
        'topic': obj,
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


def users_list(request):
    users = ForumUser.objects.order_by('-rating')[:10]
    return render(request, 'forumengine/users_list_template.html', context={'users': users})


def category_list(request):
    content = {
        'category_list': Category.objects.all(),
    }

    return render(request, 'forumengine/index.html', context=content)
