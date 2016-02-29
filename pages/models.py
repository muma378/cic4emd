# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from utils.validators import validate_not_past
from django.template.defaultfilters import default


class Article(models.Model):
	"""possesses basic properties for an article"""
	author = models.ForeignKey(User, verbose_name=u'编辑', on_delete=models.SET_NULL, null=True)
	title = models.CharField(u'标题', max_length=120)
	content = models.TextField(u'内容')
	last_edit = models.DateTimeField(u'修改日期', auto_now=True)
	create_date = models.DateTimeField(u'创建日期', auto_now_add=True)
	
	def __unicode__(self):
		return self.title

class Category(models.Model):
	"""what type an article belongs to"""
	name = models.CharField(u'栏目', max_length=30)
	desc = models.CharField(u'描述', max_length=200, null=True)
	parent = models.ForeignKey('self', null=True, blank=True)
	create_date = models.DateTimeField(u'创建日期', auto_now_add=True)
	
	def __unicode__(self):
		return self.name

class Publishment(models.Model):
	"""contains all elements consisted in an announcement/news/page"""
	PUBLISH_STATE = (
		('unpublished', u'未发布'),
		('published', u'已发布'),
		('to-publish', u'待发布'),
	)
	
	article = models.OneToOneField(Article, verbose_name=u'文章标题', on_delete=models.CASCADE)
	publisher = models.ForeignKey(User, verbose_name=u'发布人', on_delete=models.SET_NULL, null=True)
	category = models.ForeignKey(Category, verbose_name=u'所属类型', on_delete=models.SET_NULL, null=True)
	state = models.CharField(u'发布状态', max_length=15, choices=PUBLISH_STATE, default='unpublished')
	pub_date = models.DateTimeField(u'发布日期', validators=[validate_not_past])
	create_date = models.DateField(u'创建日期', auto_now_add=True)
	
	def __unicode__(self):
		return self.category.__unicode__() + u'-' + self.article.__unicode__()
	

class StaticFile(models.Model):
	"""abstract class stands for files uploaded"""
	url = models.URLField(u'下载地址', editable=False)
	desc = models.CharField(u'描述', max_length=200, null=True)
	
	class Meta:
		abstract = True
		
	def __unicode__(self):
		return self.desc

def user_derectory_path(instance, filename):
	return 'uploads/{0}/{1}'.format(instance.publishment.publisher.id, filename)

# from django.core.files.base import File
# f = open('./media/uploads/uninstall_cad.doc')
class Attachment(StaticFile):
	"""indicates files attached to articles"""
	publishment = models.ForeignKey(Publishment, verbose_name=u'附件', on_delete=models.CASCADE)
	file = models.FileField(upload_to=user_derectory_path, verbose_name=u'上传')
	date_uploaded = models.DateTimeField(u'上传日期', auto_now_add=True)
	
	def __unicode__(self):
		return str(self.id) + '.'

	class Meta:
		verbose_name = u'添加附件'
		verbose_name_plural = u'添加附件'

class Figure(StaticFile):
	"""figures laied in an article"""
	primary = models.BooleanField(u'是否为封面图片', default=False)
	image = models.ImageField(upload_to='images/{%Y}_{%m}_{%d}')
	article = models.ForeignKey(Article, verbose_name=u'所属文章', on_delete=models.CASCADE)
	