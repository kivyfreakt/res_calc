# -*- coding: utf-8 -*-

# ------------------------ Библиотеки ------------------------
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.actionbar import ActionBar, ActionButton, ActionView, ActionPrevious, ActionGroup
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

# ------------------------ Константы и переменные ------------------------

BUTTON_COLORS = [  # все возможные цвета для колец резистора
    (.70, .70, .70, 1),  # серебряный
    (.94, .64, .4, 1),  # золотой
    (0, 0, 0, 1),  # черный
    (.36, .25, .22, 1),  # коричневый
    (.91, .30, .24, 1),  # красный
    (.90, .49, .13, 1),  # оранжевый
    (1, .92, .23, 1),  # желтый
    (.15, .68, .38, 1),  # зеленый
    (.16, .50, .73, 1),  # синий
    (.56, .27, .68, 1),  # фиолетовый
    (.58, .65, .65, 1),  # серый
    (1, 1, 1, 1)  # белый
]
MULTIPLIERS = [  # все возможные множители резистора
    0.01,
    0.1,
    1,
    10,
    100,
    1000,
    10000,
    100000,
    1000000,
    10000000,
    100000000,
    1000000000
]

TOLERANCES = ["10%", "5%", "1%", "2%", "0.5%", "0.25%", "0.1%", "0.05%"]

# ------------------------ Классы ------------------------


class Scr(Screen):
    def __init__(self, **kwargs):
        super(Scr, self).__init__(**kwargs)

    def format_result(self, value):
        s = " Oм ± "
        if value >= MULTIPLIERS[11]:
            value /= MULTIPLIERS[11]
            s = " ГOм ± "
        elif value >= MULTIPLIERS[8]:
            value /= MULTIPLIERS[8]
            s = " МOм ± "
        elif value >= MULTIPLIERS[5]:
            value /= MULTIPLIERS[5]
            s = " кOм ± "
        if self.is_int(value):
            value = int(value)
        return (str(value) + s)

    def is_int(self, n):
        return not (n % 1)

    def changer(self, instance):
        if instance.id == "4":
            self.manager.current = '4rings'
        if instance.id == "5":
            self.manager.current = '5rings'
        elif instance.id == "smd":
            self.manager.current = 'smd'


class FourRingsScreen(Scr):
    def __init__(self, **kwargs):
        super(FourRingsScreen, self).__init__(**kwargs)
        NUM_COLS = 4
        self.resistor_params = ["1", "0", "0.1", "1%"]
        self.cols_heads = ["1st ring", "2nd ring", "Multiplier", "Tolerance"]

        parent = BoxLayout(orientation="vertical")
        box = BoxLayout()
        action_bar = ActionBar()
        action_view = ActionView()
        action_group1 = ActionGroup(text="Normal")
        self.result = Label(text="1 Ом ± 1%", font_size='25sp', size_hint_y=None)

        column = 0
        for column in range(NUM_COLS):
            layout = GridLayout(id=str(column), cols=1, spacing=5, padding=[5, 5, 5, 5])
            layout.add_widget(Label(text=self.cols_heads[column]))
            if column < 2:
                j = 2
                k = 0
                layout.add_widget(Label(text="-"))
                layout.add_widget(Label(text="-"))
                while j < 12:
                    layout.add_widget(
                        Button(
                            id=str(column),
                            text=str(k),
                            background_normal='',
                            background_color=BUTTON_COLORS[j],
                            on_press=self.calculation))
                    j += 1
                    k += 1
            elif column == 2:
                j = 0
                for j in range(12):
                    layout.add_widget(
                        Button(
                            id=str(column),
                            text=str(MULTIPLIERS[j]),
                            background_normal='',
                            background_color=BUTTON_COLORS[j],
                            on_release=self.calculation))
            elif column == 3:
                j = 0
                k = 0
                for j in range(12):
                    if (j == 2 or j == 5 or j == 6 or j == 11):
                        layout.add_widget(Label(text="-"))
                    else:
                        layout.add_widget(
                            Button(
                                id=str(column),
                                text=TOLERANCES[k],
                                background_normal='',
                                background_color=BUTTON_COLORS[j],
                                on_release=self.calculation))
                        k += 1
            box.add_widget(layout)

        action_view.add_widget(ActionPrevious(with_previous=False, app_icon="icon.png"))
        action_group1.add_widget(ActionButton(id="4", text="4 rings"))
        action_group1.add_widget(ActionButton(id="5", text="5 rings", on_press=self.changer))
        action_view.add_widget(action_group1)
        action_view.add_widget(ActionButton(id="smd", text="SMD", on_press=self.changer))
        action_bar.add_widget(action_view)
        parent.add_widget(action_bar)
        parent.add_widget(self.result)
        parent.add_widget(box)
        self.add_widget(parent)

    def calculation(self, instance):
        self.resistor_params[int(instance.id)] = str(instance.text)
        value = int(self.resistor_params[0] + self.resistor_params[1]) * float(self.resistor_params[2])
        self.result.text = self.format_result(value) + self.resistor_params[3]


