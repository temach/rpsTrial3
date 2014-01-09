

class Player(object):
    def __init__(self, name):
        self.text_name = name     # player name: Artem, Jisu
        self.session_score = 0
        self.current_weapon = None    # None, rock, scissors, paper



def debug(msg):
    print
    print "*"*20
    print msg




class Operator(object):
    def __init__(self, control_panel):
        self.cp = control_panel


    def func_define_player1(self, func_vars):
        self.player1 = Player(func_vars["user_input"])
        self.cp.deactivate( self.cp.objects_define_pl1 )
        self.cp.activate( self.cp.objects_define_pl2 )
        debug("Now: Have defined player one.......  ")

    def func_define_player2(self, func_vars):
        self.player2 = Player(func_vars["user_input"])
        self.cp.deactivate( self.cp.objects_define_pl2 )
        self.cp.activate( self.cp.objects_pl1_choose )
        debug("Now: TWO it is TWO that I have finished defining TWO ")


    def func_start_game(self):
        self.cp.active.clear()
        self.cp.activate( self.cp.objects_game )
        self.cp.activate( self.cp.objects_define_pl1 )
        debug("Now: Game Starting")


    def func_main_menu(self):
        debug("Now: Trying to go to main menu")
