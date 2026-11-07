
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class HelloKivyApp(App):

    def build(self):

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        heading = Label(
            text="Hello World!",
            font_size=30
        )

        button = Button(
            text="Click Me",
            font_size=20,
            size_hint=(1, 0.3)
        )

        button.bind(on_press=self.button_clicked)

        layout.add_widget(heading)
        layout.add_widget(button)

        return layout

    def button_clicked(self, instance):
        instance.text = "Welcome to Kivy!"


if __name__ == "__main__":
    HelloKivyApp().run()
