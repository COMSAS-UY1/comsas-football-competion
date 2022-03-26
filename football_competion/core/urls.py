from django.urls import path, include
from core.views import IndexView, MatchView, ContactView, TeamView, BlogView, InnerBlogView, GalleryView, getMessage

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('match', MatchView.as_view(), name='match'),
    # path('contact', ContactView.as_view(), name='contact'),
    path('contact', getMessage, name='contact'),
    path('teams', TeamView.as_view(), name='team'),
    path('blog', BlogView.as_view(), name='blog'),
    path('post', InnerBlogView.as_view(), name='innerblog'),
    path('gallery', GalleryView.as_view(), name='gallery'),
]
