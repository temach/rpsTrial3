__all__=["Maker"]

import pygame
import agk


from elements import Button, Text, Reader, Form, FormPrompter



class Maker(object):
    def __init__(self, operators):
        self.ops = operators

    def make_objects_menu(self):
        objects_menu = {}
        rect = pygame.Rect( (300,100), (100,100))
        out = pygame.image.load("img/start_out.png").convert()
        over = pygame.image.load("img/start_over.png").convert()
        down = pygame.image.load("img/start_down.png").convert()
        b = Button( [out, over, down], rect, self.ops.func_start_game)
        objects_menu[b.id] = b

        return objects_menu


    def make_objects_game(self):
        objects_credits = {}

        """
        rect = pygame.Rect( (300,100), (300,300))
        text = "This is where the game would be played, So the sides would be choosing theur weapons. After they have choosen their names of course."
        f_obj = pygame.font.SysFont("arial", 10)
        t = Text(rect, text, (100,100,210), f_obj)
        objects_credits[t.id] = t
        """

        rect = pygame.Rect( (10,10), (100,100))
        out = pygame.image.load("img/menu_out.png").convert()
        over = pygame.image.load("img/menu_over.png").convert()
        down = pygame.image.load("img/menu_down.png").convert()
        b = Button( [out, over, down], rect, self.ops.func_main_menu)
        objects_credits[b.id] = b

        return objects_credits




    def make_objects_define_pl1(self):
        objects_pl1 = {}

        text = """The first torai, should name him/her/it self, right now."""
        t = Reader(unicode(text.expandtabs(4),'utf8'),(50,40),300,fontsize=15,height=60,font=None,bg=(100,100,100),fgcolor=(255,255,255),hlcolor=(255,10,150,100),split=False)
        objects_pl1[ t.id ] = t


        f = Form((10,200),200,fontsize=12,height=24,bg=(100,100,100),fgcolor=(250,250,250),hlcolor=(250,190,150,50),curscolor=(190,0,10), maxlines=1)
        f.OUTPUT = unicode("""Name Here""","utf8")
        objects_pl1[ f.id ] = f


        out = pygame.image.load("img/YES.png").convert()
        over = pygame.image.load("img/YES.png").convert()
        down = pygame.image.load("img/YES1.png").convert()
        rect = pygame.Rect((400,200), down.get_size())
        fm = FormPrompter( [out,over,down], rect, self.ops.func_define_player1, {"user_input":""}, f )    # the final lonely "f" here referes to the Form object (defined above) that would be used to grab the user's input
        objects_pl1[ fm.id ] = fm

        return objects_pl1


    def make_objects_define_pl2(self):
        objects_pl1 = {}

        text = """Now its time to choose player Two"""
        t = Reader(unicode(text.expandtabs(4),'utf8'),(20,20),660,15,height=360,font=None,bg=(100,100,100),fgcolor=(255,255,255),hlcolor=(255,10,150,100),split=False)
        objects_pl1[ t.id ] = t


        f = Form((10,150),660,fontsize=12,height=80,bg=(100,100,100),fgcolor=(250,250,250),hlcolor=(250,190,150,50),curscolor=(190,0,10), maxlines=1)
        f.OUTPUT = unicode("""Enter name here""","utf8")
        objects_pl1[ f.id ] = f


        out = pygame.image.load("img/YES.png").convert()
        over = pygame.image.load("img/YES.png").convert()
        down = pygame.image.load("img/YES1.png").convert()
        rect = pygame.Rect((700,10), down.get_size())
        fm = FormPrompter( [out,over,down], rect, self.ops.func_define_player2, {"user_input":""}, f )    # the final lonely "f" here referes to the Form above that would be used to grab the user's input
        objects_pl1[ fm.id ] = fm

        return objects_pl1


    def make_objects_pl1_choose(self):
        objects_pl1 = {}

        rect = pygame.Rect( (300,100), (300,300))
        text = "This widget is the options for weapons the player one can choose from."
        f_obj = pygame.font.SysFont("arial", 10)
        t = Text(rect, text, (100,100,210), f_obj)
        objects_pl1[t.id] = t

        return objects_pl1
