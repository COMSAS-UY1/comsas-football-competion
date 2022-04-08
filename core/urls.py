from django.urls import path, include
from core.views import ContactView, DetailNew, GalleryView, ContributorsView, NewsView

app_name = 'core'

urlpatterns = [
    path('gallery', GalleryView.as_view(), name='gallery'),
    path('contributors', ContributorsView.as_view(), name='contributors'),
    path('contact', ContactView.as_view(), name='contact'),
    path('news', NewsView.as_view(), name='news'),
    path('news/<str:canonical_name>-<int:id>',
         DetailNew.as_view(),
         name='post'),
]
