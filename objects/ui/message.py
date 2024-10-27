from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectGuiGlobals import SUNKEN, RAISED, GROOVE, FLAT
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.showbase.ShowBaseGlobal import render2d
from panda3d.core import TextNode

from objects.locations.action import Action
from objects.ui.panel import Panel

size = .45

class CloseAction(Action):
    def __init__(self, player, container):
        Action.__init__(self, "Close", player)
        self.create_button()
        self.container = container

    def command(self):
        self.player.enable_actions()
        self.container.destroy()

    def create_button(self):
        Action.create_button(self)
        self.set_pos((0, 0, -.4))
        self.multiply_scale(0.6)


class Message(Panel):
    def __init__(self, player, title, message):
        Panel.__init__(self,"Message", frame_size=(size, -size, size, -size), sort=1000)
        player.disable_actions()
        self.title = DirectLabel(text=title, scale=0.1,
                                 text_font=player.font,
                                 pos=(0,0,.6), text_bg=(0, 0, 0, 1),
                                 text_fg=(1, 1, 1, 1),
                                 relief=None,parent=self.background)
        self.message = DirectLabel(text=message, scale=0.07,
                                   text_font=player.font,
                                   text_bg=(0, 0, 0, 1),
                                   text_fg=(1, 1, 1, 1),
                                   relief=None,text_align=TextNode.ALeft,
                                   text_wordwrap=20)
        self.close_button = CloseAction(player, self)
        self.close_button.button.wrtReparentTo(self.background)
        background_bounds = [
            -1,
            1,
            self.close_button.button.getPos()[2]-.07,
            self.title.getPos()[2]+.07,
        ]
        self.background["frameSize"] = background_bounds

        self.scrolled_frame = DirectScrolledFrame(frameSize=[background_bounds[0]*.8,
                                                             background_bounds[1]*.8,
                                                             background_bounds[2]*.6,
                                                             background_bounds[3]*.8],
                                                  sortOrder=1001,
                                                  canvasSize=[background_bounds[0]*.7,
                                                              background_bounds[1]*.7,
                                                              0,
                                                              self.message.getHeight()/10],
                                                  frameColor=(0, 0, 0, 1),
                                                  autoHideScrollBars=True,
                                                  verticalScroll_relief=FLAT,
                                                  verticalScroll_frameColor=(1, 1, 1, 0.25),
                                                  verticalScroll_thumb_frameColor=(1, 1, 1, 1),
                                                  verticalScroll_thumb_relief=FLAT,
                                                  verticalScroll_incButton_relief=FLAT,
                                                  verticalScroll_incButton_frameColor=(1, 1, 1, 0.25),
                                                  verticalScroll_decButton_frameColor=(1, 1, 1, 0.25),
                                                  verticalScroll_decButton_relief=FLAT,)
        self.message.wrtReparentTo(self.scrolled_frame.getCanvas())
        self.message.setPos(-.7, 0, self.message.getHeight()/10-.1)

    def destroy(self):
        self.title.destroy()
        self.message.destroy()
        self.background.destroy()
        self.scrolled_frame.destroy()
        self.close_button.destroy_button()
