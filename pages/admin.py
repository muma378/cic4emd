# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin.templatetags.admin_list import date_hierarchy
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text
from django.utils.functional import curry

from .models import Publishment, Category, Article
from .forms import ArticleForm, AttachmentForm
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
    form = AttachmentForm
    fields = ('desc', 'file', 'uploaded_by')
#     readonly_fields = ('uploaded_by', )
    extra = 1
    
    def get_formset(self, request, obj=None, **kwargs):
        initial = []
        if request.method == "GET":
            initial.append({
                    'uploaded_by': request.user,
                })
        formset = super(AttachmentInline, self).get_formset(request, obj, **kwargs)
        formset.__init__ = curry(formset.__init__, initial=initial)
        return formset

class PublishmentInline(admin.StackedInline):
    model = Publishment
    fields = ('category', 'state', 'pub_date')
    template = 'admin/nolabel_stack.html'
    
@admin.register(Article, site=admin_site)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline, PublishmentInline]
    date_hierarchy = 'last_edit'
    fields = ('title', 'author', 'content')
    readonly_fields= ('author', )
    form = ArticleForm
    change_form_template = 'admin/change_richtext_form.html'
    
    list_display = ('title', 'author', 'state', 'last_edit')
    list_filter = (
                    'publishment__state',
                   )
    
    def state(self, obj):
        try:
            if obj.publishment.state == 'published':
                return u'已发布'
            elif obj.publishment.state == 'to-publish':
                return u'待发布'
            else:
                return u'未发布'
        except Publishment.DoesNotExist:
            return u'编辑中'
    
    state.short_description = u'发布状态'
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        admin.ModelAdmin.save_model(self, request, obj, form, change)
    
    # TODO: save uploaded_by as request.user
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if hasattr(instance, 'uploaded_by'):
                instance.uploaded_by = request.user
            instance.save()
        
    def add_view(self, request, form_url='', extra_context=None):
        data = request.GET.copy()
        data['author'] = request.user
        request.GET = data
        return super(ArticleAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)
    
    class Media:
        js = ("asset/js/csrf_protect.js", )
#         pass    

# @admin.register(Publishment, site=admin_site)
class PublishmentAdmin(admin.ModelAdmin):
    model = Publishment
    date_hierarchy = 'pub_date'
    fields = ('article', 'category', 'state', 'pub_date')
    readonly_fields = ('article', )
    list_display = ('article', 'article_author', 'publisher', 'category', 'state', 'pub_date')
    list_filter = (
                   ('category', ExistedForeignKeyListFilter),
                   'state',
                   )
#     list_editable = ('state', )
    
    class Media:
        css = {'all':('asset/css/publishment.css', ),}
         
    def article_author(self, obj):
        return obj.article.author
    
    def article_content(self, obj):
        return obj.article.content
    
    article_author.short_description = u'编辑'
    article_content.short_name = u'内容'
     

@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    date_hierarchy = 'create_date'
    list_display = ('name', 'desc', 'parent', 'display_order', 'create_date')
    list_filter = (
                   ('parent', ExistedForeignKeyListFilter),
                   )
    
    