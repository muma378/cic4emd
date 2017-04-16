# -*- coding: utf-8 -*-
import math
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import Figure, Carousel, Publishment, Attachment, Category
from .forms import FigureForm
from cic4emd import settings
from utils.common import tz_now

# Create your views here.
def index(request):
    carousels = Carousel.objects.all().order_by("-date_uploaded")[:settings.CAROUSEL_IMAGES_NUM]
    
    # query once, but used in many times
    pub_queryset = get_broadcast_publishments()
    
    news_list = pub_queryset[:settings.NEWS_LISTED_INDEX]
    
    news_archives_categories = []
    for abbr in settings.NEWS_ARCHIVE_ABBRS:
        try:
            news_archives_categories.append(Category.objects.get(abbr=abbr))
        except ObjectDoesNotExist, e:
            pass
    
    news_archives = []
    for category in news_archives_categories:
        pubs = pub_queryset.filter(category=category).order_by("-pub_date")[:settings.NEWS_ARCHIVE_NUM]
        if pubs:    
        #     try:
        #         cover = pubs.first().article.figure_set.first().image
        #     except AttributeError, e:
        #         cover = settings.PLACEHOLDER_COVER

            news_archives.append({
                "category":category, 
                "publishments": pubs,
                # "cover": cover,
                })

    friendly_links = {
        'links': settings.FRIENDLY_LINKS, 
        'more': settings.MORE_LINKS
        }

    context = {"links":settings.QUICK_LINKS, 
                "news_list":news_list,
                "news_archives": news_archives,
                "carousels":carousels,
                "navigation": get_categories(),
                "friendly_links": friendly_links,
                }
    return render(request, "pages/index.html", context)

# TODO: cache the result, it was called so often
def get_categories():
    # only extracts query set to be demonstrated
    cate_queryset = Category.objects.exclude(display_order__lt=0)

    cate_parents = cate_queryset.filter(parent__isnull=True).order_by("display_order")
    categories = []
    for parent in cate_parents:
        children = cate_queryset.filter(parent=parent)
        categories.append({"parent":parent, "children": children})
    return categories

def get_broadcast_publishments():
    return Publishment.objects.exclude(state='unpublished')\
        .exclude(broadcast=False).filter(pub_date__lte=tz_now()).order_by("-pub_date")

def get_avaible_publishments():
    return Publishment.objects.exclude(state='unpublished')\
        .filter(pub_date__lte=tz_now()).order_by("-pub_date")

def category_archive(request, category_abbr):
    category = get_object_or_404(Category, abbr=category_abbr)
    pub_queryset = get_avaible_publishments()

    if category.parent:     # for categories in top level
        publishments = pub_queryset.filter(category=category)
        # look up related categories
        related = Category.objects.filter(Q(parent=category.parent))
    else:
        publishments = pub_queryset.filter(Q(category__parent=category) | Q(category=category))
        related = Category.objects.filter(parent=category)

    # get info for pagination
    try:
        index = int(request.GET.get('page', 1))
    except ValueError, e:
        raise Http404
    start, end = (index-1)*settings.NEWS_PER_PAGE_NUM, index*settings.NEWS_PER_PAGE_NUM
    
    total = publishments.count()
    if index < 1 or start > total:
        raise Http404

    next, prev = None, None
    if total > end:
        next = index + 1
    if index > 1:
        prev = index - 1

    pages = int( math.ceil( total/float(settings.NEWS_PER_PAGE_NUM) ))
    max_shown = settings.PAGINATION_DISPLAYED
    displayed_range = (max_shown - 1) / 2
    if pages < max_shown:
        displayed_pages = range(1, pages+1)
    elif index <= displayed_range:
        displayed_pages = range(1, max_shown+1)
    elif index >= pages - displayed_range:
        displayed_pages = range(pages-max_shown, pages+1)
    else:
        displayed_pages = range(index-displayed_range, index+displayed_range+1)

    # TODO: disable button if prev or next was none
    pagination = { "index": index, "prev": prev if prev else 1, "next": next if next else pages, "pages": pages, "displayed_pages": displayed_pages}


    context = {"title": category.name,
                "navigation": get_categories(),
                "category": category,
                "publishments": publishments[start:end],
                "subcategories": related,
                "pagination": pagination,
                }
    return render(request, "pages/list.html", context)

def publishment(request, category_abbr, publishment_id):
    content = get_object_or_404(Publishment, pk=publishment_id) # TODO: only published is ought to be seen
    if content.category.abbr != category_abbr:
        raise Http404

    topics = get_avaible_publishments().filter(category__abbr=category_abbr)
    topics_id_list = [ topic.id for topic in topics ]
    topic_index = topics_id_list.index(content.id)
    prev = topics[topic_index-1] if topic_index > 0 else content
    next = topics[topic_index+1] if topic_index < len(topics)-1 else content
    related = {"prev": prev, "next": next}

    attachments = Attachment.objects.filter(article=content.article)
    context = {"publishment": content, 
                "title": content.article, 
                "attachments": attachments,
                "related": related,
                "navigation": get_categories()
                }
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
