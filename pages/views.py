# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Figure, Carousel, Publishment, Attachment, Category
from .forms import FigureForm
from cic4emd import settings
from utils.common import tz_now

# Create your views here.
def index(request):
    carousels = Carousel.objects.all().order_by("-date_uploaded")[:settings.CAROUSEL_IMAGES_NUM]
    news_list = Publishment.objects.exclude(state='unpublished').exclude(broadcast=False).filter(pub_date__lte=tz_now()).order_by("-pub_date")[:settings.NEWS_LISTED_INDEX]

    # only extracts query set to be demonstrated
    cate_queryset = Category.objects.exclude(display_order__lt=0)  
    cate_parents = cate_queryset.filter(parent__isnull=True).order_by("display_order")
    categories = []
    for parent in cate_parents:
        children = cate_queryset.filter(parent=parent)
        categories.append({"parent":parent, "children": children})

    context = {"links":settings.QUICK_LINKS, 
                "news_list":news_list,
                "carousels":carousels,
                "categories": categories}
    return render(request, "pages/index.html", context)

def category_archive(request, category_abbr):
    context = {}
    return render(request, "pages/list.html", context)

def publishment(request, category_abbr, publishment_id):
    content = get_object_or_404(Publishment, pk=publishment_id) # TODO: only published is ought to be seen
    if content.category.abbr != category_abbr:
        raise Http404

    attachments = Attachment.objects.filter(article=content.article)
    context = {"publishment": content, "title": content.article, "attachments": attachments}
    return render(request, "pages/content.html", context)

def browse(request):
    figures = Figure.objects.filter(uploaded_by=request.user).order_by("-date_uploaded")[:settings.LISTED_IMAGES_NUM]
    func_num = request.GET['CKEditorFuncNum']
    context = {"figures": figures, "func_num": func_num}
    return render(request, "pages/images_list.html", context)

def upload(request):
    if request.method == 'POST':
        callback_template = u"<script type='text/javascript'>window.parent.CKEDITOR.tools.callFunction({func_num}, '{file_url}');</script>"
        response = u'上传成功'
        func_num = request.GET['CKEditorFuncNum']
        request.POST['uploaded_by'] = request.user.id
        form = FigureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            file_url = form.instance.image.url
            return HttpResponse(callback_template.format(**locals()))
    # TODO: not sure how to response
    raise Http404
