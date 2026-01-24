from my_game import *


def init_game(size: int):
    global occupied_seats, player_place, old_item, message, has_princess, has_sword, has_key

    # Словник зайнятих місць в лісі у вигляді пар координати: іконка об'єкта,
    # наприклад: {(0,1): Icon.PLAYERб, (2,4): Icon.DRAGON, ...}
    occupied_seats = {}
    player_place = get_initial_player_place(size, occupied_seats)
    ## розставляємо об'єкти в лісі
    occupied_seats[player_place] = Icon.PLAYER
    occupied_seats[get_random_place(size, occupied_seats)] = Icon.DRAGON
    occupied_seats[get_random_place(size, occupied_seats)] = Icon.KEY
    occupied_seats[get_random_place(size, occupied_seats)] = Icon.SWORD
    occupied_seats[get_random_place(size, occupied_seats)] = Icon.PRINCESS

    old_item = Icon.TREE
    message = "Ви зайшли в ліс"
    has_princess = False
    has_sword = False
    has_key = False


def move(size: int) -> bool:
    global player_place, occupied_seats, has_princess, has_sword, has_key, old_item, message
    direction: Direction = key_directions[get_key_input(
        "Оберіть напрямок наступного кроку",
        list(key_directions))]

    old_player_place = player_place
    player_place = next_step(old_player_place, direction)
    check_place_result: CheckPlaceResult = check_place(
        size, player_place, occupied_seats, has_princess, has_sword, has_key)
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
    return end_of_game


if __name__ == '__main__':
    new_game: bool = True
    SIZE:int = 8
    while new_game:
        end_of_game: bool = False
        init_game(SIZE)
        while not end_of_game:
            os.system('cls' if os.name == 'nt' else 'clear')
            show_player_info(message, player_place, has_princess,
                             has_sword, has_key)
            show_forest(SIZE, player_place, occupied_seats)

            end_of_game = move(SIZE)

        os.system('cls' if os.name == 'nt' else 'clear')
        show_result(message)
        new_game = get_key_input(
            "Для виходу натисніть q, для нової гри - n",
            ["q", "n"]) != "q"