class FiveRingsScreen(Scr):
    def __init__(self, **kwargs):
        super(FiveRingsScreen, self).__init__(**kwargs)
        NUM_COLS = 5

        self.resistor_params = ["1", "0", "0", "0.01", "1%"]
        self.cols_heads = ["1st ring", "2nd ring", "3rd ring", "Multiplier", "Tolerance"]
        parent = BoxLayout(orientation="vertical")
        box = BoxLayout()
        action_bar = ActionBar()
        action_view = ActionView()
        action_group1 = ActionGroup(text="Normal")
        self.result = Label(text="1 Ом ± 1%", font_size='25sp', size_hint_y=None)

        column = 0
        for column in range(NUM_COLS):
            layout = GridLayout(id=str(column), cols=1, spacing=5, padding=[5, 5, 5, 5])
            layout.add_widget(Label(text=self.cols_heads[column]))
            if column < 3:
                j = 2
                k = 0
                layout.add_widget(Label(text="-"))
                layout.add_widget(Label(text="-"))
                while j < 12:
                    layout.add_widget(
                        Button(
                            id=str(column),
                            text=str(k),
                            background_normal='',
                            background_color=BUTTON_COLORS[j],
                            on_press=self.calculation))
                    j += 1
                    k += 1
            elif column == 3:
                j = 0
                for j in range(12):
                    layout.add_widget(
                        Button(
                            id=str(column),
                            text=str(MULTIPLIERS[j]),
                            background_normal='',
                            background_color=BUTTON_COLORS[j],
                            on_release=self.calculation))
            elif column == 4:
                j = 0
                k = 0
                for j in range(12):
                    if (j == 2 or j == 5 or j == 6 or j == 11):
                        layout.add_widget(Label(text="-"))
                    else:
                        layout.add_widget(
                            Button(
                                id=str(column),
                                text=TOLERANCES[k],
                                background_normal='',
                                background_color=BUTTON_COLORS[j],
                                on_release=self.calculation))
                        k += 1
            box.add_widget(layout)

        action_view.add_widget(ActionPrevious(with_previous=False, app_icon="icon.png"))
        action_group1.add_widget(ActionButton(id="4", text="4 rings", on_press=self.changer))
        action_group1.add_widget(ActionButton(id="5", text="5 rings"))
        action_view.add_widget(action_group1)
        action_view.add_widget(ActionButton(id="smd", text="SMD", on_press=self.changer))
        action_bar.add_widget(action_view)
        parent.add_widget(action_bar)
        parent.add_widget(self.result)
        parent.add_widget(box)
        self.add_widget(parent)

    def calculation(self, instance):
        self.resistor_params[int(instance.id)] = str(instance.text)
        value = int(self.resistor_params[0] + self.resistor_params[1] + self.resistor_params[2]) * float(self.resistor_params[3])
        self.result.text = self.format_result(value) + self.resistor_params[4]


