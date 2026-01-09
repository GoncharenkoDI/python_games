import random

SIZE = 5

PLAYER_ICO = "🚶"
TREE_ICO = "🌲"
PRINCESS_ICO = "👸"
SWORD_ICO = "🗡️"
KEY_ICO = "🔑"
DRAGON_ICO = "🐉"


def get_random_place(occupied_seats: dict[tuple, str]) -> tuple:
    place = divmod(random.randint(0, SIZE * SIZE - 1), SIZE)
    while place in occupied_seats:
        place = divmod(random.randint(0, SIZE * SIZE - 1), SIZE)
    return place


def is_border(place: tuple) -> bool:
    return place[0] == 0 or place[0] == SIZE - 1 or place[1] == 0 or place[1] == SIZE - 1


def get_initial_player_place(occupied_seats: dict[tuple, str]) -> tuple:
    """ отримання початкової позиції гравця в лісі (повинна бути на границі лісу та не зайнята"""
    places = []
    for row in range(SIZE):
        for col in range(SIZE):
            place = (row, col)
            if is_border(place) and place not in occupied_seats:
                places.append(place)
    return random.choice(places)


def show_forest(occupied_seats: dict[tuple, str]):
    for row in range(SIZE):
        for column in range(SIZE):
            print(occupied_seats.get((row,column),TREE_ICO), end=" ")
        print()
    print()


def move_player(direction: str, old_place)->tuple:
    directions_action = {
        "w": lambda old_place: (old_place[0] - 1, old_place[1]),
        "s": lambda old_place: (old_place[0] + 1, old_place[1]),
        "a": lambda old_place: (old_place[0], old_place[1] - 1),
        "d": lambda old_place: (old_place[0], old_place[1] + 1)
    }
    return directions_action[direction](old_place)


def inside_forest(place: tuple) -> bool:
    return 0 <= place[0] < SIZE and 0 <= place[1] < SIZE


def place_forest_item(occupied_seats: dict[tuple, str], item_ico: str )->dict[tuple, str]:
    result = occupied_seats.copy()
    place = get_random_place(result)
    result[place] = item_ico
    return result


if __name__ == '__main__':

    # Створення порожнього лісу
    occupied_seats:dict[tuple[int], str] =  {}
    cell: str = TREE_ICO
    # визначаємо позиції та розставляємо об'єкти
    player: tuple[int] = get_initial_player_place(occupied_seats)
    occupied_seats[player] = PLAYER_ICO
    occupied_seats = place_forest_item(occupied_seats, DRAGON_ICO)
    occupied_seats = place_forest_item(occupied_seats, PRINCESS_ICO)
    occupied_seats = place_forest_item(occupied_seats, SWORD_ICO)
    occupied_seats = place_forest_item(occupied_seats, KEY_ICO)

    has_sword: bool = False
    has_key: bool = False
    has_princess: bool = False

    print("🌲 Ви зайшли в ліс")
    print("Керування: w/a/s/d")

    while True:
        show_forest(occupied_seats)
        move:str = input("Ваш хід: ").lower()
        while move not in ("w", "a", "s", "d"):
            move = input("Ваш хід: ").lower()
        old_place = player
        player = move_player(move, old_place)
        # Вийшов з лісу
        if not inside_forest(player):
            if has_princess:
                print("🏆 Ви вийшли з лісу з Принцесою! Перемога!")
            else:
                print("❌ Ви вийшли з лісу без Принцеси. Поразка.")
            break

        if cell == PRINCESS_ICO and not has_princess:
            occupied_seats[old_place] = PRINCESS_ICO
        else:
            del occupied_seats[old_place]

        cell = occupied_seats.get(player)
        occupied_seats[player] = PLAYER_ICO

        if cell == KEY_ICO:
            has_key = True
            print("🔑 Ви знайшли ключ!")

        elif cell == SWORD_ICO:
            has_sword = True
            print("🗡️ Ви знайшли меч!")

        elif cell == PRINCESS_ICO and has_key:
            has_princess = True
            print("👸 Ви забрали Принцесу!")

        elif cell == DRAGON_ICO:
            if has_sword and not has_princess:
                print("🐉 Ви вбили Дракона!")
            else:
                print("💀 Дракон вас з'їв. Гра закінчена.")
                break



