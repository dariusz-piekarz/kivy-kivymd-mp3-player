from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from shared import Shared


class Timers(BoxLayout):
    def __init__(self, **kwargs):
        super(Timers, self).__init__(**kwargs)
        middle_label = Label(text="", size_hint=(1 - 6 / 40, 1))
        self.right_label = Label(text="00:00/00:00", size_hint=(6 / 40, 1), halign='right')

        Shared.get_total_length = self.update_total_length
        Shared.update_current_pos = self.update_current_pos
        Shared.clear_timer = self.clear_timer
        Shared.timer_beginning = self.set_beginning

        self.add_widget(middle_label)
        self.add_widget(self.right_label)

    def update_total_length(self, leng):
        temp = self.right_label.text.split("/")
        temp[1] = leng
        self.right_label.text = "/".join(temp)

    def update_current_pos(self, leng):
        temp = self.right_label.text.split("/")
        temp[0] = leng
        self.right_label.text = "/".join(temp)

    def clear_timer(self):
        self.right_label.text = "00:00/00:00"

    def set_beginning(self, leng):
        self.right_label.text = f"00:00/{leng}"
