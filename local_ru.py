import random
text = """В мире Аэтер, где магия переплетается с реальностью, древний артефакт, известный как Сердце Мира, был разбит на три осколка. Это привело к дисбалансу магических сил и породило хаос. Трое героев, наделённых уникальными магическими способностями, избраны судьбой, чтобы отыскать осколки и восстановить Сердце Мира.

Эйдан: Мастер стихийной магии, способный управлять огнём, водой и землёй. Он стремится восстановить баланс в мире.
Лира: Искусная целительница и знаток тайных искусств, владеющая магией света. Её цель – исцелить раны Аэтера.
Реган: Загадочный странник, владеющий магией тени и иллюзий. Его мотивы остаются скрытыми.

Их путь лежит через опасные земли, полные загадок и испытаний. Судьба Аэтера зависит от их успеха. Сможет ли кто-нибудь из них собрать все три осколка и спасти Аэтер?"""

print(text)
ACTIVE_HERO = "Эйдан"

heroes = {
    "Эйдан": {"здоровье": 100, "магия": 100, "осколки": 0},
    "Лира": {"здоровье": 80, "магия": 120, "осколки": 0},
    "Реган": {"здоровье": 90, "магия": 110, "осколки": 0},
}

hero_list = list(heroes.keys())

# Словарь для отслеживания пройденных локаций
completed_locations = {hero: set() for hero in heroes}

resources = {
    "кристаллы": 10,
    "зелья": 3,
    "золото": 50,
}

# Количество попыток
remaining_moves = 6

# Функции игры
def print_status():
    print("\n--- Текущее состояние ---")
    print(f"Осталось попыток: {remaining_moves}")
    for hero, stats in heroes.items():
        print(f"{hero}: Здоровье - {stats['здоровье']}, Магия - {stats['магия']}, Осколки - {stats['осколки']}")
    print(f"Ресурсы: {resources}")

def choose_path(hero_name):
    print(f"\n{hero_name}, выберите путь:")
    print("1. Древний лес")
    print("2. Заброшенный город")
    print("3. Вершины гор")
    while True:
        choice = input("> ")
        if choice in ["1", "2", "3"]:
            return choice
        print("Неверный выбор. Введите 1, 2 или 3")

def test_wisdom():
    print("\nДревние стражи задают загадку:")
    print("Что имеет города, горы и реки, но не имеет домов, деревьев и воды?")
    answer = input("Ваш ответ: ").lower()
    if answer == "карта":
        print("Правильно! Вы получаете осколок.")
        return True
    print("Неверно! Страж атакует!")
    heroes[ACTIVE_HERO]["здоровье"] -= 20
    return False

def test_tragedy():
    print('\nИзвержение вулкана! Ваши действия:')
    print('1. Бежать')
    print('2. Использовать магию')
    print('3. Застыть в оцепенении')
    choice = input("> ")
    
    if choice == "1":
        heroes[ACTIVE_HERO]["здоровье"] -= 30
        print('Спаслись, но получили ранения. Получаете осколок.')
        return True
    elif choice == "2":
        if heroes[ACTIVE_HERO]["магия"] >= 40:
            heroes[ACTIVE_HERO]["магия"] -= 40
            print('Создали магический щит! Получаете осколок.')
            return True
        print('Недостаточно магии! Получили урон.')
        heroes[ACTIVE_HERO]["здоровье"] -= 50
        return False
    elif choice == "3":
        print('Погибли в лаве...')
        heroes[ACTIVE_HERO]["здоровье"] = 0
        return False
    print("Неверный выбор!")
    return False

def test_forest_fairy():
    print('\nФея просит решить 3 предела:')
    correct = 0
    
    if int(input('lim((1 - cosx)/x) при x→0: ')) == 0:
        correct += 1
    if int(input('lim((arcsinx)/x) при x→0: ')) == 1:
        correct += 1
    if int(input('lim((ln(1 + x))/x) при x→0: ')) == 1:
        correct += 1
    
    if correct == 3:
        print('Все верно! Получаете осколок!')
        return True
    
    print(f'Правильных ответов: {correct}/3. Фея разочарована...')
    return False

def trade_with_nomads():
    print("\nВы встретили кочевников. Ваши действия:")
    print("1. Купить зелье (10 золота)")
    print("2. Получить информацию (5 золота)")
    print("3. Уйти")

    choice = input("> ")
    
    if heroes[ACTIVE_HERO]["здоровье"] <= 0:
        print(f"{ACTIVE_HERO} не может торговать - персонаж мёртв!")
        return
    
    if choice == "1" and resources["золото"] >= 10:
        resources["зелья"] += 1
        resources["золото"] -= 10
        print("Купили зелье.")
    elif choice == "2" and resources["золото"] >= 5:
        resources["золото"] -= 5
        print("Кочевники дали совет.")
    else:
        print("Ушли.")

