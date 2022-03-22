from django.urls import path, include
from core.views import IndexView, MatchView

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('match', MatchView.as_view(), name='macth'),
]
