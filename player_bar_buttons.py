from kivymd.uix.slider import MDSlider
from kivymd.uix.button.button import MDIconButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

from pandas import DataFrame
from os import environ

from button_icon import UpdateIcon
from shared import Shared
from song_tools import convert_time


environ['KIVY_AUDIO'] = 'ffpyplayer'


class Buttons(BoxLayout):
    volume_value = 100
    audio = None
    list_loop = False
    song_loop = False
    playing = False
    paused_pos = 0
    iterator = 0
    current_time = 0.0
    dt = 0.0

    def __init__(self, **kwargs):
        super(Buttons, self).__init__(**kwargs)

        self.play_button = UpdateIcon(['play', 'pause'],
                                      "48sp",
                                      action=self.play_pause,
                                      orientation='horizontal',
                                      size_hint=(1/11, 1))
        next_button = MDIconButton(icon='skip-next', icon_size="48sp", size_hint=(1/11, 1))

        prev_button = MDIconButton(icon='skip-previous', icon_size="48sp", size_hint=(1/11, 1))

        self.sound_icon = UpdateIcon(['volume-high', 'volume-mute', 'volume-low', 'volume-medium'],
                                     "48sp",
                                     None,
                                     self.volume_level_button_slider,
                                     None,
                                     orientation='horizontal',
                                     size_hint=(1/11, 1))

        repeat = UpdateIcon(['repeat', 'repeat', 'repeat-once'],
                            "48sp",
                            ['grey', 'white', 'white'],
                            action=self.repeat,
                            orientation='horizontal',
                            size_hint=(1/11, 1))

        self.slider = MDSlider(min=0,
                               max=100,
                               value=self.volume_value,
                               size_hint=(3 / 11, 1),
                               hint=True,
                               color='white',
                               thumb_color_active="white",
                               thumb_color_inactive="white")

        prev_label_left = Label(text="", size_hint=(1/11, 1))
        next_label_right = Label(text="", size_hint=(1/11, 1))

        self.slider.bind(value=lambda instance, value: self.vol(instance, value))
        next_button.bind(on_release=self.next)
        prev_button.bind(on_release=self.prev)

        Shared.slider_change = self.jump_to
        Shared.clear_music_data = self.clear

        self.add_widget(next_label_right)
        self.add_widget(prev_button)
        self.add_widget(self.play_button)
        self.add_widget(next_button)
        self.add_widget(repeat)
        self.add_widget(prev_label_left)
        self.add_widget(self.sound_icon)
        self.add_widget(self.slider)

    def vol(self, instance, value):
        self.sound_icon.update_icon_slider(instance, value)
        if self.audio:
            self.audio.volume = value / 100.0

    def volume_level_button_slider(self, i, args=None):
        volume_val = (90, 0, 30, 60)
        self.slider.value = volume_val[i]
        if self.audio:
            self.audio.volume = volume_val[i] / 100

    def play_pause(self, iterator, instance):
        if len(Shared.fields) > 0:
            path = Shared.fields.at[Shared.current_choice, "Path"]

            if self.audio is None:
                Shared.update_details_data(instance)
                self.audio = SoundLoader.load(path)
                Shared.get_total_length(convert_time(self.audio.length))
                Shared.max_slider_value(self.audio.length)
                self.audio.volume = self.slider.value / 100
                self.audio.loop = self.song_loop

            self.audio.bind(on_stop=self.on_stop)

            if self.playing:
                self.paused_pos = self.audio.get_pos() if self.audio.state == 'play' else 0
                self.audio.stop()
                self.playing = False
            else:
                Clock.schedule_interval(self.update_time_label, 0.1)
                self.audio.seek(self.paused_pos)
                self.audio.play()
                self.playing = True
        else:
            self.iterator = 0
            self.play_button.update_icon_image('play', 0)
        self.iterator = iterator // 2

    def next(self, instance):
        self.current_time = 0.0

        if len(Shared.fields) > 0:
            if Shared.current_choice < len(Shared.fields) - 1:
                path = Shared.fields.at[Shared.current_choice + 1, "Path"]
                Shared.current_choice += 1
            else:
                Shared.current_choice = 0
                path = Shared.fields.at[0, "Path"]

            if self.audio is None:
                self.audio = SoundLoader.load(path)
                Shared.update_details_data(instance)
                self.audio.loop = self.song_loop

            else:
 
                self.audio.stop()
                self.audio = SoundLoader.load(path)
                Shared.update_details_data(instance)
                self.audio.volume = self.slider.value / 100

            Shared.get_total_length(convert_time(self.audio.length))
            Shared.max_slider_value(self.audio.length)

            if self.iterator == 0:
                self.audio.play()
                Clock.schedule_interval(self.update_time_label, 0.1)
        self.audio.bind(on_stop=self.on_stop)

    def prev(self, instance):
        self.current_time = 0.0

        if len(Shared.fields) > 0:
            if Shared.current_choice > 0:
                path = Shared.fields.at[Shared.current_choice - 1, "Path"]
                Shared.current_choice -= 1
            else:
                Shared.current_choice = len(Shared.fields) - 1
                path = Shared.fields.at[len(Shared.fields) - 1, "Path"]

            if self.audio is None:
                self.audio = SoundLoader.load(path)
                Shared.update_details_data(instance)
                self.audio.loop = self.song_loop
                self.audio.volume = self.slider.value / 100

            else:
                self.audio.stop()
                self.audio = SoundLoader.load(path)
                Shared.update_details_data(instance)
                self.audio.volume = self.slider.value / 100

            Shared.get_total_length(convert_time(self.audio.length))
            Shared.max_slider_value(self.audio.length)

            if self.iterator == 0:
                self.audio.play()
                Clock.schedule_interval(self.update_time_label, 0.1)
            self.audio.bind(on_stop=self.on_stop)

    def repeat(self, iterator, instance):
        if iterator % 3 == 0:
            self.song_loop = False
            self.list_loop = False
        elif iterator % 3 == 1:
            self.song_loop = False
            self.list_loop = True
        else:
            self.song_loop = True
            self.list_loop = False

    def on_stop(self, instance):

        if round(self.audio.length-self.current_time) < 0.5:
            self.playing = False

        if not self.playing:
            self.current_time = 0.0

            if len(Shared.fields) > 0 and not self.song_loop:

                if Shared.current_choice < len(Shared.fields) - 1:
                    path = Shared.fields.at[Shared.current_choice + 1, "Path"]
                    Shared.current_choice += 1
                    self.audio = SoundLoader.load(path)
                    Shared.update_details_data(instance)
                    self.audio.volume = self.slider.value / 100
                    Shared.get_total_length(convert_time(self.audio.length))
                    Shared.max_slider_value(self.audio.length)
                    self.playing = True
                    self.audio.play()
                    self.audio.bind(on_stop=self.on_stop)
                elif Shared.current_choice == len(Shared.fields) - 1:
                    Shared.current_choice = 0
                    path = Shared.fields.at[0, "Path"]
                    self.audio = SoundLoader.load(path)
                    Shared.update_details_data(instance)
                    self.audio.volume = self.slider.value / 100
                    Shared.get_total_length(convert_time(self.audio.length))
                    Shared.max_slider_value(self.audio.length)
                    if self.list_loop:
                        self.playing = True
                        self.audio.play()
                    else:
                        self.play_button.update_icon_image('play', 0)
                        self.paused_pos = 0
                        self.dt = 0.0
                        self.playing = False
                        Shared.pg_bar_clear()
                        Shared.timer_beginning(convert_time(self.audio.length))
                    self.audio.bind(on_stop=self.on_stop)
            elif len(Shared.fields) > 0 and self.song_loop:
                self.playing = True
                Shared.update_details_data(instance)
                self.audio.volume = self.slider.value / 100
                Shared.get_total_length(convert_time(self.audio.length))
                Shared.max_slider_value(self.audio.length)
                self.audio.play()
                self.audio.bind(on_stop=self.on_stop)
                
                
    

    def update_time_label(self, dt):

        if self.audio.state == 'play':
            self.current_time = self.audio.get_pos()
        else:
            self.paused_pos = Shared.slider_pos()
            self.current_time = self.paused_pos
        Shared.update_current_pos(convert_time(self.current_time))
        Shared.slider_val_update(self.current_time)

    def jump_to(self, value):
        if self.audio:
            self.current_time = value
            self.audio.seek(float(value))

    def clear(self):
        Clock.unschedule(self.update_time_label)
        self.current_time = 0
        if self.playing:
            self.audio.stop()
        self.audio = None
        self.playing = False
        self.volume_value = 100
        self.paused_pos = 0
        self.dt = 0.0
        Shared.temp = str()
        Shared.index = 0
        Shared.current_choice = 0
        Shared.fields = DataFrame(columns=['Path', 'Title', 'Author', 'Album'])
        Shared.index = 0
        Shared.temp = []
        Shared.tp = dict({})
        self.play_button.update_icon_image('play', 0)