def combat(enemy_name, enemy_health):
    print(f"\nНа вас напал {enemy_name} ({enemy_health} HP)!")
    
    while heroes[ACTIVE_HERO]["здоровье"] > 0 and enemy_health > 0:
        print(f"\n{ACTIVE_HERO}: Здоровье {heroes[ACTIVE_HERO]['здоровье']}")
        print(f"{enemy_name}: Здоровье {enemy_health}")
        print("1. Атаковать")
        print("2. Использовать зелье (+20 HP)")

        action = input("> ")
        
        if action == "1":
            damage = random.randint(10, 20)
            enemy_health -= damage
            print(f"Нанесли {damage} урона!")
        elif action == "2" and resources["зелья"] > 0:
            heroes[ACTIVE_HERO]["здоровье"] += 20
            resources["зелья"] -= 1
            print("Здоровье восстановлено!")
        else:
            print("Неверный выбор или нет зелий.")

        if enemy_health > 0:
            damage = random.randint(5, 15)
            heroes[ACTIVE_HERO]["здоровье"] -= damage
            print(f"{enemy_name} нанес {damage} урона!")

    if heroes[ACTIVE_HERO]["здоровье"] > 0:
        print(f"Победили {enemy_name}!")
        return True
    
    print("Проиграли...")
    return False

def random_event():
    events = [
        ("Магический шторм", lambda: [print("Потеряли 5 золота!"), resources.update({"золото": max(0, resources["золото"] - 5)})]),
        ("Нашли клад", lambda: [print("+10 золота!"), resources.update({"золото": resources["золото"] + 10})]),
        ("Нападение гоблинов", lambda: combat("Гоблин", 50)),
        ("Встреча с кочевниками", trade_with_nomads)
    ]
    
    if heroes[ACTIVE_HERO]["здоровье"] <= 0:
        print(f"{ACTIVE_HERO} не может участвовать в событиях - персонаж мёртв!")
        return
    
    event = random.choice(events)
    print(f"\nСобытие: {event[0]}")
    event[1]()

def main_game_loop():
    print("=== Игра 'Сердце Аэтера' ===")
    print("Соберите 3 осколка, чтобы спасти мир!")
    
    global ACTIVE_HERO, remaining_moves
    
    while remaining_moves > 0:
        # Проверяем условия победы
        if any(hero["осколки"] >= 3 for hero in heroes.values()):
            winner = [name for name, stats in heroes.items() if stats["осколки"] >= 3][0]
            print("\n=== Игра окончена ===")
            print(f"ПОБЕДА! {winner} собрал 3 осколка!")
            return
        
        # Проверяем есть ли живые герои
        if all(hero["здоровье"] <= 0 for hero in heroes.values()):
            print("\n=== Игра окончена ===")
            print("Поражение... Все герои погибли.")
            return
        
        print_status()
        
        for hero_name in hero_list:
            ACTIVE_HERO = hero_name
            
            if heroes[ACTIVE_HERO]["здоровье"] <= 0:
                print(f"\n{ACTIVE_HERO} не может действовать!")
                continue
                
            print(f"\n--- Ход {ACTIVE_HERO} ---")
            
            # Герой выбирает свой путь
            path = choose_path(ACTIVE_HERO)
            
            # Проверяем, проходил ли герой эту локацию и получал ли осколок
            if path in completed_locations[ACTIVE_HERO]:
                print(f"{ACTIVE_HERO} уже проходил это испытание и получал осколок. Пропускаем.")
                continue
                
            if path == "1":
                if test_forest_fairy():
                    heroes[ACTIVE_HERO]["осколки"] += 1
                    completed_locations[ACTIVE_HERO].add(path)
            elif path == "2":
                if test_wisdom():
                    heroes[ACTIVE_HERO]["осколки"] += 1
                    completed_locations[ACTIVE_HERO].add(path)
            elif path == "3":
                if test_tragedy():
                    heroes[ACTIVE_HERO]["осколки"] += 1
                    completed_locations[ACTIVE_HERO].add(path)
            
            # Проверяем победу после каждого действия
            if heroes[ACTIVE_HERO]["осколки"] >= 3:
                print("\n=== Игра окончена ===")
                print(f"ПОБЕДА! {ACTIVE_HERO} собрал 3 осколка!")
                return
            
            random_event()
        
        remaining_moves -= 1
        print("\n=== Конец раунда ===")

    print("\n=== Игра окончена ===")
    print("Поражение... Время вышло.")

# Запуск игры
if __name__ == "__main__":
    main_game_loop()
