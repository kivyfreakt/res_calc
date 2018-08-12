# -*- coding: utf-8 -*-
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.button import MDIconButton
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.list import ILeftBodyTouch

ROOT_DIR = os.path.dirname(__file__)
KV_DIR = os.path.join(ROOT_DIR, "kv")

__version__ = '0.1.2'


# ------------------------ Классы ------------------------
class Scr(Screen):
    ''' Класс родитель для других классов ,
        предназначенных для вычисления сопротивлений
        разных типов резисторов
        Методы класса:
            format_result(self, value):
                Изменение значений сопротивлений(value) в
                более удобный и понятный вид.
            format_mult(self, value):
                Изменение значений множителя
                с кнопки в численный вид
            is_int(self, value):
                Проверка того, является ли переменная(value) целочисленной или нет
    '''

    def __init__(self, **kwargs):
        '''Конструктор класса'''
        super(Scr, self).__init__(**kwargs)
        self.MULTIPLIERS = (  # все возможные множители резистора
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
        )

        self.BUTTON_COLORS = (  # все возможные цвета для колец резистора
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
        )
        self.BUTTON_MULTIPLIERS = ('x0.01', 'x0.1', 'x1', 'x10', 'x100', 'x1k', 'x10k', 'x100k', 'x1M', 'x10M', 'x100M', 'x1G')
        self.TOLERANCES = ("10%", "5%", "1%", "2%", "0.5%", "0.25%", "0.1%", "0.05%")  # все возможные значения допусков резистора
        self.COLS_HEADS = ["1st band", "2nd band", "3rd band", "Mult.", "Tol."]

    def format_result(self, value):
        '''Изменение значений сопротивлений в более удобный вид'''
        s = " Om "
        if value >= self.MULTIPLIERS[11]:  # если сопротивление больше 10^8 , то
            value /= self.MULTIPLIERS[11]  # делим сопротивление на 10^8 и
            s = " GOm "                 # добавляем десятичную приставку
        elif value >= self.MULTIPLIERS[8]:
            value /= self.MULTIPLIERS[8]
            s = " MOm "
        elif value >= self.MULTIPLIERS[5]:
            value /= self.MULTIPLIERS[5]
            s = " kOm "
        if self.is_int(value):  # если значение целое число, то
            value = int(value)  # округляем float до int
        return (str(value) + s)

    def format_mult(self, value):
        '''Изменение значений множителя с кнопки в численный вид'''
        value = self.BUTTON_MULTIPLIERS.index(value)
        return (self.MULTIPLIERS[value])

    def is_int(self, n):
        '''Проверка того, является ли переменная целочисленной или нет'''
        return not (n % 1)


class FourRingsScreen(Scr):
    ''' Класс, предназначенный для вычисления сопротивлений
        резисторов, имеющих четырехполосную маркировку
        Методы класса:
            calculation(self, instance):
                Метод, производящий вычисление сопротивления,
                по заданным параметрам резистора
    '''
    result = StringProperty()
    resistor_colors = ListProperty()

    def __init__(self, **kwargs):
        super(FourRingsScreen, self).__init__(**kwargs)
        self.result = '1 Om ± 1%'  # сопротивление резитора
        self.resistor_params = ["1", "0", "x0.1", "1%"]  # параметры резистора
        self.resistor_colors = [3, 2, 1, 3]  # номера цветов колец резистора в массиве всех цветов

    def calculation(self, id_, text, pos):
        '''Метод, производящий вычисление сопротивления, по заданным параметрам резистора'''
        self.resistor_colors[id_] = int(pos)    # устанавливаем цвета колец на картинке резистора
        self.resistor_params[id_] = str(text)   # устанавливаем параметры резистора
        resistance = int(self.resistor_params[0] + self.resistor_params[1]) * self.format_mult(self.resistor_params[2])   # первые 2 значения резистора умножаем на множитель
        self.result = self.format_result(resistance) + "± " + self.resistor_params[3]   # изменяем значение Label


class FiveRingsScreen(Scr):
    ''' Класс, предназначенный для вычисления сопротивлений
        резисторов, имеющих пятиполосную маркировку
        Методы класса:
            calculation(self, instance):
                Метод, производящий вычисление сопротивления,
                по заданным параметрам резистора
    '''
    result = StringProperty()
    resistor_colors = ListProperty()

    def __init__(self, **kwargs):
        super(FiveRingsScreen, self).__init__(**kwargs)
        self.result = '1 Om ± 1%'  # сопротивление резитора
        self.resistor_params = ["1", "0", "0", "x0.01", "1%"]  # параметры резистора
        self.resistor_colors = [3, 2, 2, 0, 3]  # номера цветов колец резистора в массиве всех цветов

    def calculation(self, id_, text, pos):
        '''Метод, производящий вычисление сопротивления, по заданным параметрам резистора'''
        self.resistor_colors[id_] = int(pos)   # устанавливаем цвета колец на картинке резистора
        self.resistor_params[id_] = str(text)  # устанавливаем параметры резистора
        resistance = int(self.resistor_params[0] + self.resistor_params[1] + self.resistor_params[2]) * self.format_mult(self.resistor_params[3])  # первые 3 значения резистора умножаем на множитель
        self.result = self.format_result(resistance) + "± " + self.resistor_params[4]  # изменяем значение Label


