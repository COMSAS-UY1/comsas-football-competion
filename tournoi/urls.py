from django.urls import path
from tournoi.views import IndexView, MatchView, TeamView

app_name = 'tournoi'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('match', MatchView.as_view(), name='match'),
    path('teams', TeamView.as_view(), name='team'),
]
