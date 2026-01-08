import random

SIZE = 5

PLAYER_ICO = "🚶"
TREE_ICO = "🌲"
PRINCESS_ICO = "👸"
SWORD_ICO = "🗡️"
KEY_ICO = "🔑"
DRAGON_ICO = "🐉"


def get_random_place(forest: list) -> tuple:
    value = random.randint(0, SIZE * SIZE - 1)
    place = divmod(value, SIZE)
    while forest[place[0]][place[1]] != TREE_ICO:
        value = random.randint(0, SIZE * SIZE - 1)
        place = divmod(value, SIZE)
    return place


def is_border(place: tuple) -> bool:
    return place[0] == 0 or place[0] == SIZE - 1 or place[1] == 0 or place[1] == SIZE - 1


def get_initial_player_place(forest: list) -> tuple:
    places = []
    for row in range(SIZE):
        for col in range(SIZE):
            if is_border((row, col)) and forest[row][col] == TREE_ICO:
                places.append((row, col))
    return random.choice(places)


def show_forest(forest:list[list[str]]):
    for i in range(SIZE):
        for j in range(SIZE):
            print(forest[i][j], end=" ")
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


def place_forest_item(forest: list[list[str]], item_ico: str ):
    # УВАГА!!! Щоб не плодити великі структури змінюємо наявний список forest
    place = get_random_place(forest)
    forest[place[0]][place[1]] = item_ico


if __name__ == '__main__':

    # Створення порожнього лісу
    forest = [[TREE_ICO for _ in range(SIZE)] for _ in range(SIZE)]

    # визначаємо позиції та розставляємо об'єкти
    player = get_initial_player_place(forest)
    forest[player[0]][player[1]] = PLAYER_ICO
    place_forest_item(forest, DRAGON_ICO)
    place_forest_item(forest, PRINCESS_ICO)
    place_forest_item(forest, SWORD_ICO)
    place_forest_item(forest, KEY_ICO)

    has_sword = False
    has_key = False
    has_princess = False

    print("🌲 Ви зайшли в ліс")
    print("Керування: w/a/s/d")

    while True:
        show_forest(forest)
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

        cell = forest[player[0]][player[1]]

        if cell == KEY_ICO:
            has_key = True
            forest[player[0]][player[1]] = TREE_ICO
            print("🔑 Ви знайшли ключ!")

        elif cell == SWORD_ICO:
            has_sword = True
            forest[player[0]][player[1]] = TREE_ICO
            print("🗡️ Ви знайшли меч!")

        elif cell == PRINCESS_ICO and has_key:
            has_princess = True
            forest[player[0]][player[1]] = TREE_ICO
            print("👸 Ви забрали Принцесу!")

        elif cell == DRAGON_ICO:
            if has_sword and not has_princess:
                print("🐉 Ви вбили Дракона!")
                forest[player[0]][player[1]] = TREE_ICO
            else:
                print("💀 Дракон вас з'їв. Гра закінчена.")
                break

        forest[old_place[0]][old_place[1]] = TREE_ICO
        forest[player[0]][player[1]] = PLAYER_ICO

