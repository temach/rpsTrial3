#! /usr/bin/env python-32
# -*- coding: utf-8 -*-

"""
Resolve Clash of Titans
"""



import pygame
from pygame.locals import *

import time
import random
from maker import Maker
from operators import Operator

from agk.vector2 import Vector2
pygame.init()


screen = pygame.display.set_mode((800, 600))

def debug(msg):
    print
    print "*"*20
    print msg




class ControlPanel(object):
    def __init__(self):
        self.operator = Operator(self)
        self.maker = Maker( self.operator )

        self.active = {}

        self.objects_credits = {}
        self.objects_menu = {}
        self.objects_game = {}
        self.objects_pl1_choose = {}
        self.objects_pl2_choose = {}

        self.cur_player = None  # player object

        self.player1 = None
        self.player2 = None


    def deactivate(self, id_list):
        for a_id in id_list:
            if self.active.has_key( a_id ):
                del self.active[ a_id ]
    def activate(self, some_dict):
        self.active.update( some_dict )

    def manage_event(self, ev):
        for thing in self.active.values():
            thing.receive_event( ev )
    def manage_render(self, screen):
        for thing in self.active.values():
            thing.render( screen )
    def manage_run(self):
        for thing in self.active.values():
            thing.run()



    def setup(self):
        self.objects_menu = self.maker.make_objects_menu()
        self.objects_game = self.maker.make_objects_game()

        self.objects_define_pl1 = self.maker.make_objects_define_pl1()
        self.objects_define_pl2 = self.maker.make_objects_define_pl2()

        self.objects_pl1_choose = self.maker.make_objects_pl1_choose()

        self.activate( self.objects_menu )






clock = pygame.time.Clock()

cp = ControlPanel()
cp.setup()

while True:
    screen.fill((240,240,240))

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        elif event.type==MOUSEMOTION or event.type==MOUSEBUTTONUP or event.type==MOUSEBUTTONDOWN:
            cp.manage_event( event )

        elif event.type == KEYDOWN or event.type==KEYUP:
            if event.key == K_q or event.key==K_ESCAPE:
                exit()
            cp.manage_event( event )


    cp.manage_render( screen )
    cp.manage_run()


    pygame.display.update()






