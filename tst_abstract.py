"""

State: спать, сидеть, action. Экшен у каждого типа животного свой.

* Важно, если животное находится в действии, 
то оно не может лечь спать сразу без остановки, ему сначала надо сесть, и наоборот.

1.
кошка - мяукает
кенгуру - прыгает
собака - лает

2. дописать интерфейс

3. добавить реализацию протокола


from typing import Protocol

class AniLink(Protocol):
  def connect(self, animal: Animal) -> animal: Animal:
    ...
  def disconnect(self, uniq_name: str) -> None:
    ...
  def get_state(self, uniq_name: str) -> state: str:
    ... 
  def set_state(self, uniq_name: str, state: str) -> state: str:
    ... # дописать код для перевода животного между состояниями
"""
from typing import Protocol, Dict

class Animal:
    """Класс, представляющий животное с уникальным именем и действием."""
    
    def __init__(self, uniq_name: str, action: str):
        """
        Инициализирует экземпляр животного.
        
        Args:
            uniq_name: Уникальное имя животного (например, 'собака').
            action: Уникальное действие животного (например, 'лает').
        """
        self.uniq_name = uniq_name
        self.state = 'спать'
        self.action = action


class AniLink(Protocol):
    """Интерфейс для работы с животными."""
    
    def connect(self, animal: Animal) -> None:
        """
        Добавляет животное в систему.
        
        Args:
            animal: Экземпляр животного для добавления.
        """
        ...

    def disconnect(self, uniq_name: str) -> None:
        """
        Удаляет животное из системы.
        
        Args:
            uniq_name: Уникальное имя животного для удаления.
        """
        ...

    def get_state(self, uniq_name: str) -> str:
        """
        Возвращает текущее состояние животного.
        
        Args:
            uniq_name: Уникальное имя животного.
            
        Returns:
            Текущее состояние животного или сообщение об ошибке.
        """
        ...

    def set_state(self, uniq_name: str, state: str) -> str:
        """
        Устанавливает новое состояние животного с учетом правил переходов.
        
        Args:
            uniq_name: Уникальное имя животного.
            state: Новое состояние для установки.
            
        Returns:
            Установленное состояние или сообщение об ошибке.
        """
        ...


class MyAniLink(AniLink):
    """Реализует протокол для управления животными через словарь."""
    
    def __init__(self):
        """
        Инициализирует хранилище данных о животных.
        
        Attributes:
            link_data: Словарь для хранения данных о животных в формате:
                      {имя_животного: {'state': состояние, 'action': действие}}.
        """
        self.link_data: Dict[str, Dict[str, str]] = {}

    def connect(self, animal: Animal) -> None:
        """
        Добавляет животное в систему с помощью метода update()
        корректнее, чем реализация через
        self.link_data[animal.uniq_name] = {
        'state': animal.state,
        'action': animal.action
    }.
        
        Args:
            animal: Экземпляр животного для добавления.
        """
        self.link_data.update({
            animal.uniq_name: {'state': animal.state, 'action': animal.action}
        })

    def disconnect(self, uniq_name: str) -> None:
        """
        Удаляет животное из системы с помощью метода pop().
        Безопаснее реализации через del self.link_data[uniq_name] + позволяет обработать значение после, если нужно.
        Args:
            uniq_name: Уникальное имя животного для удаления.
        """
        self.link_data.pop(uniq_name, None)

    def get_state(self, uniq_name: str) -> str:
        """
        Возвращает текущее состояние животного с помощью метода get().
        короче и безопаснее, чем через
        if uniq_name in self.link_data:
            return self.link_data[uniq_name]['state']
        return "Животное не найдено"

        Args:
            uniq_name: Уникальное имя животного.
            
        Returns:
            Текущее состояние животного или "Животное не найдено".
        """
        return self.link_data.get(uniq_name, "Животное не найдено")

    def set_state(self, uniq_name: str, state: str) -> str:
        """
        Меняет состояние животного с соблюдением правил переходов.
        
        Args:
            uniq_name: Уникальное имя животного.
            state: Новое состояние для установки (может быть 'спать', 'сидеть', 'action' или специальное действие).
            
        Returns:
            Установленное состояние или сообщение об ошибке.
        """
        data = self.link_data.get(uniq_name)
        if not data:
            return "Животное не найдено"
        else:
            # Получаем данные животного
            current_state = data['state']
            saved_action = data['action']

            # Обработка специального состояния "action"
            new_state = saved_action if state == "action" else state
        
        # Определяем базовые группы состояний для проверки переходов
        def get_base_state(st: str) -> str:
            """
            Определяет базовую группу состояния.
            
            Args:
                st: Конкретное состояние животного.
                
            Returns:
                Базовая группа: 'action' для уникальных действий, иначе исходное состояние.
            """
            return "action" if st == saved_action else st
        
        current_base = get_base_state(current_state)
        new_base = get_base_state(new_state)
        
        # Проверка некорректных переходов
        if (current_base == "спать" and new_base == "action") or \
           (current_base == "action" and new_base == "спать"):
            return "переход невозможен"
        
        # Проверка допустимых состояний
        allowed_states = ["спать", "сидеть", saved_action]
        if new_state not in allowed_states:
            return "ошибка: недопустимое состояние"
        
        # Обновляем состояние с помощью метода update()
        data.update({'state': new_state})
        return new_state


# Пример использования
if __name__ == "__main__":
    dog = Animal('собака', 'лает')
    cat = Animal('кошка', 'мяукает')
    kangaroo = Animal('кенгуру', 'прыгает')

    link = MyAniLink()

    # Подключаем животных
    link.connect(dog)
    link.connect(cat)
    link.connect(kangaroo)

    # Проверяем начальное состояние
    print(link.get_state('собака'))  # спит

    # Корректные переходы
    print(link.set_state('собака', 'сидеть'))  # сидит
    print(link.set_state('собака', 'лает'))  # лает (действие)

    # Некорректный переход (действие -> сон)
    print(link.set_state('собака', 'спать'))  # переход невозможен

    # Корректный переход через сидение
    print(link.set_state('собака', 'сидеть'))  # сидит
    print(link.set_state('собака', 'спать'))  # спит

    # Некорректный переход (сон -> действие)
    print(link.set_state('собака', 'лает'))  # переход невозможен

    # Используем общее состояние "action"
    print(link.set_state('кошка', 'action'))  # мяукает
    print(link.set_state('кенгуру', 'action'))  # прыгает

    # Отключаем животное
    link.disconnect('собака')
    print(link.get_state('собака'))  # Животное не найдено

    # Проверка смены состояния не существующего животного
    print(link.set_state('чупакабра', 'action'))
