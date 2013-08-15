from django.contrib import admin
from countpucks.webservice.models import Team, HockeyPlayer, PlayerScores, GoalieScores


class HockeyPlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'sweater', 'position', 'team')
    list_filter = ['team']
    search_fields = ['full_name']


admin.site.register(Team)
admin.site.register(HockeyPlayer, HockeyPlayerAdmin)
admin.site.register(PlayerScores)
admin.site.register(GoalieScores)