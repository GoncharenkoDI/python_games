import os
import random
from enum import IntEnum, StrEnum


class Icon(StrEnum):
    PLAYER =   "🚶"
    TREE =     "🌲"
    PRINCESS = "👸"
    SWORD =    "🗡️"
    KEY   =    "🔑"
    DRAGON =   "🐉"


class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class CheckPlaceResult(IntEnum):
    CONTINUE = 0
    OUT_WITH_PRINCESS = 1
    OUT_WITHOUT_PRINCESS = 2
    FIND_KEY = 3
    FIND_SWORD = 4
    KILLED_DRAGON = 5
    ATE_PLAYER = 6
    ATE_PRINCESS = 7
    FIND_PRINCESS = 8
    GET_PRINCESS = 9


result_message: dict[CheckPlaceResult, str] = {
    CheckPlaceResult.CONTINUE: "",  # CONTINUE = 0
    CheckPlaceResult.OUT_WITH_PRINCESS: "Перемога!!! Ви врятували принцесу",  # OUT_WITH_PRINCESS = 1
    CheckPlaceResult.OUT_WITHOUT_PRINCESS: "Поразка!!! Ви не врятували принцесу!",  # OUT_WITHOUT_PRINCESS = 2
    CheckPlaceResult.FIND_KEY: "Ви знайшли ключ!",  # FIND_KEY = 3
    CheckPlaceResult.FIND_SWORD: "Ви знайшли меч!",  # FIND_SWORD = 4
    CheckPlaceResult.KILLED_DRAGON: "Ви вбили дракона!",  # KILLED_DRAGON = 5
    CheckPlaceResult.ATE_PLAYER: "Поразка!!! Вас з'їв дракон!",  # ATE_PLAYER = 6
    CheckPlaceResult.ATE_PRINCESS: "Поразка!!! Дракон з'їв принцесу",  # ATE_PRINCESS = 7
    CheckPlaceResult.FIND_PRINCESS: "Ви знайшли принцесу, але у Вас немає ключа!",  # FIND_PRINCESS = 8
    CheckPlaceResult.GET_PRINCESS: "Ви звільнили принцесу!"  # GET_PRINCESS = 9
}


key_directions: dict[str, Direction] = {
    "w": Direction.NORTH,
    "a": Direction.WEST,
    "s": Direction.SOUTH,
    "d": Direction.EAST
}


def show_result(message) -> None:
    print(message)


def get_random_place(size: int, occupied_seats: dict[tuple[int, int], Icon]) -> tuple[int, int]:
    place: tuple[int, int] = divmod(random.randint(0, size * size - 1), size)
    while place in occupied_seats:
        place = divmod(random.randint(0, size * size - 1), size)
    return place


def is_forest_border(size: int, place: tuple[int, int]) -> bool:
    return place[0] == 0 or place[0] == size - 1 or place[1] == 0 or place[1] == size - 1


def get_initial_player_place(size: int, occupied_seats: dict[tuple[int, int], Icon]) -> tuple[int, int]:
    """ отримання початкової позиції гравця в лісі (повинна бути на границі лісу та не зайнята"""
    places: list[tuple[int, int]] = []
    for row in range(size):
        for col in range(size):
            place = (row, col)
            if is_forest_border(size, place) and place not in occupied_seats:
                places.append(place)
    return random.choice(places)


def in_forest(size: int, place: tuple[int, int]) -> bool:
    return size > place[0] >= 0 and size > place[1] >= 0


def show_player_info(message: str, player_place: tuple[int, int], has_princess: bool,
                     has_sword: bool, has_key: bool) -> None:
    print(message)
    info_str = f"Ваші координати: {player_place}"

    state_str = " Ви маєте ключ!" if has_key else ""
    state_str = " ".join([state_str, "Ви маєте меч!" if has_sword else ""])
    state_str = " ".join([state_str, "З вами принцеса!" if has_princess else ""])
    print(info_str, state_str)


def get_key_input(prompt: str, valid_keys: list[str]) -> str:
    key: str = ""
    while key not in valid_keys:
        key = input(f"{prompt} (управління клавішами {' | '.join(valid_keys)}): ").lower()
    return key


def show_forest(size: int, player: tuple[int, int], occupied_seats: dict[tuple[int, int], Icon]) -> None:
    for row in range(size):
        for column in range(size):
            print(occupied_seats.get((row, column), Icon.TREE), end="")
            # print(Icon.PLAYER.value if (row, column) == player else Icon.TREE.value, end=" ")
        print(" ")
    print()


