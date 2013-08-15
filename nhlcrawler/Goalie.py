class Goalie(object):
    def __init__(self, full_name, sweater, team, position, season, GP, GS, W,
                 L, OT, GA, SA, Sv, SvPercentage, GAA, SO, Min):
        self.full_name = full_name
        self.sweater = sweater
        self.team = team
        self.position = position
        self.season = season
        self.GP = GP
        self.GS = GS
        self.W = W
        self.L = L
        self.OT = OT
        self.GA = GA
        self.SA = SA
        self.Sv = Sv
        self.SvPercentage = SvPercentage
        self.GAA = GAA
        self.SO = SO
        self.Min = Min

    def __str__(self):
        return ('%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' %
                (self.full_name, self.sweater, self.team, self.position,
                 self.season, self.GP, self.GS, self.W, self.L, self.OT,
                 self.GA, self.SA, self.Sv, self.SvPercentage, self.GAA,
                 self.SO, self.Min))