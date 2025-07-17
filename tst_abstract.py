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

from typing import Protocol, Dict, Union

class Animal:
    def __init__(self, uniq_name: str, action: str):
        self.uniq_name = uniq_name
        self.state = 'спать'
        self.action = action  # Уникальное действие для животного

class AniLink(Protocol):
    def connect(self, animal: Animal) -> None:
        ...
    def disconnect(self, uniq_name: str) -> None:
        ...
    def get_state(self, uniq_name: str) -> str:
        ... 
    def set_state(self, uniq_name: str, state: str) -> str:
        ...  # Должен учитывать правила переходов

class MyAniLink(AniLink):
    def __init__(self):
        # Храним данные в формате: 
        # {uniq_name: {'state': текущее состояние, 'action': уникальное действие}}
        self.link_data: Dict[str, Dict[str, str]] = {}
      
    def connect(self, animal: Animal) -> None:
        self.link_data[animal.uniq_name] = {
            'state': animal.state,
            'action': animal.action
        }
        
    def disconnect(self, uniq_name: str) -> None:
        if uniq_name in self.link_data:
            del self.link_data[uniq_name]
            
    def get_state(self, uniq_name: str) -> str:
        if uniq_name in self.link_data:
            return self.link_data[uniq_name]['state']
        return "Животное не найдено"
    
    def set_state(self, uniq_name: str, state: str) -> str:
        if uniq_name not in self.link_data:
            return "Животное не найдено"
            
        data = self.link_data[uniq_name]
        current_state = data['state']
        saved_action = data['action']
        
        # Обработка состояния "action" - заменяем на конкретное действие животного
        new_state = saved_action if state == "action" else state
        
        # Определяем базовые группы состояний
        current_base = self._get_base_state(current_state, saved_action)
        new_base = self._get_base_state(new_state, saved_action)
        
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
    
    def _get_base_state(self, state: str, action: str) -> str:
        """Определяет базовую группу состояния (для проверки переходов)"""
        if state == action:
            return "action"
        return state

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
