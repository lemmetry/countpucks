from django.contrib import admin
from countpucks.webservice.models import Team, HockeyPlayer, PlayerScores, GoalieScores


class HockeyPlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birthdate', 'sweater', 'position', 'team')
    list_filter = ['team']
    search_fields = ['full_name']


class PlayerScoresAdmin(admin.ModelAdmin):
    readonly_fields = ['date']
    

admin.site.register(Team)
admin.site.register(HockeyPlayer, HockeyPlayerAdmin)
admin.site.register(PlayerScores, PlayerScoresAdmin)
admin.site.register(GoalieScores)