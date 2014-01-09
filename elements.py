__all__=["Text", "Button", "Reader", "Form", "FormPrompter"]

import pygame
from agk.vector2 import Vector2
from pygame.locals import *
import textwrap

class ElementBase( pygame.sprite.Sprite ):
    def receive_event(self, ev):
        return
    def render(self, screen):
        return
    def run(self):
        return



class Text( ElementBase ):
    def __init__( self, rect, text, color, font_obj ):
        self.id = id( self )

        self.rect = rect

        self.textRaw = text
        self.fontColor = color
        self.fontObj = font_obj

        self.text_surf = None
        self.text_pos = (True, True)       # (True, True) == then the text will be in the center, Will be determined

        # this is like setup
        self.change_text( self.textRaw, self.text_pos)
        """ End """



    def change_text(self, new_str, reset_pos=(False,False)):  # By default don't re evaluate, don't re center the text.
        self.textRaw = new_str
        self.text_surf = self.fontObj.render( new_str, True, self.fontColor)

        if reset_pos[0]==True:
            x = self.rect.x + (self.rect.size[0]/2.0) - (self.text_surf.get_width()/2.0)
            self.text_pos = (x, self.text_pos[1])
        if reset_pos[1]==True:
            y = self.rect.y + (self.rect.size[1]/2.0) - (self.text_surf.get_height()/2.0)
            self.text_pos = (self.text_pos[0], y)

    def render( self, screen ):
        if self.textRaw!=None:
            screen.blit( self.text_surf, self.text_pos)





class Button( ElementBase ):

    def __init__( self, imgs_list, rect, func, func_vars=None):
        pygame.sprite.Sprite.__init__( self )

        self.id = id( self )
        self.state = "mouseout"   # mouseout, mouseover, mouseclick

        self.rect = rect
        self.func = func     # function object
        self.func_vars = func_vars   # a dict variables

        self.mouseout_img = imgs_list.pop(0)
        self.mouseover_img = imgs_list.pop(0)
        self.mousedown_img = imgs_list.pop(0)


    def run(self):
        if self.state=="mouseclick":
            if self.func!=None:
                if self.func_vars!=None:
                    self.func( self.func_vars )
                else:
                    self.func()
            self.state = "mouseout"


    def receive_event(self, eventmouse):
        if eventmouse.type==MOUSEMOTION:
            if self.rect.collidepoint( eventmouse.pos ):
                if self.state=="mouseout":
                    self.state = "mouseover"
            else:
                self.state = "mouseout"

        elif self.state=="mouseover" and eventmouse.type==MOUSEBUTTONDOWN:
            self.state = "mousedown"

        elif self.state=="mousedown" and eventmouse.type==MOUSEBUTTONUP:
            self.state = "mouseclick"


    def render( self, screen ):
        if self.state=="mouseover": # First draw the border than the inner filling. This way border will be easier to erase.
            screen.blit( self.mouseover_img, self.rect.topleft )
        elif self.state=="mousedown":
            screen.blit( self.mousedown_img, self.rect.topleft)
        else:   # draw as normal
            screen.blit( self.mouseout_img, self.rect.topleft)





