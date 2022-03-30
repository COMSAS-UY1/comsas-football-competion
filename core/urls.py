from django.urls import path, include
from core.views import ContactView, GalleryView, ContributorsView, BlogView, NewsView

app_name = 'core'

urlpatterns = [
    path('gallery', GalleryView.as_view(), name='gallery'),
    path('contributors', ContributorsView.as_view(), name='contributors'),
    path('contact', ContactView.as_view(), name='contact'),
    path('blog', BlogView.as_view(), name='blog'),
]
