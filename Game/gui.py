"""
gui.py

Модуль, содержащий класс для работы с графическим интерфейсом приложения.

Этот файл определяет класс `MyWidget`, который отвечает за построение
и настройку пользовательского интерфейса. Все элементы интерфейса
и их обработчики сигналов описаны здесь.

Классы:
    MyWidget: Основной класс интерфейса, наследуемый от QMainWindow.

Методы:
    - initialize_ui(): Инициализация элементов интерфейса.
    - rewrite_text(): Обновление слов на экране.
    - switch_language_typing(): Переключение языка интерфейса.
    - tick_timer(): Обновление таймера и управление временем.
"""

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
import random
from exceptions import FileMissingError


class MyWidget(QMainWindow):
    """
    Класс для создания графического интерфейса теста скорости печати.
    """
    def __init__(self):
        super().__init__()
        try:
            uic.loadUi('Wpm Test.ui', self)
        except FileNotFoundError:
            raise FileMissingError("Wpm Test.ui")

        # Инициализация списков слов
        self.english_easy_words = []
        self.english_hard_words = []
        self.russian_easy_words = []
        self.russian_hard_words = []

        # Сопоставление списков слов и файлов
        self.all_words = [
            self.english_easy_words,
            self.english_hard_words,
            self.russian_easy_words,
            self.russian_hard_words
        ]
        self.all_txt_files = [
            'english_easy_words.txt',
            'english_hard_words.txt',
            'russian_easy_words.txt',
            'russian_hard_words.txt'
        ]

        # Загрузка слов из файлов
        self.load_words()

        # Элементы интерфейса
        self.first_words = [
            self.word1_1, self.word1_2, self.word1_3,
            self.word1_4, self.word1_5, self.word1_6
        ]
        self.second_words = [
            self.word2_1, self.word2_2, self.word2_3,
            self.word2_4, self.word2_5, self.word2_6
        ]

        # Настройка шрифтов для слов
        for label in self.first_words + self.second_words:
            label.setFont(QFont('Times', 17))

        # Начальная настройка интерфейса
        self.initialize_ui()

        # Логические флаги
        self.flag_rus_words = True
        self.flag_eng_words = False
        self.flag_btn_1 = True
        self.flag_btn_2 = False
        self.ready_words = 0
        self.flag_timer = True
        self.list_value_timer = []

        # Списки для отображаемых слов
        self.list_first_line = []
        self.list_second_line = []
        self.count = 0

        # Начальная генерация текста
        self.rewrite_text()

    def load_words(self):
        """
        Загружает слова из файлов в соответствующие списки.
        """
        for index, words in enumerate(self.all_words):
            try:
                with open(self.all_txt_files[index], encoding='utf-8') as file:
                    for line in file:
                        for word in line.split(','):
                            if word.strip():
                                words.append(word.strip().lower())
            except FileNotFoundError:
                raise FileMissingError(self.all_txt_files[index])

    def initialize_ui(self):
        """
        Настраивает элементы пользовательского интерфейса.
        """
        self.btn_1.setStyleSheet(
            'QPushButton {'
                'background-color: #ff9900;'
                'color: white;'
            '}'
        )
        self.btn_2.setStyleSheet(
            'QPushButton {'
                'background-color: transparent;'
                'color: black;'
            '}'
        )
        self.btn_rewrite.setStyleSheet(
            'QPushButton {'
                'background-color: #ff9900;'
                'color: white;'
            '}'
        )
        self.btn_switch_lng.setStyleSheet(
            'QPushButton {'
                'background-color: #ff9900;'
                'color: white;'
            '}'
        )
        self.btn_switch_lng.setFont(QFont("Times", 13))
        self.main_line_edit.setFont(QFont("Times", 17))

        # Подключение сигналов
        self.btn_1.clicked.connect(self.switch_level_typing)
        self.btn_2.clicked.connect(self.switch_level_typing)
        self.btn_rewrite.clicked.connect(self.rewrite_text)
        self.btn_switch_lng.clicked.connect(self.switch_language_typing)
        self.main_line_edit.textChanged.connect(self.check_text)

        self.lcd_timer.display(60)

    def tick_timer(self):
        """
        Запускает и обновляет таймер.
        """
        lcd_value = self.lcd_timer.value()
        self.list_value_timer.append(lcd_value)

        if len(self.list_value_timer) >= 2 and self.list_value_timer[-1] >= self.list_value_timer[-2]:
            self.lcd_timer.display(0)
            lcd_value = self.lcd_timer.value()

        if lcd_value > 0:
            self.lcd_timer.display(lcd_value - 1)
            QTimer().singleShot(1000, self.tick_timer)
        else:
            self.finish_timer()

    def finish_timer(self):
        """
        Завершает работу таймера и отображает результат.
        """
        self.ready_label.show()
        self.ready_label_num.setText(str(self.ready_words))
        self.ready_label_num.setFont(QFont("Times", 48))
        self.ready_label_num.setStyleSheet("QLabel{color: black}")
        self.ready_label_num.show()
        self.ready_words = 0
        self.list_value_timer = []
        self.main_line_edit.setEnabled(False)
        self.lcd_timer.display(60)
        self.flag_timer = True

    def switch_level_typing(self):
        """
        Переключает уровень сложности (легкий/сложный).
        """
        self.flag_btn_1 = not self.flag_btn_1
        self.flag_btn_2 = not self.flag_btn_2

        # Выбираем новый набор слов
        word_list = self.russian_easy_words if self.flag_rus_words else self.english_easy_words
        if not self.flag_btn_1:  # Если выбран сложный уровень
            word_list = self.russian_hard_words if self.flag_rus_words else self.english_hard_words

        # Обновляем текст в виджетах
        self.populate_words(word_list, self.first_words, self.list_first_line)
        self.populate_words(word_list, self.second_words, self.list_second_line)
        if self.flag_btn_1:
            self.btn_1.setStyleSheet("""
                QPushButton {
                    background-color: #ff9900;  
                    color: white;
                }
            """)
            self.btn_2.setStyleSheet("background-color: transparent; color: black;")
        else:
            self.btn_1.setStyleSheet("background-color: transparent; color: black;")
            self.btn_2.setStyleSheet("""
                QPushButton {
                    background-color: #ff9900; 
                    color: white;
                }
            """)

    def switch_language_typing(self):
        """
        Переключает язык (русский/английский).
        """
        self.flag_rus_words = not self.flag_rus_words
        self.flag_eng_words = not self.flag_eng_words
        self.btn_switch_lng.setText('English' if self.flag_eng_words else 'Russian')
        self.rewrite_text()

    def check_text(self):
        """
        Проверяет введенный пользователем текст.
        """
        if self.flag_timer:
            self.flag_timer = False
            self.tick_timer()

        if self.count == 6:
            self.list_first_line = self.list_second_line
            for i, word in enumerate(self.list_first_line[:len(self.first_words)]):
                self.first_words[i].setText(word)
                self.first_words[i].setStyleSheet("QLabel{color: black}")
            self.rewrite_second_line()
            self.count = 0
        elif ' ' in self.main_line_edit.text():
            if self.main_line_edit.text().strip() == self.list_first_line[self.count]:
                self.first_words[self.count].setStyleSheet("QLabel{color: green}")
                self.ready_words += 1
            else:
                self.first_words[self.count].setStyleSheet("QLabel{color: red}")
            self.count += 1
            self.main_line_edit.setText('')
        else:
            current_text = self.main_line_edit.text()
            expected_text = self.first_words[self.count].text()
            if expected_text.startswith(current_text):
                self.first_words[self.count].setStyleSheet("QLabel{background-color: #b3b3b3}")
            else:
                self.first_words[self.count].setStyleSheet("QLabel{background-color: red}")

    def rewrite_text(self):
        """
        Обновляет слова на экране.
        """
        self.ready_label.hide()
        self.ready_label_num.hide()
        self.main_line_edit.setEnabled(True)
        self.lcd_timer.display(60)
        self.count = 0
        self.ready_words = 0
        self.list_first_line = []
        self.list_second_line = []
        self.main_line_edit.setText('')

        word_list = self.russian_easy_words if self.flag_rus_words else self.english_easy_words
        if not self.flag_btn_1:
            word_list = self.russian_hard_words if self.flag_rus_words else self.english_hard_words

        self.populate_words(word_list, self.first_words, self.list_first_line)
        self.populate_words(word_list, self.second_words, self.list_second_line)

    def populate_words(self, word_list, labels, output_list):
        """
        Заполняет виджеты случайными словами.
        """
        for label in labels:
            word = random.choice(word_list)
            label.setText(word)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setStyleSheet("QLabel{color: black}")
            output_list.append(word)

    def rewrite_second_line(self):
        """
        Обновляет вторую строку слов.
        """
        word_list = self.russian_easy_words if self.flag_rus_words else self.english_easy_words
        self.populate_words(word_list, self.second_words, self.list_second_line)