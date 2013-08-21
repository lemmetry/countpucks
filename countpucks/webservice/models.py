# Create your models here.
from django.db import models


class Team(models.Model):
    team_name = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.team_name


class HockeyPlayer(models.Model):
    nhl_url = models.URLField(verbose_name='NHL Url', max_length=100)
    full_name = models.CharField(max_length=100)
    sweater = models.CharField(max_length=3, blank=True)
    position = models.CharField(max_length=50)
    team = models.ForeignKey(Team)
    birthdate = models.CharField(max_length=30)

    def __unicode__(self):
        return '%s %s %s %s' % (self.full_name, self.sweater, self.position, self.team)


class PlayerScores(models.Model):
    player = models.ForeignKey(HockeyPlayer)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date of the record')
    GP = models.CharField(max_length=5, verbose_name='Games played')
    G = models.CharField(max_length=5, verbose_name='Goals')
    A = models.CharField(max_length=5, verbose_name='Assists')
    P = models.CharField(max_length=5, verbose_name='Points')
    PlusMinus = models.CharField(max_length=5, verbose_name='+/-')
    PIM = models.CharField(max_length=5, verbose_name='Penalties in minutes')
    PP = models.CharField(max_length=5, verbose_name='Power play goals')
    SH = models.CharField(max_length=5, verbose_name='Short-handed goals')
    GWG = models.CharField(max_length=5, verbose_name='Game winning goals')
    S = models.CharField(max_length=5, verbose_name='Shots on goal')
    hits = models.CharField(max_length=5, verbose_name='Hits')
    BkS = models.CharField(max_length=5, verbose_name='Blocked shots')
    GvA = models.CharField(max_length=5, verbose_name='Giveaways')
    TkA = models.CharField(max_length=5, verbose_name='Takeaways')
    TOIg = models.CharField(max_length=5, verbose_name='Time on ice per game')

    class Meta:
        verbose_name_plural = 'Player scores'

    def __unicode__(self):
        return '%s %s %s' % (self.player.full_name, self.player.sweater, self.player.team)


class GoalieScores(models.Model):
    player = models.ForeignKey(HockeyPlayer)
    date = models.DateField(auto_now_add=True)
    GP = models.CharField(max_length=5, verbose_name='Games played')
    GS = models.CharField(max_length=5, verbose_name='Games started')
    W = models.CharField(max_length=5, verbose_name='Wins')
    L = models.CharField(max_length=5, verbose_name='Losses')
    OT = models.CharField(max_length=5, verbose_name='Overtime or shootout losses')
    GA = models.CharField(max_length=5, verbose_name='Goals against')
    SA = models.CharField(max_length=5, verbose_name='Shots against')
    Sv = models.CharField(max_length=5, verbose_name='Saves')
    SvPercentage = models.CharField(max_length=5, verbose_name='Save percentage')
    GAA = models.CharField(max_length=5, verbose_name='Goals against average')
    SO = models.CharField(max_length=5, verbose_name='Shutouts')
    MIN = models.CharField(max_length=5, verbose_name='Minutes on ice')

    class Meta:
        verbose_name_plural = 'Goalie scores'