def next_step(place: tuple[int, int], direct: Direction) -> tuple[int, int]:
    directions_action = {
        Direction.NORTH: lambda old_place: (old_place[0] - 1, old_place[1]),
        Direction.SOUTH: lambda old_place: (old_place[0] + 1, old_place[1]),
        Direction.WEST: lambda old_place: (old_place[0], old_place[1] - 1),
        Direction.EAST: lambda old_place: (old_place[0], old_place[1] + 1)
    }
    return directions_action[direct](place)


def check_place(
        size: int,
        place: tuple[int, int],
        occupied_seats: dict[tuple[int, int], Icon],
        has_princess: bool,
        has_sword: bool,
        has_key: bool
) -> CheckPlaceResult:
    if not in_forest(size, place) and has_princess:
        return CheckPlaceResult.OUT_WITH_PRINCESS
    if not in_forest(size, place) and not has_princess:
        return CheckPlaceResult.OUT_WITHOUT_PRINCESS

    item = occupied_seats.get(place, Icon.TREE)

    if (item == Icon.DRAGON) and has_princess:
        return CheckPlaceResult.ATE_PRINCESS
    if item == Icon.DRAGON and not has_sword:
        return CheckPlaceResult.ATE_PLAYER
    if item == Icon.DRAGON:
        return CheckPlaceResult.KILLED_DRAGON
    if item == Icon.PRINCESS and has_key:
        return CheckPlaceResult.GET_PRINCESS
    if item == Icon.PRINCESS and not has_key:
        return CheckPlaceResult.FIND_PRINCESS
    if item == Icon.KEY:
        return CheckPlaceResult.FIND_KEY
    if item == Icon.SWORD:
        return CheckPlaceResult.FIND_SWORD

    return CheckPlaceResult.CONTINUE


if __name__ == '__main__':

    new_game: bool = True
    while new_game:
        end_of_game: bool = False
        SIZE: int = 5
        # Словник зайнятих місць в лісі у вигляді пар координати: іконка об'єкта,
        # наприклад: {(0,1): Icon.PLAYERб, (2,4): Icon.DRAGON, ...}
        occupied_seats: dict[tuple[int, int], Icon] = {}
        player_place: tuple[int, int] = get_initial_player_place(SIZE, occupied_seats)
        ## розставляємо об'єкти в лісі
        occupied_seats[player_place] = Icon.PLAYER
        occupied_seats[get_random_place(SIZE, occupied_seats)] = Icon.DRAGON
        occupied_seats[get_random_place(SIZE, occupied_seats)] = Icon.KEY
        occupied_seats[get_random_place(SIZE, occupied_seats)] = Icon.SWORD
        occupied_seats[get_random_place(SIZE, occupied_seats)] = Icon.PRINCESS

        old_item = Icon.TREE
        message = "Ви зайшли в ліс"
        has_princess: bool = False
        has_sword: bool = False
        has_key: bool = False

        while not end_of_game:

            os.system('cls' if os.name == 'nt' else 'clear')
            show_player_info(message, player_place, has_princess,
                             has_sword, has_key)
            show_forest(SIZE, player_place, occupied_seats)
            direction: Direction = key_directions[get_key_input(
                "Оберіть напрямок наступного кроку",
                list(key_directions))]

            old_player_place = player_place
            player_place = next_step(old_player_place, direction)
            check_place_result: CheckPlaceResult = check_place(
                SIZE, player_place, occupied_seats, has_princess, has_sword, has_key)
            has_princess = has_princess or check_place_result == CheckPlaceResult.GET_PRINCESS
            has_sword = has_sword or check_place_result == CheckPlaceResult.FIND_SWORD
            has_key = has_key or check_place_result == CheckPlaceResult.FIND_KEY
            del occupied_seats[old_player_place]
            if old_item == Icon.PRINCESS and not has_princess:
                occupied_seats[old_player_place] = Icon.PRINCESS
            old_item = occupied_seats.get(player_place, Icon.TREE)
            occupied_seats[player_place] = Icon.PLAYER
            message = result_message[check_place_result]
            end_of_game = check_place_result in (
                CheckPlaceResult.ATE_PRINCESS, CheckPlaceResult.ATE_PLAYER,
                CheckPlaceResult.OUT_WITH_PRINCESS, CheckPlaceResult.OUT_WITHOUT_PRINCESS)

        os.system('cls' if os.name == 'nt' else 'clear')
        show_result(message)
        new_game = get_key_input(
            "Для виходу натисніть q, для нової гри - n",
            ["q", "n"]) != "q"
