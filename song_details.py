from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image as CoreImage

from mutagen.id3 import ID3
from io import BytesIO
from base64 import b64encode

from shared import Shared


class SongDetails(BoxLayout):
    def __init__(self, **kwargs):
        super(SongDetails, self).__init__(**kwargs)
        space_label = Label(text="", size_hint=(1, 1/10))
        space_label1 = Label(text="", size_hint=(1, 3/10))
        self.album_cover = CoreImage(source="cover.jpg", size_hint=(1, 3/10))
        self.song_name = Label(text="Song Name", size_hint=(1, 1/10))
        self.author_name = Label(text="Author", size_hint=(1, 1/10))
        self.album_name = Label(text="Album name", size_hint=(1, 1/10))

        self.add_widget(space_label)
        self.add_widget(self.album_cover)
        self.add_widget(self.album_name)
        self.add_widget(self.author_name)
        self.add_widget(self.song_name)
        self.add_widget(space_label1)

        Shared.update_details_data = self.update_data
        Shared.clear_details = self.clear_details

    def update_data(self, instance):
        if len(Shared.fields) > 0:
            path = Shared.fields.at[Shared.current_choice, 'Path']
            try:
                self.song_name.text = Shared.fields.at[Shared.current_choice, 'Title']
            except:
                self.song_name.text = "Unknown"
            try:
                self.author_name.text = Shared.fields.at[Shared.current_choice, 'Author']
            except:
                self.author_name.text = 'Unknown'
            try:
                self.album_name.text = Shared.fields.at[Shared.current_choice, 'Album']
            except:
                self.album_name.text = 'Unknown'

            tags = ID3(path)
            if "APIC:" in tags.keys():
                cover = tags["APIC:"]
                cover_image = BytesIO(cover.data)

                self.album_cover.source = f"data:image/png;base64,{b64encode(cover_image.getvalue()).decode()}"

            elif "APIC:Cover" in tags.keys():
                cover = tags["APIC:Cover"]
                cover_image = BytesIO(cover.data)
                self.album_cover.source = f"data:image/png;base64,{b64encode(cover_image.getvalue()).decode()}"

            else:
                self.album_cover.source = "cover.jpg"
            Shared.update_bg(self.album_cover.source)

    def clear_details(self):
        self.album_cover.source = "cover.jpg"
        Shared.update_bg(self.album_cover.source)
        self.song_name.text = "Song Name"
        self.author_name.text = "Author"
        self.album_name.text = "Album name"
