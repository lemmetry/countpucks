from django.contrib import admin
from webservice.models import Team, HockeyPlayer, PlayerScores, GoalieScores


admin.site.register(Team)
admin.site.register(HockeyPlayer)
admin.site.register(PlayerScores)
admin.site.register(GoalieScores)