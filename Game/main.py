from PyQt5.QtWidgets import QApplication
from gui import MyWidget
import sys


def main():
    """
    Основная функция для запуска приложения.
    """
    # Создаем экземпляр приложения
    app = QApplication(sys.argv)

    # Создаем и настраиваем главное окно
    main_window = MyWidget()
    main_window.setFixedSize(1296, 327)
    main_window.show()

    # Запускаем главный цикл приложения
    sys.exit(app.exec())


if __name__ == '__main__':
    main()