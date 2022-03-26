from django.contrib import admin
from core.models import Edition, Player, Poule, Match, PouleTeam, Team, Goal, News, GalleryFilter, Gallery


class EditionAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "begin_date", "end_date", "programmed",
        "active"
    ]


class PlayerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "surname", "add_date"]


class PouleAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "edition", "add_date"]
    search_fields = ["id", "name"]


class PouleTeamAdmin(admin.ModelAdmin):
    list_display = [
        "id", "team", "poule", "points", "goals", "conceded_goals",
        "goals_average"
    ]
    search_fields = ["team", "poule", "goals_average"]
    list_filter = ["team", "poule"]


class TeamAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "abreviation", "add_date", "logo"]
    list_filter = ["abreviation"]
    search_fields = ["name"]


class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "id", "team1", "team2", "date_to_play", "goal_team1", "goal_team2",
        "edition"
    ]


class GoalAdmin(admin.ModelAdmin):
    list_display = ["id", "player", "match", "goal_type"]

class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    search_fields = ['title']


admin.site.register(Team, TeamAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Edition, EditionAdmin)
admin.site.register(Poule, PouleAdmin)
admin.site.register(PouleTeam, PouleTeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(News, NewsAdmin)
