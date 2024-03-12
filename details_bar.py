from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from song_list import ListPlayer
from song_details import SongDetails
from choose_song_core import Chooser


class NestedBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(NestedBoxLayout, self).__init__(**kwargs)
        space = Label(text="", size_hint=(1 / 60, 1))
        self.nested = SongDetails(orientation="vertical", size_hint=(1/7, 1))
        space1 = Label(text="", size_hint=(1 / 60, 1))
        self.list_of_songs = ListPlayer(orientation='vertical', size_hint=(3/7-1/30, 1))
        space2 = Label(text="", size_hint=(1 / 60, 1))
        chooser = Chooser(self.list_of_songs, orientation='vertical', size_hint=(2/7-1/30, 1))
        space3 = Label(text="", size_hint=(1/60, 1))

        self.add_widget(space)
        self.add_widget(self.nested)
        self.add_widget(space1)
        self.add_widget(self.list_of_songs)
        self.add_widget(space2)
        self.add_widget(chooser)
        self.add_widget(space3)

    def update_size(self, width, scale_width=3/7-1/30):
        self.list_of_songs.update_size(width, scale_width=scale_width)

    def details_update(self, instance):
        self.nested.update_data(instance)
