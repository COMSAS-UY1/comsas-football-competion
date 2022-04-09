from django.contrib import admin
from tournoi.models import Edition, Player, Poule, Match, Team, Goal, TeamMatch


class EditionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "begin_date", "end_date", "status"]


class PlayerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "surname", "add_date"]
    search_fields = ["id", "name", 'surname', 'matricule']
    list_filter = ["team", 'edition', 'top_player']


class PouleAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "edition", "add_date"]
    search_fields = ["id", "name"]


class TeamMatchAdmin(admin.ModelAdmin):
    list_display = ["id", "team1", "team2", "match", "edition"]
    search_fields = [
        "team1",
        'team2',
    ]
    list_filter = ["match", 'edition']


class TeamAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", 'poule', "abreviation", "add_date", "logo", 'victory',
        'points', 'red_cart', 'yellow_cart', 'defeat', 'null'
    ]
    list_filter = ["abreviation", 'points', 'defeat', 'poule']
    search_fields = ["name", 'poule']


class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "id", "date_to_play", "stade_name", "goal_team1", "goal_team2",
        "edition"
    ]


class GoalAdmin(admin.ModelAdmin):
    list_display = ["id", "player", "match", "goal_type"]


admin.site.register(Team, TeamAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Edition, EditionAdmin)
admin.site.register(Poule, PouleAdmin)
admin.site.register(TeamMatch, TeamMatchAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)