class SMDScreen(Scr):
    ''' Класс, предназначенный для вычисления
        сопротивлений SMD резисторов
        Методы класса:
            calculation(self, instance):
                Метод, производящий вычисление сопротивления,
                по заданным параметрам резистора
            get_code_value(self, digits, letter):
                Получение значения сопротивления резистора
                с маркировкой EIA-96. По таблице находим
                значения, совпадающие с кодом digits, и множитель.
                Возвращаем произведение значения и множителя
    '''
    result = StringProperty()

    def __init__(self, **kwargs):
        super(SMDScreen, self).__init__(**kwargs)
        self.result = ""

    def calculation(self, instance):
        '''Метод, производящий вычисление сопротивления, по заданным параметрам резистора'''
        user_input = instance.text  # значение, полученное из textinputа
        resistance = ''  # сопротивление
        tolerance = ''  # допуск
        if user_input.isdigit():  # если полученное значение - число , то
            if len(user_input) == 3:  # если длина user_input - 3 , то
                resistance = int(user_input[0] + user_input[1]) * pow(10, int(user_input[2]))  # первые два числа из полученного значения умножаем на 10 в степени 3 числа
                tolerance = self.TOLERANCES[1]
                self.result = self.format_result(resistance) + "± " + tolerance  # изменяем значение Label
            elif len(user_input) == 4:  # если длина user_input - 4 , то
                resistance = int(user_input[0] + user_input[1] + user_input[2]) * pow(10, int(user_input[3]))   # первые три числа из полученного значения умножаем на 10 в степени 4 числа
                tolerance = self.TOLERANCES[2]
                self.result = self.format_result(resistance) + "± " + tolerance  # изменяем значение Label
        else:  # если полученное значение не полностью число , то
            try:
                if (user_input.index("R") >= 0) and not(user_input.index("R") == len(user_input) - 1):  # если в полученном значении если Буква R и она находится не на последнем месте, то
                    if(user_input.index("R") == 0):  # если в полученном значении R находится на 1 месте , то
                        resistance = float(user_input.replace("R", "0."))  # заменяем букву R в строке на 0.
                    else:
                        resistance = float(user_input.replace("R", "."))  # иначе заменяем букву R в строке на .
                    self.result = self.format_result(resistance)  # изменяем значение Label
            except ValueError:  # если буквы R в строке нет, то
                if len(user_input) == 3:  # если длина строки - 3
                    tolerance = self.TOLERANCES[2]
                    digits_code = user_input[0] + user_input[1]  # Первые два символа в строке
                    letter_code = user_input[2]  # последний символ в строке
                    if digits_code.isdigit():  # если первые два символа в строке - число
                        resistance = self.get_code_value(digits_code, letter_code)  # находим в таблице значения и получаем результат
                    self.result = self.format_result(resistance) + "± " + tolerance  # изменяем значение Label

    def get_code_value(self, digits, letter):
        ''' Получение значения сопротивления резистора
            с маркировкой EIA-96. По таблице находим
            значения, совпадающие с кодом digits, и множитель.
            Возвращаем произведение значения и множителя
        '''
        value = 0  # значение сопротивления
        multiplier = 0  # множитель
        digits = int(digits)
        digits_codes = (  # таблица кодов
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
            value = digits_codes[digits]
        if letter == "Z" or letter == "z":
            multiplier = 0.001
        elif letter == "Y" or letter == "y":
            multiplier = self.MULTIPLIERS[0]
        elif letter == "X" or letter == "x" or letter == "S" or letter == "s":
            multiplier = self.MULTIPLIERS[1]
        elif letter == "A" or letter == "a":
            multiplier = self.MULTIPLIERS[2]
        elif letter == "B" or letter == "b" or letter == "H" or letter == "h":
            multiplier = self.MULTIPLIERS[3]
        elif letter == "C" or letter == "c":
            multiplier = self.MULTIPLIERS[4]
        elif letter == "D" or letter == "d":
            multiplier = self.MULTIPLIERS[5]
        elif letter == "E" or letter == "e":
            multiplier = self.MULTIPLIERS[6]
        elif letter == "F" or letter == "f":
            multiplier = self.MULTIPLIERS[7]
        return value * multiplier

    def update_padding(self, text_input, *args):
        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width) / 2


class ColorScreen(Scr):
    def __init__(self, **kwargs):
        super(ColorScreen, self).__init__(**kwargs)


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)


class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.add_widget(ColorScreen(name="color"))
        self.add_widget(SMDScreen(name="smd"))
        self.add_widget(SettingsScreen(name="settings"))
        self.add_widget(AboutScreen(name="about"))


class ResCalcApp(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "ResCalc"
    icon = "data/icon.png"
    tabs_display_mode = StringProperty()
    prefix_dropdown = ObjectProperty()

    def build(self):
        self.tabs_display_mode = 'text'
        self.theme_cls.theme_style = 'Dark'
        self.load_kv_files(KV_DIR)
        main_widget = Builder.load_file(os.path.join(KV_DIR, "startscreen.kv"))
        return main_widget

    def load_kv_files(self, directory_kv_files):
        Builder.load_file(os.path.join(directory_kv_files, "startscreen.kv"))
        Builder.load_file(os.path.join(directory_kv_files, "smd.kv"))
        Builder.load_file(os.path.join(directory_kv_files, "settings.kv"))
        Builder.load_file(os.path.join(directory_kv_files, "about.kv"))
        Builder.load_file(os.path.join(directory_kv_files, "color.kv"))
        Builder.load_file(os.path.join(directory_kv_files, "4bands.kv"))
        Builder.load_file(os.path.join(directory_kv_files, "5bands.kv"))

    def settings(self):
        self.root.ids.manager.current = 'settings'
        return True

    def about(self):
        self.root.ids.manager.current = 'about'
        return True

    def smd(self):
        self.root.ids.manager.current = 'smd'
        return True

    def color(self):
        self.root.ids.manager.current = 'color'
        return True

    def show_snackbar(self, snack_text):
        Snackbar(text=snack_text).show()


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


if __name__ == '__main__':
    ResCalcApp().run()
