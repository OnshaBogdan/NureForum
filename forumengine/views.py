from django.views.generic import View
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from forumengine.models import *
from django.http import HttpResponse


def category_list(request):
    content = {
        'category_list': Category.objects.all(),
    }

    return render(request, 'forumengine/index.html', context=content)


class CategoryDetail(View):

    def get(self, request, slug):
        obj = get_object_or_404(Category, slug__iexact=slug)
        context = {'category': obj,
                   'topic_list': Topic.objects.filter(category=obj)
                   }
        return render(request, 'forumengine/category_detail_template.html', context=context)


class TopicDetail(View):

    def get(self, request, slug):
        obj = get_object_or_404(Topic, slug__iexact=slug)
        context = {'topic': obj,
                   'message_list': Message.objects.filter(topic=obj)
                   }
        return render(request, 'forumengine/topic_detail_template.html', context=context)
