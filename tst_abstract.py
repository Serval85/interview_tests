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
    """Класс, представляющий животное с уникальным именем и действием"""
    
    def __init__(self, uniq_name: str, action: str):
        """
        Инициализирует экземпляр животного
        
        Args:
            uniq_name: Уникальное имя животного (например, 'собака')
            action: Уникальное действие животного (например, 'лает')
        """
        self.uniq_name = uniq_name
        self.state = 'спать'
        self.action = action

class AniLink(Protocol):
    """Протокол (интерфейс) для работы с животными"""
    
    def connect(self, animal: Animal) -> None:
        """
        Добавляет животное в систему
        
        Args:
            animal: Экземпляр животного для добавления
        """
        ...
        
    def disconnect(self, uniq_name: str) -> None:
        """
        Удаляет животное из системы
        
        Args:
            uniq_name: Уникальное имя животного для удаления
        """
        ...
        
    def get_state(self, uniq_name: str) -> str:
        """
        Возвращает текущее состояние животного
        
        Args:
            uniq_name: Уникальное имя животного
            
        Returns:
            Текущее состояние животного или сообщение об ошибке
        """
        ... 
        
    def set_state(self, uniq_name: str, state: str) -> str:
        """
        Изменяет состояние животного с проверкой правил перехода
        
        Args:
            uniq_name: Уникальное имя животного
            state: Новое состояние для установки (может быть 'спать', 'сидеть', 
                   'action' или конкретное действие животного)
                   
        Returns:
            Установленное состояние или сообщение об ошибке
        """
        ...

class MyAniLink(AniLink):
    """Реализация интерфейса для управления животными"""
    
    def __init__(self):
        """
        Инициализирует хранилище данных о животных
        
        Attributes:
            link_data: Словарь для хранения данных о животных в формате:
                {имя_животного: {'state': состояние, 'action': действие}}
        """
        self.link_data: Dict[str, Dict[str, str]] = {}
      
    def connect(self, animal: Animal) -> None:
        """
        Добавляет животное в систему
        
        Args:
            animal: Экземпляр животного для добавления
        """
        self.link_data[animal.uniq_name] = {
            'state': animal.state,
            'action': animal.action
        }
        
    def disconnect(self, uniq_name: str) -> None:
        """
        Удаляет животное из системы
        
        Args:
            uniq_name: Уникальное имя животного для удаления
        """
        if uniq_name in self.link_data:
            del self.link_data[uniq_name]
            
    def get_state(self, uniq_name: str) -> str:
        """
        Возвращает текущее состояние животного
        
        Args:
            uniq_name: Уникальное имя животного
            
        Returns:
            Текущее состояние животного или "Животное не найдено"
        """
        if uniq_name in self.link_data:
            return self.link_data[uniq_name]['state']
        return "Животное не найдено"
    
    def set_state(self, uniq_name: str, state: str) -> str:
        """
        Изменяет состояние животного с проверкой правил перехода
        
        Правила переходов:
        1. Из 'спать' нельзя сразу перейти в действие (action)
        2. Из действия (action) нельзя сразу перейти в 'спать'
        3. Разрешены только состояния: 'спать', 'сидеть' и уникальное действие животного
        4. Состояние 'action' автоматически заменяется на уникальное действие животного
        
        Args:
            uniq_name: Уникальное имя животного
            state: Новое состояние для установки (может быть базовым состоянием 
                   или специальным значением 'action')
                   
        Returns:
            Установленное состояние или сообщение об ошибке:
            - "Животное не найдено" - если животное не подключено
            - "переход невозможен" - при нарушении правил переходов
            - "ошибка: недопустимое состояние" - при попытке установить недопустимое состояние
        """
        # Проверка существования животного
        if uniq_name not in self.link_data:
            return "Животное не найдено"
            
        # Получаем данные животного
        data = self.link_data[uniq_name]
        current_state = data['state']
        saved_action = data['action']
        
        # Обработка специального состояния "action"
        new_state = saved_action if state == "action" else state
        
        # Определяем базовые группы состояний для проверки переходов
        def get_base_state(st: str) -> str:
            """
            Определяет базовую группу состояния
            
            Args:
                st: Конкретное состояние животного
                
            Returns:
                Базовую группу: 'action' для уникальных действий, 
                иначе исходное состояние
            """
            return "action" if st == saved_action else st
        
        current_base = get_base_state(current_state)
        new_base = get_base_state(new_state)
        
        # Проверка некорректных переходов
        if (current_base == "спать" and new_base == "action") or \
           (current_base == "action" and new_base == "спать"):
            return "переход невозможен"
        
        # Проверка допустимости состояния
        allowed_states = ["спать", "сидеть", saved_action]
        if new_state not in allowed_states:
            return "ошибка: недопустимое состояние"
        
        # Обновляем состояние
        data['state'] = new_state
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
    print(link.get_state('собака'))  # спать

    # Корректные переходы
    print(link.set_state('собака', 'сидеть'))  # сидеть
    print(link.set_state('собака', 'лает'))    # лает (action)
    
    # Некорректный переход (action -> спать)
    print(link.set_state('собака', 'спать'))   # переход невозможен
    
    # Корректный переход через сидеть
    print(link.set_state('собака', 'сидеть'))  # сидеть
    print(link.set_state('собака', 'спать'))   # спать

    # Некорректный переход (спать -> action)
    print(link.set_state('собака', 'лает'))    # переход невозможен

    # Использование общего состояния "action"
    print(link.set_state('кошка', 'action'))   # мяукает
    print(link.set_state('кенгуру', 'action')) # прыгает

    # Отключаем животное
    link.disconnect('собака')
    print(link.get_state('собака'))  # Животное не найдено
