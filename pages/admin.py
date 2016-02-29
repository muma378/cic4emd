# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

from .models import Publishment, Category, Article
from pages.models import Attachment
from cic4emd.admin import admin_site


class ExistedForeignKeyListFilter(admin.RelatedFieldListFilter):
    title = _('display existed foreign keys only')
    
    @property
    def include_empty_choice(self):
        return False
    
    def choices(self, cl):
        yield {
            'selected': self.lookup_val is None and not self.lookup_val_isnull,
            'query_string': cl.get_query_string({},
                [self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All'),
        }
        for pk_val, val in self.lookup_choices:
            if cl.queryset.filter(**{self.field.name:pk_val}).exists():
                yield {
                       'selected': self.lookup_val == smart_text(pk_val),
                       'query_string': cl.get_query_string({
                            self.lookup_kwarg: pk_val,
                            }, [self.lookup_kwarg_isnull]),
                       'display': val,
                       }


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1


@admin.register(Publishment, site=admin_site)
class PublishmentAdmin(admin.ModelAdmin):
    model = Publishment
    date_hierarchy = 'pub_date'
    fieldsets = (
        (u'编辑文章', {
            'classes': ('wide', ),
            'fields': ('article', )}),
        (u'发布设置', {
            'classes': ('collapse', 'extrapretty' ),
            'fields': ('category', 'state', 'pub_date'),
                }),
        )
    inlines = [AttachmentInline, ]
    list_display = ('article', 'article_author', 'publisher', 'category', 'state', 'pub_date')
    list_filter = (
                   ('category', ExistedForeignKeyListFilter),
                   'state',
                   )
#     list_editable = ('state', )
    
    class Media:
        css = {'all':('css/publishment.css', ),}
#         js = ('js/collapse.js', )
         
    def article_author(self, obj):
        return obj.article.author
    
    def article_content(self, obj):
        return obj.article.content
    
    article_author.short_description = u'编辑'
    article_content.short_name = u'内容'
    
# @admin.register(Article, site=admin_site)
# class ArticleInline(admin.ModelAdmin):
#     inlines = [AttachmentInline]
    
     