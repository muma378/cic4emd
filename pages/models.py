# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from utils.validators import validate_not_past


class Article(models.Model):
	"""possesses basic properties for an article"""
	title = models.CharField(u'标题', max_length=120)
	author = models.ForeignKey(User, verbose_name=u'编辑', on_delete=models.SET_NULL, null=True, blank=True)
	content = models.TextField(u'内容')
	last_edit = models.DateTimeField(u'修改日期', auto_now=True)
	create_date = models.DateTimeField(u'创建日期', auto_now_add=True)
	
	def __unicode__(self):
		return self.title
	
	class Meta:
		verbose_name = u'文章'
		verbose_name_plural = u'文章'

class Category(models.Model):
	"""what type an article belongs to"""
	name = models.CharField(u'名称', max_length=30)
	abbr = models.CharField(u'缩写', max_length=20, unique=True, help_text=u"栏目拼音或英文的首字母组合，只会出现在url中")
	desc = models.CharField(u'描述', max_length=200, null=True, blank=True)
	parent = models.ForeignKey('self', verbose_name=u'上级栏目', null=True, blank=True, help_text=u"将会决定在导航栏中哪个栏目里展示，如果想作为顶级栏目可以不设置")
	display_order = models.	IntegerField(u'展示顺序', help_text=u"在导航栏中的展示顺序，如果不希望展示在导航栏中，可设该值为负数")	# not displayed in navigation if the value was negative
	create_date = models.DateTimeField(u'创建日期', auto_now_add=True)
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		verbose_name = u'栏目'
		verbose_name_plural = u'栏目'
		# unique_together = (('parent', 'display_order'), )

	def get_url(self):
		return "/pages/%s" % self.abbr


class Publishment(models.Model):
	"""contains all elements consisted in an ---/news/page"""
	PUBLISH_STATE = (
		('unpublished', u'未发布'),
		('published', u'已发布'),
		('to-publish', u'待发布'),
	)
	
	article 	= models.OneToOneField(Article, verbose_name=u'文章标题', on_delete=models.CASCADE)
	publisher 	= models.ForeignKey(User, verbose_name=u'发布人', on_delete=models.SET_NULL, null=True)
	category 	= models.ForeignKey(Category, verbose_name=u'所属栏目', on_delete=models.SET_NULL, null=True)
	state 		= models.CharField(u'发布状态', max_length=15, choices=PUBLISH_STATE, default='unpublished')
	pub_date 	= models.DateTimeField(u'发布日期', validators=[], default=timezone.now)
	create_date = models.DateField(u'创建日期', auto_now_add=True)
	broadcast	= models.BooleanField(u'显示在中心动态中', default=True)
	
	class Meta:
		verbose_name = u'发布'
		verbose_name_plural = u'发布'


	def __unicode__(self):
		return self.category.__unicode__() + u'-' + self.article.__unicode__()
	
	def get_url(self):
		return "/pages/%s/%d" % (self.category.abbr, self.pk)


def user_uploads_path(instance, filename):
# 	if hasattr(instance, "uploaded_by"):
	return 'uploads/{0}/{1}'.format(instance.uploaded_by.id, filename)
# 	else:
# 		return 'uploads/temp/{0}'.format(filename)

def user_derectory_path(instance, filename):
	return 'uploads/{0}/{1}'.format(instance.uploaded_by.id, filename)


class MediaFile(models.Model):
	article = models.ForeignKey(Article, verbose_name=u'所属文章', null=True, blank=True, on_delete=models.CASCADE)	#assigned latter
	uploaded_by = models.ForeignKey(User, verbose_name=u'上传者', on_delete=models.CASCADE)
	date_uploaded = models.DateTimeField(u'上传日期', auto_now_add=True)
	
	class Meta:
		abstract = True

# from django.core.files.base import File
# f = open('./media/uploads/uninstall_cad.doc')
class Attachment(MediaFile):
	"""indicates files attached to articles"""
	desc = models.CharField(u'描述', max_length=200, null=True)
	file = models.FileField(upload_to=user_uploads_path, verbose_name=u'文件')
	
	def __unicode__(self):
		return unicode(self.id) + '.' + self.desc
	
	class Meta:
		verbose_name = u'添加附件'
		verbose_name_plural = u'添加附件'
		

def user_images_path(instance, filename):
	return 'images/{0}/{1}'.format(instance.uploaded_by.id, filename)
	
class Figure(MediaFile):
	"""figures laied in an article"""
	primary = models.BooleanField(u'是否为封面图片', default=False)
	image = models.ImageField(upload_to=user_images_path, verbose_name=u'图片')


class Carousel(models.Model):
	"""images displayed in the carousel module of the index page"""
	desc  = models.CharField(u"描述", max_length=200, null=True)
	image = models.ImageField(upload_to=user_images_path, verbose_name=u"图片")
	publishment = models.ForeignKey(Publishment, verbose_name=u"链接文章")
	uploaded_by = models.ForeignKey(User, verbose_name=u'上传者', on_delete=models.CASCADE)
	date_uploaded = models.DateTimeField(u'上传日期', auto_now_add=True)

	class Meta:
		verbose_name = u'首页图片'
		verbose_name_plural = u'首页图片'
	
	"{{ MEDIA_PREFIX }}{{ carousel.image }}"