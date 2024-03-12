from kivymd.uix.button.button import MDIconButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from glob import glob

from shared import Shared
from song_tools import get_metadata


class ChooserButtons(BoxLayout):
    def __init__(self, object, **kwargs):
        super(ChooserButtons, self).__init__(**kwargs)
        self.object = object
        add = MDIconButton(icon='plus',
                           icon_size="29sp",
                           pos_hint={'center_x': 0.5, 'center_y': 0.5},
                           size_hint=(1 / 7, 1))
        remove = MDIconButton(icon='minus',
                              icon_size="29sp",
                              pos_hint={'center_x': 0.5, 'center_y': 0.5},
                              size_hint=(1 / 7, 1))
        load_folder = MDIconButton(icon='folder-plus-outline',
                                   icon_size="29sp",
                                   size_hint=(1 / 7, 1))
        clear = MDIconButton(icon='broom',
                             icon_size="29sp",
                             size_hint=(1 / 7, 1))
        space = Label(text="", size_hint=(3/7, 1))

        add.bind(on_release=self.on_add)
        remove.bind(on_release=self.on_del)
        clear.bind(on_release=self.on_clear)
        load_folder.bind(on_release=self.add_folder)

        self.add_widget(add)
        self.add_widget(remove)
        self.add_widget(load_folder)
        self.add_widget(clear)
        self.add_widget(space)

    def on_add(self, instance):
        if len(Shared.temp) > 0:
            tp = get_metadata(Shared.temp)
            for field in ['Path', 'Title', 'Author', 'Album']:
                Shared.fields.at[Shared.index, field] = tp[field]
            self.object.add_row()
            Shared.tp = dict({})
            Shared.temp = []
            Shared.index += 1

    def on_del(self, instance):
        value_to_remove = self.object.del_row()
        Shared.tp = dict({})
        Shared.temp = []
        condition = Shared.fields.index == value_to_remove

        Shared.fields = Shared.fields.drop(Shared.fields[condition].index)
        Shared.fields = Shared.fields.reset_index(drop=True)

    def on_clear(self, instance):
        self.object.del_all_rows()
        Shared.clear_music_data()
        Shared.clear_timer()
        Shared.pg_bar_clear()
        Shared.clear_details()

    def add_folder(self, instance):
        allowed_extensions = ['mp3', 'ogg', 'flac', 'wma', 'wav']
        list_of_path = []
        for extension in allowed_extensions:
            pattern = f"{Shared.folder_path}\\*.{extension}"
            list_of_path.extend(glob(pattern))
        for path in list_of_path:
            for field in ['Path', 'Title', 'Author', 'Album']:
                tp = get_metadata(path)
                Shared.fields.at[Shared.index, field] = tp[field]
            self.object.add_row()
            Shared.tp = dict({})
            Shared.temp = []
            Shared.index += 1
