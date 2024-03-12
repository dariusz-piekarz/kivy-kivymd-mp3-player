from pathlib import Path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from choose_song_layout import ChooserButtons
import os
from shared import Shared

path = str(Path(__file__).parent)


def check_extension(file_path):
    _, file_extension = os.path.splitext(file_path)
    if any([file_extension == target_extension for target_extension in ('.mp3', '.wav', '.ogg', '.wma', '.flac')]):
        return True
    else:
        return False


class Chooser(BoxLayout):
    def __init__(self, object, **kwargs):
        super(Chooser, self).__init__(**kwargs)
        path = r"C:\Users\DXD\Desktop\Moje\Muzyka"
        self.chooser = FileChooserListView(path=path,
                                           size_hint=(1, 13/15))
        Shared.folder_path = path
        space = Label(text="", size_hint=(1, 1/15))
        buttons = ChooserButtons(object, orientation='horizontal', size_hint=(1, 1/15))

        self.chooser.bind(on_submit=self.pass_path)
        self.chooser.bind(path=self.folder_path)

        self.add_widget(self.chooser)
        self.add_widget(space)
        self.add_widget(buttons)

    def pass_path(self, instance, selection, touch):
        if selection:
            if check_extension(selection[0]):
                Shared.temp = selection[0]

    def folder_path(self, instance, value):
        Shared.folder_path = value
