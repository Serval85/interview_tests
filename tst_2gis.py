import sys


def print_in_box(message: str, width: int, height: int) -> None:
    """
    Рисует текстовую строку внутри прямоугольной рамки из символов '#'.

    Параметры:
      message (str): Выводимый текст.
      width (int): Ширина рамки.
      height (int): Высота рамки.

    Возбуждает исключения:
      ValueError: Если ширина рамки меньше требуемого размера или высота менее трёх символов.
    """
    if len(message) >= width - 2:
        raise ValueError("Ширина рамки недостаточна для отображения текста.")
    if height < 3:
        raise ValueError("Высота рамки должна быть минимум 3 символа.")

    # Горизонтальные отступы для центрирования текста
    horizontal_padding = (width - len(message)) // 2

    # Верхняя строка рамки
    print("#" * width)

    # Внутренность рамки
    middle_row = height // 2
    for i in range(1, height - 1):
        if i != middle_row:
            print("#" + " " * (width - 2) + "#")  # Пустые строки внутри рамки
        else:
            padding_left = max(horizontal_padding, 1)
            padding_right = width - len(message) - padding_left - 2
            print("#" + " " * padding_left + message + " " * padding_right + "#")

    # Нижняя строка рамки
    print("#" * width)


if __name__ == "__main__":
    try:
        # Простое тестирование функции
        print_in_box("Hello, World!", 16, 5)
    except Exception as e:
        print(f"Произошла ошибка: {e}", file=sys.stderr)
