# Create your models here.
from django.db import models


class Team(models.Model):
    team_name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.team_name


class HockeyPlayer(models.Model):
    full_name = models.CharField(max_length=100)
    sweater = models.CharField(max_length=3)
    position = models.CharField(max_length=50)
    team = models.ForeignKey(Team)

    def __unicode__(self):
        return '%s %s %s %s' % (self.full_name, self.sweater, self.position, self.team)


class PlayerScores(models.Model):
    player = models.ForeignKey(HockeyPlayer)
    date = models.DateField(auto_now_add=True)
    GP = models.IntegerField(max_length=5, verbose_name='Games played')
    G = models.IntegerField(max_length=5, verbose_name='Goals')
    A = models.IntegerField(max_length=5, verbose_name='Assists')
    P = models.IntegerField(max_length=5, verbose_name='Points')
    PlusMinus = models.IntegerField(max_length=5, verbose_name='+/-')
    PIM = models.IntegerField(max_length=5, verbose_name='Penalties in minutes')
    PP = models.IntegerField(max_length=5, verbose_name='Power play goals')
    SH = models.IntegerField(max_length=5, verbose_name='Short-handed goals')
    GWG = models.IntegerField(max_length=5, verbose_name='Game winning goals')
    S = models.IntegerField(max_length=5, verbose_name='Shots on goal')
    hits = models.IntegerField(max_length=5, verbose_name='Hits')
    BkS = models.IntegerField(max_length=5, verbose_name='Blocked shots')
    GvA = models.IntegerField(max_length=5, verbose_name='Giveaways')
    TkA = models.IntegerField(max_length=5, verbose_name='Takeaways')
    TOIg = models.IntegerField(max_length=5, verbose_name='Time on ice per game')

    class Meta:
        verbose_name_plural = 'Player scores'


class GoalieScores(models.Model):
    player = models.ForeignKey(HockeyPlayer)
    date = models.DateField(auto_now_add=True)
    GP = models.IntegerField(max_length=5, verbose_name='Games played')
    GS = models.IntegerField(max_length=5, verbose_name='Games started')
    W = models.IntegerField(max_length=5, verbose_name='Wins')
    L = models.IntegerField(max_length=5, verbose_name='Losses')
    OT = models.IntegerField(max_length=5, verbose_name='Overtime or shootout losses')
    GA = models.IntegerField(max_length=5, verbose_name='Goals against')
    SA = models.IntegerField(max_length=5, verbose_name='Shots against')
    Sv = models.IntegerField(max_length=5, verbose_name='Saves')
    SvPercentage = models.FloatField(max_length=5, verbose_name='Save percentage')
    GAA = models.FloatField(max_length=5, verbose_name='Goals against average')
    SO = models.IntegerField(max_length=5, verbose_name='Shutouts')
    MIN = models.IntegerField(max_length=5, verbose_name='Minutes on ice')

    class Meta:
        verbose_name_plural = 'Goalie scores'