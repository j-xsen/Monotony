from direct.gui.DirectGuiGlobals import FLAT
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from panda3d.core import TextNode

from objects.ui.UIConstants import UIConstants
from objects.ui.action import Action
from objects.ui.panel import Panel

size = .45


class CloseAction(Action):
    def __init__(self, container):
        Action.__init__(self, "Close")
        self.create_button()
        self.container = container

    def command(self):
        messenger.send("clock_resume")
        messenger.send("inv_enable")
        self.container.destroy()

    def create_button(self):
        Action.create_button(self)
        self.button["clickSound"] = base.loader.loadSfx("art/sounds/close.ogg")
        self.set_pos((0, 0, -.4))
        self.multiply_scale(0.6)


class Note:
    def __init__(self, title: str, message: str):
        self.title = title
        self.message = message
        self.UI = None

    def display(self):
        self.UI = UIMessage(self)


class UIMessage(Panel):
    scroll_speed = 0.05

    def __init__(self, message: Note):
        Panel.__init__(self, "Message", frame_size=(size, -size, size, -size), sort=1000)
        self.message = message

        self.UI_title = None
        self.UI_message = None
        self.UI_scrolled_frame = None
        self.UI_close_button = None

        self.font = loader.loadFont("Monotony-Regular.ttf")

        messenger.send("disable_actions")
        messenger.send("clock_pause")
        self.UI_title = DirectLabel(text=self.message.title, scale=0.1,
                                    text_font=self.font,
                                    pos=(0, 0, .6), text_bg=UIConstants.COLOR_BLACK,
                                    text_fg=UIConstants.COLOR_ENABLE,
                                    relief=None, parent=self.background)
        self.UI_message = DirectLabel(text=self.message.message, scale=UIConstants.TXT["scale"],
                                      text_font=self.font,
                                      text_bg=UIConstants.COLOR_BLACK,
                                      text_fg=UIConstants.COLOR_ENABLE,
                                      relief=None, text_align=TextNode.ALeft,
                                      text_wordwrap=20)
        self.UI_close_button = CloseAction(self)
        self.UI_close_button.button.wrtReparentTo(self.background)
        background_bounds = [
            -1,
            1,
            self.UI_close_button.button.getPos()[2] - UIConstants.TXT["scale"],
            self.UI_title.getPos()[2] + UIConstants.TXT["scale"],
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
                                                     frameColor=UIConstants.COLOR_BLACK,
                                                     autoHideScrollBars=True,
                                                     verticalScroll_relief=FLAT,
                                                     verticalScroll_frameColor=(1, 1, 1, 0.25),
                                                     verticalScroll_thumb_frameColor=UIConstants.COLOR_ENABLE,
                                                     verticalScroll_thumb_relief=FLAT,
                                                     verticalScroll_incButton_relief=FLAT,
                                                     verticalScroll_incButton_frameColor=(1, 1, 1, 0.25),
                                                     verticalScroll_decButton_frameColor=(1, 1, 1, 0.25),
                                                     verticalScroll_decButton_relief=FLAT, )
        self.UI_message.wrtReparentTo(self.UI_scrolled_frame.getCanvas())
        self.UI_message.setPos(-.7, 0, self.UI_message.getHeight() / 10 - .1)

        self.accept('wheel_up', self.scroll_up)
        self.accept('wheel_down', self.scroll_down)

    def scroll_up(self):
        self.UI_scrolled_frame.verticalScroll['value'] -= self.scroll_speed

    def scroll_down(self):
        self.UI_scrolled_frame.verticalScroll['value'] += self.scroll_speed

    def destroy(self):
        self.ignore_all()
        self.UI_title.destroy()
        self.UI_message.destroy()
        self.background.destroy()
        self.UI_scrolled_frame.destroy()
        self.UI_close_button.destroy_button()
