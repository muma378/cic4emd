# -*- coding: utf-8 -*-
from django.contrib.admin import sites
from django.contrib.auth import admin, models

class CoInnoCentAdminSite(sites.AdminSite):
    site_header = u'少数名族事业发展协同创新中心'
    title = u'后台管理'
    
admin_site = CoInnoCentAdminSite(name='cic4emd')

admin_site.register(models.Group, admin.GroupAdmin)
admin_site.register(models.User, admin.UserAdmin)