class Reader(pygame.Rect,object):

    class ln(object):
        def __init__(self,string,nl,sp):
            self.string = string
            self.nl = nl
            self.sp = sp

    def __init__(self,text,pos,width,fontsize,height=None,font=None,bg=(250,250,250),fgcolor=(0,0,0),hlcolor=(180,180,200),split=True):
        self.id = id(self)
        self._original = text.expandtabs(4).split('\n')
        self.BG = bg
        self.FGCOLOR = fgcolor
        self._line = 0
        self._index = 0
        if not font:
            self._fontname = pygame.font.match_font('mono',1)
            self._font = pygame.font.Font(self._fontname,fontsize)
        elif type(font) == str:
            self._fontname = font
            self._font = pygame.font.Font(font,fontsize)
        self._w,self._h = self._font.size(' ')
        self._fontsize = fontsize
        if not height: pygame.Rect.__init__(self,pos,(width,self._font.get_height()))
        else: pygame.Rect.__init__(self,pos,(width,height))
        self.split = split
        self._splitted = self.splittext()
        self._x,self._y = pos
        self._src = pygame.display.get_surface()
        self._select = self._line,self._index
        self._hlc = hlcolor
        self.HLCOLOR = hlcolor

    def splittext(self):
        nc = self.width / self._w
        out = []
        for e,i in enumerate(self._original):
            a = Reader.ln('',e,0)
            if not i:
                out.append(a)
                continue
            for j in textwrap.wrap(i,nc,drop_whitespace=False) if self.split else [i]:
                out.append(Reader.ln(j,e,a.sp+len(a.string)))
                a = out[-1]
        return out

    @property
    def HLCOLOR(self):
        return self._hlc
    @HLCOLOR.setter
    def HLCOLOR(self,color):
        self._hlsurface = pygame.Surface((self._w,self._h),pygame.SRCALPHA)
        self._hlsurface.fill(color)

    @property
    def POS(self):
        return self._line,self._index

    @property
    def NLINE(self):
        return self._splitted[self._line].nl

    @property
    def LINE(self):
        return self._original[self.NLINE]

    @property
    def WORD(self):
        try:
            s = self._splitted[self._line].sp+self.wrd
            p1 = self.LINE[:s].split(' ')[-1]
            p2 = self.LINE[s:].split(' ')[0]
            if p2: return p1+p2
        except: return None

    @property
    def SELECTION(self):
        p1,p2 = sorted(((self._line,self._index),self._select))
        if p1 != p2:
            selection = [len(i.string) for i in self._splitted[:p2[0]]]
            return '\n'.join(self._original)[sum(selection[:p1[0]]) + self._splitted[p1[0]].nl + p1[1]:sum(selection) + self._splitted[p2[0]].nl + p2[1]]
        return ''

    @property
    def FONTSIZE(self):
        return self._fontsize
    @FONTSIZE.setter
    def FONTSIZE(self,size):
        self._font = pygame.font.Font(self._fontname,size)
        self._fontsize = size
        self._w,self._h = self._font.size(' ')
        self._splitted = self.splittext()
        y = self._y
        h = len(self._splitted) * self._h
        if h > self.height:
            if self._y - self._h < self.bottom - h: self._y = self.bottom - h
        self._y += (self.top - self._y)%self._h
        self.HLCOLOR = self._hlc

    def screen(self):
        clip = self._src.get_clip()
        self._src.set_clip(self.clip(clip))
        try: self._src.fill(self.BG,self)
        except: self._src.blit(self.BG,self)

        start = (self.top - self._y) / self._h
        end = (self.bottom - self._y) / self._h + 1

        p1,p2 = sorted(((self._line,self._index),self._select))

        y = self._y + start * self._h
        for py,i in enumerate(self._splitted[start:end],start):
            x = self._x
            for px,j in enumerate(i.string):
                if p1<=(py,px)<p2:
                    self._src.blit(self._hlsurface,(x,y))
                    self._src.blit(self._font.render(j,1,self.FGCOLOR),(x,y))
                else:
                    self._src.blit(self._font.render(j,1,self.FGCOLOR),(x,y))
                x += self._w
            y += self._h
        self._src.set_clip(clip)

    def run(self):
        return

    def render(self, screen):
        self.screen()
        pygame.display.update(self)


    def receive_event(self,ev):

        line,index = self._line,self._index
        ctrl = pygame.key.get_pressed()
        ctrl = ctrl[pygame.K_RCTRL] | ctrl[pygame.K_LCTRL]

        def scrollup(n):
            y = self._y
            if self._y + self._h * n > self.top: self._y = self.top
            else: self._y += self._h * n

        def scrolldown(n):
            y = self._y
            h = len(self._splitted) * self._h
            if h > self.height:
                if self._y - self._h * n < self.bottom - h: self._y = self.bottom - h
                else: self._y -= self._h * n

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_UP:
                scrollup(1)

            elif ev.key == pygame.K_DOWN:
                scrolldown(1)

            elif ctrl and ev.key == pygame.K_KP_PLUS:
                self.FONTSIZE += 1

            elif ctrl and ev.key == pygame.K_KP_MINUS and self._fontsize:
                self.FONTSIZE -= 1

        elif ev.type == pygame.MOUSEBUTTONDOWN and self.collidepoint(ev.pos):
            if ev.button == 1:
                self._line = (ev.pos[1] - self._y) / self._h
                self._index = (ev.pos[0] - self._x) / self._w
                self.wrd = self._index
                if ((ev.pos[0] - self._x) % self._w) > (self._w / 2): self._index += 1
                if self._line > len(self._splitted)-1:
                    self._line = len(self._splitted)-1
                    self._index = len(self._splitted[self._line].string)
                if self._index > len(self._splitted[self._line].string): self._index = len(self._splitted[self._line].string)
                self._select = self._line,self._index

        elif ev.type == pygame.MOUSEBUTTONUP and self.collidepoint(ev.pos):
            if ev.button == 4:
                scrollup(3)
            elif ev.button == 5:
                scrolldown(3)

        elif ev.type == pygame.MOUSEMOTION and ev.buttons[0] and self.collidepoint(ev.pos):
            self._line = (ev.pos[1] - self._y) / self._h
            self._index = (ev.pos[0] - self._x) / self._w
            if ((ev.pos[0] - self._x) % self._w) > (self._w / 2): self._index += 1
            if self._line > len(self._splitted)-1:
                self._line = len(self._splitted)-1
                self._index = len(self._splitted[self._line].string)
            if self._index > len(self._splitted[self._line].string): self._index = len(self._splitted[self._line].string)








