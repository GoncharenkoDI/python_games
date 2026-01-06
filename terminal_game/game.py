import random

SIZE = 5

PLAYER_ICO = "🚶"
TREE_ICO = "🌲"
PRINCESS_ICO = "👸"
SWORD_ICO = "🗡️"
KEY_ICO = "🔑"
DRAGON_ICO = "🐉"


def get_random_place(forest: list) -> list:
    value = random.randint(0, SIZE * SIZE - 1)
    place = list(divmod(value, SIZE))
    while forest[place[0]][place[1]] != TREE_ICO:
        value = random.randint(0, SIZE * SIZE - 1)
        place = list(divmod(value, SIZE))
    return place


def is_border(place: list) -> bool:
    return place[0] == 0 or place[0] == SIZE - 1 or place[1] == 0 or place[1] == SIZE - 1


def get_initial_player_place(forest: list) -> list:
    places = []
    for row in range(SIZE):
        for col in range(SIZE):
            if is_border([row, col]) and forest[row][col] == TREE_ICO:
                places.append([row, col])
    return random.choice(places)


# Створення порожнього лісу
forest = [[TREE_ICO for _ in range(SIZE)] for _ in range(SIZE)]

# визначаємо позиції та розставляємо об'єкти
player = get_initial_player_place(forest)
forest[player[0]][player[1]] = PLAYER_ICO
dragon = get_random_place(forest)
forest[dragon[0]][dragon[1]] = DRAGON_ICO
princess = get_random_place(forest)
forest[princess[0]][princess[1]] = PRINCESS_ICO
sword = get_random_place(forest)
forest[sword[0]][sword[1]] = SWORD_ICO
key = get_random_place(forest)
forest[key[0]][key[1]] = KEY_ICO

has_sword = False
has_key = False
has_princess = False


def show_forest():
    for i in range(SIZE):
        for j in range(SIZE):
            print(forest[i][j], end=" ")
        print()
    print()


def move_player(direction):
    if direction == "w":
        player[0] -= 1
    elif direction == "s":
        player[0] += 1
    elif direction == "a":
        player[1] -= 1
    elif direction == "d":
        player[1] += 1


def inside_forest():
    return 0 <= player[0] < SIZE and 0 <= player[1] < SIZE


print("🌲 Ви зайшли в ліс")
print("Керування: w/a/s/d")

while True:
    show_forest()
    move = input("Ваш хід: ").lower()
    move_player(move)

    # Вийшов з лісу
    if not inside_forest():
        if has_princess:
            print("🏆 Ви вийшли з лісу з Принцесою! Перемога!")
        else:
            print("❌ Ви вийшли з лісу без Принцеси. Поразка.")
        break

    cell = forest[player[0]][player[1]]

    if cell == "К":
        has_key = True
        forest[player[0]][player[1]] = "."
        print("🔑 Ви знайшли ключ!")

    elif cell == "М":
        has_sword = True
        forest[player[0]][player[1]] = "."
        print("🗡️ Ви знайшли меч!")

    elif cell == "П":
        has_princess = True
        forest[player[0]][player[1]] = "."
        print("👸 Ви забрали Принцесу!")

    elif cell == "Д":
        if has_sword and not has_princess:
            print("🐉 Ви вбили Дракона!")
            forest[player[0]][player[1]] = "."
        else:
            print("💀 Дракон вас з'їв. Гра закінчена.")
            break
