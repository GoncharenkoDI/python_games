SIZE = 5

# Створення порожнього лісу
forest = [["." for _ in range(SIZE)] for _ in range(SIZE)]

# Позиції
player = [0, 0]
dragon = [4, 4]
princess = [2, 2]
sword = [1, 3]
key = [3, 1]

# Розставляємо об'єкти
forest[dragon[0]][dragon[1]] = "Д"
forest[princess[0]][princess[1]] = "П"
forest[sword[0]][sword[1]] = "М"
forest[key[0]][key[1]] = "К"

has_sword = False
has_key = False
has_princess = False


def show_forest():
    for i in range(SIZE):
        for j in range(SIZE):
            if [i, j] == player:
                print("Г", end=" ")
            else:
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
