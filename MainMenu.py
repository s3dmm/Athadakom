"""Pseudo-code for the main menu of the 2D trivia game "اتحداكم".
Designed for Unity using Python style to prototype the UI logic.
"""

# Pseudo imports representing Unity APIs
from UnityEngine import GameObject, MonoBehaviour
from UnityEngine.UI import Canvas, Button, Text, Image
from UnityEngine.SceneManagement import SceneManager

class MainMenuUI(MonoBehaviour):
    """Create and manage the main menu scene."""

    def start(self):
        """Initialize UI when the scene loads."""
        self.setup_canvas()
        self.setup_background()
        self.create_title()
        self.create_buttons()

    def setup_canvas(self):
        self.canvas = GameObject("MainMenuCanvas").add_component(Canvas)
        self.canvas.render_mode = Canvas.ScreenSpaceOverlay

    def setup_background(self):
        background = GameObject("Background").add_component(Image)
        background.transform.set_parent(self.canvas.transform, False)
        background.color = (0.9, 0.9, 0.9, 1)  # soft gray

    def create_title(self):
        title = GameObject("GameTitle").add_component(Text)
        title.transform.set_parent(self.canvas.transform, False)
        title.text = "اتحداكم"
        title.font_size = 48
        title.alignment = Text.Anchor.UpperCenter
        title.rect_transform.pivot = (0.5, 1)
        title.rect_transform.anchor_min = (0.5, 1)
        title.rect_transform.anchor_max = (0.5, 1)
        title.rect_transform.anchored_position = (0, -50)

    def create_buttons(self):
        # Create Play, Profile and Settings buttons
        self.play_btn = self.make_button("Play", self.on_play)
        self.profile_btn = self.make_button("Profile", self.on_profile)
        self.settings_btn = self.make_button("Settings", self.on_settings)
        self.arrange_buttons([self.play_btn, self.profile_btn, self.settings_btn])

    def make_button(self, label, callback):
        btn_obj = GameObject(f"{label}Button").add_component(Button)
        btn_obj.transform.set_parent(self.canvas.transform, False)
        text = GameObject(f"{label}Text").add_component(Text)
        text.transform.set_parent(btn_obj.transform, False)
        text.text = label
        btn_obj.on_click.add_listener(callback)
        return btn_obj

    def arrange_buttons(self, buttons):
        for index, btn in enumerate(buttons):
            btn.rect_transform.anchor_min = (0.5, 0.5)
            btn.rect_transform.anchor_max = (0.5, 0.5)
            btn.rect_transform.pivot = (0.5, 0.5)
            btn.rect_transform.anchored_position = (0, -100 * index)

    def on_play(self):
        SceneManager.load_scene("Level1")

    def on_profile(self):
        print("Profile clicked")

    def on_settings(self):
        print("Settings clicked")
