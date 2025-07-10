import sys


def process_list(lst: list) -> tuple:
    """
    Обрабатывает список: подсчитывает количество повторений элементов и удаляет дубликаты.

    Параметры:
      lst (list): Исходный список для обработки.

    Возвращает:
      tuple: Кортеж из двух элементов:
          - Словарь с подсчётом повторений каждого элемента
          - Список уникальных элементов в порядке первого вхождения
    """
    count_dict = {}
    unique_list = []
    seen_keys = set()

    for item in lst:
        # Ключ, учитывающий тип элемента
        key = (type(item), item

        # Подсчёт повторений
        count_dict[key] = count_dict.get(key, 0) + 1

        # Формирование списка без дубликатов
        if key not in seen_keys:
            seen_keys.add(key)
            unique_list.append(item)

    return count_dict, unique_list


if __name__ == "__main__":
    try:
        # Исходные данные
        source_data = [1.1, -1, 'test', 3, -1, None, -1, 0, 'test', False]

        # Обработка списка
        counts, unique = process_list(source_data)

        # Вывод результатов
        print("Количество повторений:")
        for key, count in counts.items():
            item = key[1]  # Извлекаем оригинальное значение из кортежа
            print(f"{item!r}: {count}")

        print()
        print("Список без повторений:")
        print(unique)
        
    except Exception as e:
        print(f"Произошла ошибка: {e}", file=sys.stderr)
