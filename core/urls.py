from django.urls import path, include
from core.views import ContactView, GalleryView, ContributorsView, NewsView, InnerBlog

app_name = 'core'

urlpatterns = [
    path('gallery', GalleryView.as_view(), name='gallery'),
    path('contributors', ContributorsView.as_view(), name='contributors'),
    path('contact', ContactView.as_view(), name='contact'),
    path('news', NewsView.as_view(), name='news'),
    path('post', InnerBlog.as_view(), name='post'),
]
