from django.contrib import admin
from countpucks.webservice.models import Team, HockeyPlayer, PlayerScores, GoalieScores


class HockeyPlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birthdate', 'sweater', 'position', 'team')
    list_filter = ['team']
    search_fields = ['full_name']


class PlayerScoresAdmin(admin.ModelAdmin):
    list_display = ('get_fullname', 'get_team', 'get_position', 'date')
    list_filter = ['player__team']
    search_fields = ['player__full_name']
    readonly_fields = ['date']


class GoalieScoresAdmin(admin.ModelAdmin):
    list_display = ('get_fullname', 'get_team', 'date')
    list_filter = ['player__team']
    search_fields = ['player__full_name']
    readonly_fields = ['date']    
    

admin.site.register(Team)
admin.site.register(HockeyPlayer, HockeyPlayerAdmin)
admin.site.register(PlayerScores, PlayerScoresAdmin)
admin.site.register(GoalieScores, GoalieScoresAdmin)