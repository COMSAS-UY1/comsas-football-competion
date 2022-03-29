from pyexpat import model
from django.contrib import admin
from core.models import News, GalleryImage, Gallery, Contributor


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'edition']
    search_fields = ['title']


class ContributorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'title', 'website']
    list_filter = ['title']
    search_fields = ['name', 'title']


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'edition']
    search_fields = ['title']
    inlines = [GalleryImageInline]


admin.site.register(News, NewsAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Contributor, ContributorAdmin)
