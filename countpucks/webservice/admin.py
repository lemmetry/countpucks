from django.contrib import admin
from countpucks.webservice.models import Team, HockeyPlayer, PlayerScores, GoalieScores


class TeamAdmin(admin.ModelAdmin):
    ordering = ['team_name']


class TeamListFilter(admin.SimpleListFilter):
    title = 'Team'

    parameter_name = 'team'

    def lookups(self, request, model_admin):
        teams = Team.objects.all()
        return [(t.id, t.team_name) for t in teams.order_by('team_name')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(team__exact=self.value())


class HockeyPlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'sweater', 'position', 'team')
    list_filter = (TeamListFilter,)
    search_fields = ['full_name']


admin.site.register(Team, TeamAdmin)
admin.site.register(HockeyPlayer, HockeyPlayerAdmin)
admin.site.register(PlayerScores)
admin.site.register(GoalieScores)