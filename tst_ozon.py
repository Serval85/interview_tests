from typing import List, Optional


def query(
        events: List[List[int]],
        assets: List[List[str]],
        lim: int = 100
) -> List[List[Optional[int]]]:
    """
    Выполняет операцию левого соединения между таблицами событий и активов,
    возвращает отсортированные ограниченные результаты.

    Эта функция имитирует следующий SQL-запрос:
    SELECT event.id, event.name, asset.id, asset.name
    FROM events AS event LEFT JOIN assets AS asset ON event.asset_id = asset.id
    ORDER BY event.id
    LIMIT 100

    Args:
        events: Список записей событий, каждая запись — список формата:
               [id, timestamp, название события, ..., id_актива].
               Поле id_актива может отсутствовать.
        assets: Список записей активов, каждая запись — список формата:
               [id, название актива, ...].

    Returns:
        Отсортированный список объединённых записей следующего формата:
        [[id_события, имя_события, id_актива, имя_актива], ...].
        Возвращается максимум 100 первых записей, отсортированных по полю id_события.
    """
    # Создаем словарь для быстрого поиска активов по идентификатору
    asset_dict = {asset[0]: asset[1] for asset in assets}

    result = []
    for event in events[:lim]:  # Ограничиваем количество обработанных записей заданным лимитом
        event_id = event[0]
        event_name = event[2]
        asset_id = event[3]

        # Получаем имя актива из словаря или None, если такой актив отсутствует
        asset_name = asset_dict.get(asset_id)

        result.append([event_id, event_name, asset_id, asset_name])

    # Сортируем итоговые записи по полю event_id и возвращаем первые 100 элементов
    sorted_result = sorted(result, key=lambda x: x[0])[:100]
    return sorted_result


def print_results(results: List[List[Optional[int]]]) -> None:
    """
    Печатает результат запроса в удобочитаемом виде.

    Args:
        results: Список записей результата, каждая запись имеет формат:
                [id_события, имя_события, id_актива, имя_актива].
    """
    print("ID события | Название события | ID актива | Имя актива")
    print("----------------------------------------")
    for row in results:
        event_id, event_name, asset_id, asset_name = row
        print(f"{event_id:<8} | {event_name:<12} | {str(asset_id):<8} | {str(asset_name):<9}")


# Пример использования функций
if __name__ == "__main__":
    events = [
        [4, '2024-03-28', 'Event 4', 1],
        [1, '2024-03-26', 'Event 1', 1],
        [6, '2024-03-29', 'Event 6', 3],
        [3, '2024-03-28', 'Event 3', 2],
        [5, '2024-03-29', 'Event 5', None],
        [2, '2024-03-27', 'Event 2', None],
    ]

    assets = [
        [4, 'Asset 4'],
        [1, 'Asset 1'],
        [3, 'Asset 3'],
        [2, 'Asset 2'],
    ]

    lim = 100
    # Запускаем выполнение запроса и выводим результат
    query_result = query(events, assets, lim)
    print_results(query_result)