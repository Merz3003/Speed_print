"""
logic.py

Модуль, содержащий вспомогательные функции для логики приложения.

Этот файл включает функции, используемые для обработки текстов,
расчета результатов и проверки введенных данных.

Функции:
    - load_words_from_file(file_path): Загружает слова из текстового файла.
    - generate_random_words(word_list, count): Генерирует случайные слова из списка.
    - validate_user_input(input_text, expected_text): Проверяет правильность ввода пользователя.
    - calculate_wpm(word_count, elapsed_time): Рассчитывает скорость печати (WPM).
"""
import random


def load_words_from_file(file_path: str) -> list:
    """
    Загружает слова из указанного текстового файла.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            words = []
            for line in file:
                words.extend([word.strip().lower() for word in line.split(',') if word.strip()])
            return words
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{file_path}' не найден.")
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке файла '{file_path}': {e}")


def generate_random_words(word_list: list, count: int) -> list:
    """
    Генерирует случайные слова из указанного списка.
    """
    if not isinstance(word_list, list) or not word_list:
        raise ValueError("Список слов должен быть непустым списком.")
    if not isinstance(count, int) or count <= 0:
        raise ValueError("Количество слов должно быть положительным целым числом.")
    if count > len(word_list):
        raise ValueError("Количество запрашиваемых слов превышает доступное количество.")
    return random.sample(word_list, count)


def validate_user_input(input_text: str, expected_text: str) -> bool:
    """
    Проверяет введенное пользователем слово.
    """
    if not isinstance(input_text, str) or not isinstance(expected_text, str):
        raise ValueError("Оба аргумента должны быть строками.")
    return input_text.strip().lower() == expected_text.lower()


def calculate_wpm(word_count: int, elapsed_time: int) -> float:
    """
    Вычисляет скорость печати в словах в минуту (WPM).
    """
    if not isinstance(word_count, int) or word_count < 0:
        raise ValueError("Количество слов должно быть неотрицательным целым числом.")
    if not isinstance(elapsed_time, int) or elapsed_time <= 0:
        raise ValueError("Время должно быть положительным целым числом.")
    return (word_count / elapsed_time) * 60