class Player(object):
    def __init__(self, full_name, sweater, team, position, season, GP, G, A,
                 P, PlusMinus, PIM, PP, SH, GWG, S, Hits, BkS, GvA, TkA, TOIg):
        self.full_name = full_name
        self.sweater = sweater
        self.team = team
        self.position = position
        self.season = season
        self.GP = GP
        self.G = G
        self.A = A
        self.P = P
        self.PlusMinus = PlusMinus
        self.PIM = PIM
        self.PP = PP
        self.SH = SH
        self.GWG = GWG
        self.S = S
        self.Hits = Hits
        self.BkS = BkS
        self.GvA = GvA
        self.TkA = TkA
        self.TOIg = TOIg

    def __str__(self):
        return (
            '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (
                self.full_name, self.sweater, self.team, self.position,
                self.season, self.GP, self.G, self.A, self.P, self.PlusMinus,
                self.PIM, self.PP, self.SH, self.GWG, self.S, self.Hits,
                self.BkS, self.GvA, self.TkA, self.TOIg))