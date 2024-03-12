from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.slider import MDSlider
from kivy.uix.label import Label

from player_bar_buttons import Buttons
from timers import Timers
from shared import Shared


class PlayerBar(BoxLayout):
    def __init__(self, **kwargs):
        super(PlayerBar, self).__init__(**kwargs)
        space_label = Label(text="")
        timers = Timers(orientation='horizontal', size_hint=(1, 1/6))
        self.pg_bar = MDSlider(min=0,
                               max=0,
                               value=.0,
                               value_track=False,
                               value_track_color=[116/255, 200/255, 255/255, 1],
                               size_hint=(1, 1))
        buttons = Buttons(orientation='horizontal')

        Shared.max_slider_value = self.update_max_val
        Shared.slider_val_update = self.slider_val_update
        self.pg_bar.bind(on_touch_up=self.on_slider_touch_up, on_touch_move=self.on_slider_touch_up)

        Shared.pg_bar_clear = self.reset_pg_bar
        Shared.slider_pos = self.slider_value

        self.add_widget(space_label)
        self.add_widget(timers)
        self.add_widget(self.pg_bar)
        self.add_widget(buttons)

    def update_max_val(self, max_slider_val):

        self.pg_bar.max = max_slider_val
        self.pg_bar.value = .0

    def slider_val_update(self, value):
        self.pg_bar.value = value

    def slider_value(self):
        return self.pg_bar.value

    def on_slider_touch_up(self, instance, touch):
        if self.pg_bar.collide_point(*touch.pos):
            max_slider_value = self.pg_bar.max
            normalized_value = max(0, min(touch.spos[0], 1))
            slider_value = normalized_value * max_slider_value
            self.pg_bar.value = slider_value+1.5
            Shared.slider_change(str(slider_value))

    def reset_pg_bar(self):
        self.pg_bar.value = 0.0