class Form(pygame.Rect, object):

    def __init__(self,pos,width,fontsize,height=None,font=None,bg=(250,250,250),fgcolor=(0,0,0),hlcolor=(180,180,200),curscolor=(0xff0000),maxlines=0):
        self.id = id(self)
        if not font: self.FONT = pygame.font.Font(pygame.font.match_font('mono',1),fontsize)
        elif type(font) == str: self.FONT = pygame.font.Font(font,fontsize)
        else: self.FONT = fonts
        self.BG = bg
        self.FGCOLOR = fgcolor
        self.HLCOLOR = hlcolor
        self.CURSCOLOR = curscolor
        self._line = 0
        self._index = 0
        self.MAXLINES = maxlines
        self._splitted = ['']
        if not height: pygame.Rect.__init__(self,pos,(width,self.FONT.get_height()))
        else: pygame.Rect.__init__(self,pos,(width,height))
        self._x,self._y = pos
        self._src = pygame.display.get_surface()
        self._select = self._line,self._index
        self.TAB = 4
        self._adjust()
        self._cursor = True

    @property
    def CURSOR(self):
        return self._cursor
    @CURSOR.setter
    def CURSOR(self,value):
        self._cursor = value

    @property
    def HLCOLOR(self):
        return None
    @HLCOLOR.setter
    def HLCOLOR(self,color):
        self._hlsurface = pygame.Surface((self._w,self._h),pygame.SRCALPHA)
        self._hlsurface.fill(color)

    @property
    def OUTPUT(self):
        return '\n'.join(self._splitted)
    @OUTPUT.setter
    def OUTPUT(self,string):
        self._splitted = string.split('\n')

    @property
    def FONT(self):
        return self._font
    @FONT.setter
    def FONT(self,font):
        self._font = font
        self._w,self._h = self._font.size(' ')

    @property
    def SELECTION(self):
        p1,p2 = sorted(((self._line,self._index),self._select))
        if p1 != p2:
            selection = [len(i) for i in self._splitted[:p2[0]]]
            return self.OUTPUT[sum(selection[:p1[0]]) + p1[0] + p1[1]:sum(selection) + p2[0] + p2[1]:]
        return ''

    def _adjust(self):
        if self._index < len(self._splitted[self._line]):
            rcurs = pygame.Rect(self._x+self._index*self._w,self._y+self._line*self._h,self._w,self._h)
        else:
            rcurs = pygame.Rect(self._x+len(self._splitted[self._line])*self._w,self._y+self._line*self._h,1,self._h)

        self._rcursor = rcurs.clamp(self)
        self._x += self._rcursor.x - rcurs.x
        self._y += self._rcursor.y - rcurs.y

    def screen(self):
        clip = self._src.get_clip()
        self._src.set_clip(self.clip(clip))
        try: self._src.fill(self.BG,self)
        except: self._src.blit(self.BG,self)

        start = (self.top - self._y) / self._h
        end = (self.bottom - self._y) / self._h + 1

        p1,p2 = sorted(((self._line,self._index),self._select))

        y = self._y + start * self._h
        for py,i in enumerate(self._splitted[start:end],start):
            x = self._x
            for px,j in enumerate(i):
                if p1<=(py,px)<p2:
                    self._src.blit(self._hlsurface,(x,y))
                    self._src.blit(self._font.render(j,1,self.FGCOLOR),(x,y))
                else:
                    self._src.blit(self._font.render(j,1,self.FGCOLOR),(x,y))
                x += self._w
            y += self._h
        if self._cursor:
            pygame.draw.line(self._src,self.CURSCOLOR,self._rcursor.topleft,self._rcursor.bottomleft,1)
        self._src.set_clip(clip)


    def run(self):
        return

    def render(self, screen):
        self.screen()
        pygame.display.update(self)

    def receive_event(self,ev):

        line,index = self._line,self._index
        shift = pygame.key.get_pressed()
        shift = shift[pygame.K_RSHIFT]|shift[pygame.K_LSHIFT]

        def clear():
            p1,p2 = sorted(((self._line,self._index),self._select))
            if p1 != p2:
                selection = [len(i) for i in self._splitted[:p2[0]]]
                self.OUTPUT = self.OUTPUT[:sum(selection[:p1[0]]) + p1[0] + p1[1]] + self.OUTPUT[sum(selection[:p2[0]]) + p2[0] + p2[1]:]
                self._select = self._line,self._index = p1

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RIGHT:
                if self._index < len(self._splitted[self._line]):
                    self._index += 1
                elif self._line < len(self._splitted)-1:
                    self._index = 0
                    self._line += 1
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_LEFT:
                if self._index > len(self._splitted[self._line]):
                    self._index = len(self._splitted[self._line])
                if self._index:
                    self._index -= 1
                elif self._line:
                    self._line -= 1
                    self._index = len(self._splitted[self._line])
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_UP:
                if self._line: self._line -= 1
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_DOWN:
                if self._line < len(self._splitted)-1: self._line += 1
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_DELETE:
                if self._select == (self._line,self._index):
                    if self._index > len(self._splitted[self._line]):
                        self._index = len(self._splitted[self._line])
                        self._select = self._line + 1,0
                    else:
                        self._select = self._line,self._index + 1
                clear()

            elif ev.key == pygame.K_END:
                self._index = len(self._splitted[self._line])
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_HOME:
                self._index = 0
                if not pygame.mouse.get_pressed()[0] and not shift and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_BACKSPACE:
                if self._select == (self._line,self._index):
                    if self._index > len(self._splitted[self._line]): self._index = len(self._splitted[self._line])
                    if self._index == 0:
                        if self._line: self._select = self._line - 1,len(self._splitted[self._line - 1])
                    else: self._select = self._line,self._index - 1
                clear()

            elif ev.key == pygame.K_TAB:
                clear()
                sp = self.TAB-self._index%self.TAB
                self._splitted[self._line] = self._splitted[self._line][:self._index] + ' '*sp + self._splitted[self._line][self._index:]
                self._index += sp
                self._select = self._line,self._index

            elif ev.key == pygame.K_RETURN or ev.key == pygame.K_KP_ENTER or ev.unicode == '\n':
                clear()
                if not self.MAXLINES or self.OUTPUT.count('\n') < self.MAXLINES - 1:
                    self._splitted[self._line] = self._splitted[self._line][:self._index] + '\n' + self._splitted[self._line][self._index:]
                    self.OUTPUT = self.OUTPUT
                    self._line += 1
                    self._index = 0
                    self._select = self._line,self._index

            elif ev.unicode:
                clear()
                self._splitted[self._line] = self._splitted[self._line][:self._index] + ev.unicode + self._splitted[self._line][self._index:]
                self._index += 1
                self._select = self._line,self._index

        elif ev.type == pygame.MOUSEBUTTONDOWN and self.collidepoint(ev.pos):
            if ev.button < 3:
                self._line = (ev.pos[1] - self._y) / self._h
                self._index = (ev.pos[0] - self._x) / self._w
                if ((ev.pos[0] - self._x) % self._w) > (self._w / 2): self._index += 1
                if self._line > len(self._splitted)-1:
                    self._line = len(self._splitted)-1
                    self._index = len(self._splitted[self._line])
                if self._index > len(self._splitted[self._line]): self._index = len(self._splitted[self._line])
                if ev.button == 2:
                    self._splitted[self._line] = self._splitted[self._line][:self._index] + self.SELECTION + self._splitted[self._line][self._index:]
                    self.OUTPUT = self.OUTPUT
                    self._index += len(self.SELECTION)

                self._select = self._line,self._index

            elif ev.button == 4:
                y = self._y
                if self._y + self._h*3 > self.top: self._y = self.top
                else: self._y += self._h*3
                self._rcursor.move_ip(0,self._y-y)
                return

            elif ev.button == 5:
                y = self._y
                h = len(self._splitted) * self._h
                if h > self.height:
                    if self._y - self._h*3 < self.bottom - h: self._y = self.bottom - h
                    else: self._y -= self._h*3
                    self._rcursor.move_ip(0,self._y-y)
                return

        elif ev.type == pygame.MOUSEMOTION and ev.buttons[0] and self.collidepoint(ev.pos):
            self._line = (ev.pos[1] - self._y) / self._h
            self._index = (ev.pos[0] - self._x) / self._w
            if ((ev.pos[0] - self._x) % self._w) > (self._w / 2): self._index += 1
            if self._line > len(self._splitted)-1:
                self._line = len(self._splitted)-1
                self._index = len(self._splitted[self._line])
            if self._index > len(self._splitted[self._line]): self._index = len(self._splitted[self._line])

        if (line,index) != (self._line,self._index):
            self._adjust()




class FormPrompter( Button ):
    def __init__(self, imgs_list, rect, func, func_vars, some_form):
        super( FormPrompter, self).__init__(imgs_list, rect, func, func_vars)

        self.form = some_form
        self.form_active = False


    def receive_event(self, ev):
        super( FormPrompter, self).receive_event( ev )

        if self.state=="clicked":
            self.func_vars["user_input"] = self.form.OUTPUT


