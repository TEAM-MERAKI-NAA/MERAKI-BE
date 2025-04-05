# from django.contrib import admin
# from .models import News, NewsCategory
# from django.utils.html import mark_safe
# from django.urls import path
# from django.http import HttpResponse

    
# class NewsCategoryInline(admin.TabularInline):
#     model = NewsCategory
#     verbose_name = "Category"
#     verbose_name_plural = "Categories"
#     extra = 1

# class NewsAdmin(admin.ModelAdmin):
#     list_display = ('title', 'short_description', 'status',
#                     'categories', 'user', 'published_date', 'actionfield')
#     list_filter = ('categories', 'status')
#     actions_on_top = False
#     class Media:
#         css = {
#              'all': ('custom.css',)
#         }
#         js = ('custom.js',)

#     def actionfield(self, obj):
#         status = obj.status
#         returnhtml = ""
#         if status == 'archived':
#             returnhtml = """<input onclick="location.href=\'{1}/change/\'" type="button" value="Edit" class="waves-button-input">
#             <input rel="{0}" type="button" value="Unarchive" class="waves-button-input archive" name="_unarchive">
#             <input onclick="location.href=\'{1}/delete/\'" type='button' value='Delete' />
#             """.format(obj.pk, obj.pk)
#         else:
#             returnhtml = """<input onclick="location.href=\'{1}/change/\'" type="button" value="Edit" class="waves-button-input">
#             <input rel="{0}" type="button" value="Archive" class="waves-button-input archive" name="_archive">
#             <input onclick="location.href=\'{1}/delete/\'" type='button' value='Delete' />
#             """.format(obj.pk, obj.pk)
#         return mark_safe(
#                 returnhtml
#             )

#     actionfield.allow_tags = True
#     actionfield.short_description = 'Action'


#     def save_model(self, request, obj, form, change):
#         if "_draft" in request.POST:
#             obj.status = 'draft'
#         elif "_publish" in request.POST:
#             obj.status = 'published'
#             obj.published_date
#         elif "_archive" in request.POST:
#             print('sdfsfsdf')
#             obj.status = 'archived'
#         elif "_unarchive" in request.POST:
#             obj.status = 'draft'
#         else:
#             obj.status = 'draft'
#         super(NewsAdmin, self).save_model(request, obj, form, change)

#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path('archive/', self.set_archive)
#         ]
#         return my_urls + urls

#     def set_archive(self, request):
#         id = request.POST.get('id')
#         action = request.POST.get('name')
#         status = 'draft'
#         msg = ''
#         if action == '_archive':
#             status = 'archived'
#             msg = 'News has been Archived Successfully'
#         else:
#             msg = 'News has been Unarchived Successfully'
#         self.model.objects.filter(
#             id = id
#         ).update(status=status)
#         self.message_user(request, msg)
#         return HttpResponse("")

# admin.site.register(News, NewsAdmin)
# admin.site.register(NewsCategory)