class SMDScreen(Scr):
    def __init__(self, **kwargs):
        super(SMDScreen, self).__init__(**kwargs)
        parent = BoxLayout(orientation="vertical")
        action_bar = ActionBar()
        action_view = ActionView()
        action_group1 = ActionGroup(text="Normal")
        self.result = Label(text="100 Ом ± 5%", font_size='25sp', size_hint_y=None)
        box = FloatLayout()
        value_textbox = TextInput(multiline=False, text="101", size_hint=(None, None), size=(150, 80), padding=[20, 10, 10, 20], background_color=(0, 0, 0, 1), cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1), pos_hint={'center_x': .5, 'y': .5}, font_size=50, on_text_validate=self.calculation)
        action_view.add_widget(ActionPrevious(with_previous=False, app_icon="icon.png"))
        action_group1.add_widget(ActionButton(id="4", text="4 rings", on_press=self.changer))
        action_group1.add_widget(ActionButton(id="5", text="5 rings", on_press=self.changer))
        action_view.add_widget(action_group1)
        action_view.add_widget(ActionButton(id="smd", text="SMD"))
        action_bar.add_widget(action_view)
        box.add_widget(value_textbox)
        parent.add_widget(action_bar)
        parent.add_widget(self.result)
        parent.add_widget(box)
        self.add_widget(parent)

    def calculation(self, instance):
        user_input = instance.text
        value = ''
        tol = ""
        if user_input.isdigit():
            if len(user_input) == 3:
                value = int(user_input[0] + user_input[1]) * pow(10, int(user_input[2]))
                tol = "5%"
            elif len(user_input) == 4:
                value = int(user_input[0] + user_input[1] + user_input[2]) * pow(10, int(user_input[3]))
                tol = "1%"
            self.result.text = self.format_result(value) + tol
        else:
            try:
                if (user_input.index("R") >= 0) and not(user_input.index("R") == len(user_input) - 1):
                    if(user_input.index("R") == 0):
                        value = float(user_input.replace("R", "0."))
                    else:
                        value = float(user_input.replace("R", "."))
                    self.result.text = self.format_result(value) + tol
            except ValueError:
                if len(user_input) == 3:
                    tol = "1%"
                    digits_code = user_input[0] + user_input[1]
                    letter_code = user_input[2]
                    if digits_code.isdigit():
                        value = self.get_code_value(digits_code, letter_code)
                    self.result.text = self.format_result(value) + tol

    def get_code_value(self, digits, letter):
        a = b = 0
        digits = int(digits)
        codes = (
            0, 100, 102, 105, 107, 110, 113,
            115, 118, 121, 124, 127, 130,
            133, 137, 140, 143, 147, 150,
            154, 158, 162, 165, 169, 174,
            178, 182, 187, 191, 196, 200,
            205, 210, 215, 221, 226, 232,
            237, 243, 249, 255, 261, 267,
            274, 280, 287, 294, 301, 309,
            316, 324, 332, 340, 348, 357,
            365, 374, 383, 392, 402, 412,
            422, 432, 442, 453, 464, 475,
            487, 499, 511, 523, 536, 549,
            562, 576, 590, 604, 619, 634,
            649, 665, 681, 698, 715, 732,
            750, 768, 787, 806, 825, 845,
            866, 887, 909, 931, 953, 976
        )
        if digits < 97:
            a = codes[digits]
        if letter == "Z" or letter == "z":
            b = 0.001
        elif letter == "Y" or letter == "y":
            b = 0.01
        elif letter == "X" or letter == "x" or letter == "S" or letter == "s":
            b = 0.1
        elif letter == "A" or letter == "a":
            b = 1
        elif letter == "B" or letter == "b" or letter == "H" or letter == "h":
            b = 10
        elif letter == "C" or letter == "c":
            b = 100
        elif letter == "D" or letter == "d":
            b = 1000
        elif letter == "E" or letter == "e":
            b = 10000
        elif letter == "F" or letter == "f":
            b = 100000
        return a * b


class RescalcApp(App):
    def build(self):
        self.icon = "icon.png"
        Window.clearcolor = (.19, .19, .19, 1)  # фоновой цвет приложения
        screen_manager = ScreenManager(transition=NoTransition())  # виджет управления окнами
        four_rings_screen = FourRingsScreen(name='4rings')  # окно для расчета сопротивления резистора с 4 кольцами
        five_rings_screen = FiveRingsScreen(name='5rings')  # окно для расчета сопротивления резистора с 5 кольцами
        smd_screen = SMDScreen(name="smd")  # окно для расчета сопротивления smd резистора
        screen_manager.add_widget(four_rings_screen)
        screen_manager.add_widget(five_rings_screen)
        screen_manager.add_widget(smd_screen)
        return screen_manager


if __name__ == '__main__':
    RescalcApp().run()
