from django.urls import path, include
from core.views import IndexView, MatchView, ContactView, TeamView,  GalleryView, getMessage

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('match', MatchView.as_view(), name='match'),
    path('contact', getMessage, name='contact'),
    path('teams', TeamView.as_view(), name='team'),
    path('gallery', GalleryView.as_view(), name='gallery'),
]
