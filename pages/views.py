# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Figure
from .forms import FigureForm
from cic4emd.settings import LISTED_IMAGES_NUM
# Create your views here.
def index(request):
    context = {"links":[u'少数名族事业发展蓝皮书', u'创新平台', u'民族事务数据库'], "news_list":[u'新闻资讯', u'工作简报', u'通知公告']}
    return render(request, "pages/index.html", context)

def browse(request):
    figures = Figure.objects.filter(uploaded_by=request.user).order_by("-date_uploaded")[:LISTED_IMAGES_NUM]
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
