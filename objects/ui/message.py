from direct.gui.DirectGuiGlobals import FLAT
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from panda3d.core import TextNode

from objects.ui.action import Action
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


class Message:
    def __init__(self, title, message, player):
        self.title = title
        self.message = message
        self.player = player
        self.UI_message = None

    def display(self):
        self.UI_message = UIMessage(self)


class UIMessage(Panel):
    def __init__(self, message):
        Panel.__init__(self,"Message", frame_size=(size, -size, size, -size), sort=1000)
        self.player = message.player
        self.message = message

        self.UI_title = None
        self.UI_message = None
        self.UI_scrolled_frame = None
        self.UI_close_button = None

        self.player.disable_actions()
        self.player.clock.pause_clock()
        self.UI_title = DirectLabel(text=self.message.title, scale=0.1,
                                 text_font=self.player.font,
                                 pos=(0, 0, .6), text_bg=(0, 0, 0, 1),
                                 text_fg=(1, 1, 1, 1),
                                 relief=None, parent=self.background)
        self.UI_message = DirectLabel(text=self.message.message, scale=0.07,
                                   text_font=self.player.font,
                                   text_bg=(0, 0, 0, 1),
                                   text_fg=(1, 1, 1, 1),
                                   relief=None, text_align=TextNode.ALeft,
                                   text_wordwrap=20)
        self.UI_close_button = CloseAction(self.player, self)
        self.UI_close_button.button.wrtReparentTo(self.background)
        background_bounds = [
            -1,
            1,
            self.UI_close_button.button.getPos()[2] - .07,
            self.UI_title.getPos()[2] + .07,
        ]
        self.background["frameSize"] = background_bounds

        self.UI_scrolled_frame = DirectScrolledFrame(frameSize=[background_bounds[0] * .8,
                                                             background_bounds[1] * .8,
                                                             background_bounds[2] * .6,
                                                             background_bounds[3] * .8],
                                                  sortOrder=1001,
                                                  canvasSize=[background_bounds[0] * .7,
                                                              background_bounds[1] * .7,
                                                              0,
                                                              self.UI_message.getHeight() / 10],
                                                  frameColor=(0, 0, 0, 1),
                                                  autoHideScrollBars=True,
                                                  verticalScroll_relief=FLAT,
                                                  verticalScroll_frameColor=(1, 1, 1, 0.25),
                                                  verticalScroll_thumb_frameColor=(1, 1, 1, 1),
                                                  verticalScroll_thumb_relief=FLAT,
                                                  verticalScroll_incButton_relief=FLAT,
                                                  verticalScroll_incButton_frameColor=(1, 1, 1, 0.25),
                                                  verticalScroll_decButton_frameColor=(1, 1, 1, 0.25),
                                                  verticalScroll_decButton_relief=FLAT, )
        self.UI_message.wrtReparentTo(self.UI_scrolled_frame.getCanvas())
        self.UI_message.setPos(-.7, 0, self.UI_message.getHeight() / 10 - .1)

    def destroy(self):
        self.UI_title.destroy()
        self.UI_message.destroy()
        self.background.destroy()
        self.UI_scrolled_frame.destroy()
        self.UI_close_button.destroy_button()
        self.player.clock.resume_clock()
