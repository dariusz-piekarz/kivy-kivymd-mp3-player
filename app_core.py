from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image

from PIL import Image as PILImage, ImageFilter, ImageEnhance
from base64 import b64decode
from io import BytesIO

from shared import Shared
from player_bar import PlayerBar
from details_bar import NestedBoxLayout


class Application(MDApp):

    window_width = 800
    window_height = 600

    def build(self):
        self.layout = FloatLayout()
        self.theme_cls.theme_style = 'Dark'

        self.space_label = Label(text="", size_hint=(1, 1 / 20), pos_hint={'top': 0.76})
        self.nested = NestedBoxLayout(orientation='horizontal', size_hint=(1, 5 / 7), pos_hint={'top': 0.74})
        self.player_panel = PlayerBar(orientation='vertical',
                                      size_hint=(1, 1 - 1 / 20 - 5 / 7),
                                      pos_hint={'top': 1.0})

        self.layout.add_widget(self.player_panel)
        self.layout.add_widget(self.space_label)
        self.layout.add_widget(self.nested)

        Shared.update_bg = self.update_background

        return self.layout

    def on_start(self):
        Window.bind(on_resize=self.on_window_resize)

    def on_window_resize(self, instance, width, height):
        self.nested.update_size(width)

    def update_background(self, base64_data):
        if base64_data != "cover.jpg":
            image_data = b64decode(base64_data.split(",")[1])
            cover_image = PILImage.open(BytesIO(image_data))
            blurred_image = cover_image.copy().filter(ImageFilter.BLUR)
            saturation_factor = 0.6
            alpha_factor = 0.6
            enhanced_image = ImageEnhance.Color(blurred_image).enhance(saturation_factor)
            final_image = self.add_alpha_channel(enhanced_image, alpha_factor)
            rotated_image = final_image.rotate(180, expand=True)

            if hasattr(self, 'bg_image'):
                self.bg_image.texture = self.create_texture(rotated_image)
            else:
                self.bg_image = Image(texture=self.create_texture(rotated_image), allow_stretch=True, keep_ratio=False)

                self.layout.add_widget(self.bg_image)
                self.layout.remove_widget(self.player_panel)
                self.layout.add_widget(self.player_panel)
                self.layout.remove_widget(self.space_label)
                self.layout.add_widget(self.space_label)
                self.layout.remove_widget(self.nested)
                self.layout.add_widget(self.nested)

        else:
            if hasattr(self, 'bg_image'):
                self.layout.remove_widget(self.bg_image)
                del self.bg_image

    def create_texture(self, pil_image):
        width, height = pil_image.size
        texture = Texture.create(size=(width, height), colorfmt='rgba')
        texture.blit_buffer(pil_image.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
        return texture

    def add_alpha_channel(self, image, alpha_factor):
        alpha = int(255 * alpha_factor)
        alpha_channel = PILImage.new('L', image.size, alpha)
        image.putalpha(alpha_channel)
        return image
