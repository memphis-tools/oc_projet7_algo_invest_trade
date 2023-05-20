class Action:
    def __init__(self, **args):
        self.name = args["name"]
        self.cost = float(args["cost"])
        self.rate = float(args["rate"])
        self.profit = float(self.cost * self.rate)
        self.number = float(args["number"])

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __lt__(self, other_action):
        return self.profit < other_action.profit
    
    def __gt__(self, other_action):
        return self.profit > other_action.profit
    
class ActionOptimized:
    def __init__(self, **args):
        self.name = args["name"]
        self.cost = int(float(args["cost"])*100)
        self.rate = int(float(args["rate"])*100)
        self.profit = int(round(float(self.cost * self.rate),8))
        self.number = args["number"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __lt__(self, other_action):
        return self.profit < other_action.profit
    
    def __gt__(self, other_action):
        return self.profit > other_action.profit
    
