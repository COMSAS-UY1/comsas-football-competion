from pyexpat import model
from django.contrib import admin
from core.models import Author, News, GalleryImage, Gallery, Contributor, ContactInfo


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'edition']
    search_fields = ['title']


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']


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


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject', 'email', 'message']
    search_fields = ['name', 'subject']


admin.site.register(News, NewsAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(ContactInfo, ContactAdmin)
admin.site.register(Contributor, ContributorAdmin)
