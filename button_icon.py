from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button.button import MDIconButton


class UpdateIcon(BoxLayout):
    iterator = 0

    def __init__(self, icons, icon_size, icon_colors=None, action=None, args=None, **kwargs):
        super(UpdateIcon, self).__init__(**kwargs)
        self.icons = icons
        self.action = action
        self.args = args
        self.upper_limit = len(icons)

        self.icon_colors = icon_colors
        self.icon_button = MDIconButton(icon=self.icons[0], size_hint=(1, 1), icon_size=icon_size)

        if self.icon_colors:
            self.icon_button.theme_icon_color = "Custom"
            self.icon_button.icon_color = self.icon_colors[0]

        self.icon_button.bind(on_press=self.update_icon)

        self.add_widget(self.icon_button)

    def update_icon(self, instance):
        self.iterator = (self.iterator + 1) % self.upper_limit

        self.icon_button.icon = self.icons[self.iterator]
        if self.icon_colors:
            self.icon_button.icon_color = self.icon_colors[self.iterator]
        if self.action:
            self.action(self.iterator, self.args)

    def update_icon_image(self, image, iter):
        self.iterator = iter
        self.icon_button.icon = image

    def update_icon_slider(self, instance, value, thresholds={0.0: 1, 30.0: 2, 60.0: 3, 90.0: 0, 100.0: 0}):
        keys = list(thresholds.keys())
        if value == keys[0]:
            self.icon_button.icon = self.icons[thresholds[keys[0]]]
            self.iterator = thresholds[keys[0]]
        elif value == keys[-1]:
            self.icon_button.icon = self.icons[thresholds[keys[-1]]]
            self.iterator = thresholds[keys[-1]]
        else:
            for i in range(1, len(keys)):
                if keys[i - 1] < value <= keys[i]:
                    self.iterator = thresholds[keys[i]]
                    self.icon_button.icon = self.icons[self.iterator]
