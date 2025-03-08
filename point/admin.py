from django.contrib import admin
from .models import AllocatedPoint, Point
from django import forms
from django.db import models
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import mark_safe
from django.contrib import messages

    
class AllocatedPointAdmin(admin.ModelAdmin):
    list_display = ('title', 'allocated_point', 'actionfield')
    actions_on_top = False
    verbose_name = "Allocated Point"
    verbose_name_plural = "Allocated Points"
    class Media:
        css = {
             'all': ('custom.css',)
        }
        js = ('custom.js',)


    def actionfield(self, obj):
        returnhtml = """
            <button onclick="location.href=\'{1}/change/\'" type="button" value="Edit" class="tooltip waves-button-input el-button el-button--primary el-button--small">
            <i class="el-icon-edit"></i>
             <span class="tooltiptext">Edit</span>
             </button>
            """.format(obj.pk, obj.pk)
        return mark_safe(
                returnhtml
            )

    actionfield.allow_tags = True
    actionfield.short_description = 'Action'

    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         if 'title' in form.changed_data:
    #             allocatedPointObj = AllocatedPoint.objects.filter(title=form.cleaned_data['title'])
    #             if allocatedPointObj:
    #                 msg = "Points has already been allocated for {}".format(form.cleaned_data['title'])
    #                 messages.error(request, msg)
    #                 return
    #     print('sdfsdfsdf')
    #     super(AllocatedPointAdmin, self).save_model(request, obj, form, change)

    
admin.site.register(AllocatedPoint, AllocatedPointAdmin)

class PointAdmin(admin.ModelAdmin):
    verbose_name = "Point"
    verbose_name_plural = "Points"
    list_display = ('user', 'title','points_earned','created_at')
    actions_on_top = False
    class Media:
        css = {
             'all': ('custom.css',)
        }
        js = ('custom.js',)
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False

    
admin.site.register(Point, PointAdmin)