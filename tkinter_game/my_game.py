import random
import sys
from enum import StrEnum, IntEnum
import tkinter as tk
from tkinter import messagebox
import os
from typing import Literal, Union, Optional


class Icon(StrEnum):
    PLAYER = "🚶"
    TREE = "🌲"
    PRINCESS = "👸"
    SWORD = "🗡️"
    KEY = "🔑"
    DRAGON = "🐉"


class Dirs(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def on_closing():
    if messagebox.askokcancel("Вихід із застосунку", "Хочете вийти із застосунку?"):
        main_window.destroy()


def resource_path(relative_path):
    """Отримує абсолютный шлях до ресурсу, працює для dev та для PyInstaller"""
    try:
        # PyInstaller створює тимчасову теку та зберігає шлях в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def random_place(
    size: int, occupied_seats: dict[tuple[int, int], Icon]
) -> tuple[int, int]:
    place: tuple[int, int] = divmod(random.randint(0, size * size - 1), size)
    while place in occupied_seats:
        place = divmod(random.randint(0, size * size - 1), size)
    return place


def is_forest_border(size: int, place: tuple[int, int]) -> bool:
    return (
        place[0] == 0 or place[0] == size - 1 or place[1] == 0 or place[1] == size - 1
    )


def ini_player_place(
    size: int, occupied_seats: dict[tuple[int, int], Icon]
) -> tuple[int, int]:
    """отримання початкової позиції гравця в лісі (повинна бути на границі лісу та не зайнята"""
    places: list[tuple[int, int]] = []
    for row in range(size):
        for col in range(size):
            place = (row, col)
            if is_forest_border(size, place) and place not in occupied_seats:
                places.append(place)
    return random.choice(places)


def create_images(master: tk.Tk, script_path: str) -> dict[Icon, tk.PhotoImage]:
    images = {
        Icon.PLAYER: tk.PhotoImage(
            master=master, file=os.path.join(script_path, "Prince.png")
        ),
        Icon.TREE: tk.PhotoImage(
            master=master, file=os.path.join(script_path, "tree.png")
        ),
        Icon.PRINCESS: tk.PhotoImage(
            master=master, file=os.path.join(script_path, "Princess.png")
        ),
        Icon.DRAGON: tk.PhotoImage(
            master=master, file=os.path.join(script_path, "Dragon.png")
        ),
        Icon.SWORD: tk.PhotoImage(
            master=master, file=os.path.join(script_path, "Sword.png")
        ),
        Icon.KEY: tk.PhotoImage(
            master=master, file=os.path.join(script_path, "Key.png")
        ),
    }
    return images


def create_btn_ico_images(master: tk.Tk, script_path: str) -> dict[str, tk.PhotoImage]:
    images = {
        "btn_up": tk.PhotoImage(
            master=master, file=os.path.join(script_path, "up-arrow.png")
        ),
        "btn_down": tk.PhotoImage(
            master=master, file=os.path.join(script_path, "down-arrow.png")
        ),
        "btn_left": tk.PhotoImage(
            master=master, file=os.path.join(script_path, "left-arrow.png")
        ),
        "btn_right": tk.PhotoImage(
            master=master, file=os.path.join(script_path, "right-arrow.png")
        ),
    }
    return images


def create_btn(
    master: tk.Frame,
    row: int,
    col: int,
    column_span: int = 0,
    state: Literal["normal", "active", "disabled"] = "normal",
    text: str = "",
    image: Optional[tk.Image] = None,
) -> tk.Button:
    btn = tk.Button(master, state=state)
    if text != "":
        btn["text"] = text
    if image is not None:
        btn["image"] = image
    btn["image"] = image
    btn.grid(row=row, column=col, padx=2, pady=1, columnspan=column_span)
    return btn


def set_fog_of_war(event):
    global forest, SIZE, occupied_seats, images, fog_of_war
    fog_of_war = not fog_of_war
    update_forest(forest, SIZE, occupied_seats, images, fog_of_war)


def in_forest(size: int, place: tuple[int, int]) -> bool:
    return size > place[0] >= 0 and size > place[1] >= 0


def create_forest(size: int, game_panel: tk.Frame) -> list[list[tk.Label]]:
    forest: list[list[tk.Label]] = [
        [
            tk.Label(
                master=game_panel,
                height=FOREST_CELL_SIZE,
                width=FOREST_CELL_SIZE,
                name=f"label_{row}_{col}",
                bg="green",
            )
            for row in range(SIZE)
        ]
        for col in range(SIZE)
    ]
    return forest


def update_forest(
    forest: list[list[tk.Label]],
    size: int,
    occupied_seats: dict[tuple[int, int], Icon],
    images: dict[Icon, tk.PhotoImage],
    fog_of_war: bool,
):
    for row in range(size):
        for col in range(size):
            icon = Icon.TREE
            if (row, col) in occupied_seats:
                if occupied_seats[(row, col)] == Icon.PLAYER:
                    icon = Icon.PLAYER
                elif not fog_of_war:
                    icon = occupied_seats[(row, col)]
            update_forest_cell(forest, (row, col), icon, images)


def update_forest_cell(
    forest: list[list[tk.Label]],
    place: tuple[int, int],
    item: Icon,
    images: dict[Icon, tk.PhotoImage],
):
    cell: tk.Label = forest[place[0]][place[1]]
    cell["image"] = images[item]


def show_forest(forest, size):
    for row in range(size):
        for col in range(size):
            forest[row][col].grid(row=row, column=col)


def show_player_info(
    player: dict[str, Union[tuple[int, int], bool]],
    message: str,
    is_win: Optional[bool] = None,
):
    global player_info
    what_has = ""
    what_has += "\nВи маєте меч." if player["has_sword"] else ""
    what_has += "\nВи маєте ключ." if player["has_key"] else ""
    what_has += "\nЗ вами принцеса." if player["has_princess"] else ""

    info_text = f"{message}\nВаші координати:  {player['place']} {what_has}"
    player_info["text"] = info_text
    title = "Інформація" if is_win is None else "Перемога" if is_win else "Поразка"
    messagebox.showinfo(title, message)
    pass


def start_game(size: int, forest: list[list[tk.Label]]):
    global player, occupied_seats, btn_start, btn_stop, btn_up, btn_right, btn_left, btn_down, old_item, player_info

    # occupied_seats - Словник зайнятих місць в лісі у вигляді пар координати: іконка об'єкта,
    # наприклад: {(0,1): Icon.PLAYER, (2,4): Icon.DRAGON, ...}
    occupied_seats = {}
    place = ini_player_place(size, occupied_seats)
    old_item = Icon.TREE

    player = {
        "place": place,
        "has_sword": False,
        "has_key": False,
        "has_princess": False,
    }

    ## розставляємо об'єкти в лісі
    occupied_seats[place] = Icon.PLAYER
    occupied_seats[random_place(size, occupied_seats)] = Icon.DRAGON
    occupied_seats[random_place(size, occupied_seats)] = Icon.KEY
    occupied_seats[random_place(size, occupied_seats)] = Icon.SWORD
    occupied_seats[random_place(size, occupied_seats)] = Icon.PRINCESS

    update_forest(forest, size, occupied_seats, images, fog_of_war)
    show_forest(forest, size)

    # ініціалізуємо кнопки
    btn_start["state"] = "disabled"
    btn_stop["state"] = "normal"
    btn_up["state"] = "normal"
    btn_right["state"] = "normal"
    btn_left["state"] = "normal"
    btn_down["state"] = "normal"
    show_player_info(player, "В зайшли до лісу. В лісі є дракон. Бережіть себе.")


def stop_game(size: int, forest: list[list[tk.Label]]):
    global btn_start, btn_stop, btn_up, btn_right, btn_left, btn_down
    occupied_seats: dict[tuple[int, int], Icon] = {}

    update_forest(forest, size, occupied_seats, images, fog_of_war)
    show_forest(forest, size)

    # ініціалізуємо кнопки
    btn_start["state"] = "normal"
    btn_stop["state"] = "disabled"
    btn_up["state"] = "disabled"
    btn_right["state"] = "disabled"
    btn_left["state"] = "disabled"
    btn_down["state"] = "disabled"


def get_new_place(direction: Dirs, player_place: tuple[int, int]) -> tuple[int, int]:
    match direction:
        case Dirs.NORTH:
            player_place = (player_place[0] - 1, player_place[1])
        case Dirs.EAST:
            player_place = (player_place[0], player_place[1] + 1)
        case Dirs.SOUTH:
            player_place = (player_place[0] + 1, player_place[1])
        case Dirs.WEST:
            player_place = (player_place[0], player_place[1] - 1)
    return player_place


def player_step(direction: Dirs, game_panel: tk.Frame, size: int):
    global player

    player_place: tuple[int, int] = player["place"]  # type: ignore[assignment]
    old_place: tuple[int, int] = player_place
    player_place = get_new_place(direction, player_place)
    if not in_forest(size, player_place):
        has_princess: bool = bool(player["has_princess"])
        game_panel.event_generate("<<OutOfForest>>", state=int(has_princess))
        return
    player["place"] = player_place
    if player_place in occupied_seats:
        game_panel.event_generate("<<Occupied>>", x=old_place[1], y=old_place[0])
        return
    game_panel.event_generate("<<ContinueGame>>", x=old_place[1], y=old_place[0])


def game_over(message: str, is_win: bool):
    global player

    show_player_info(player, message, is_win)
    stop_game(SIZE, forest)


def out_forest(event):
    is_win = bool(event.state)
    info_text = "Ви врятували принцесу." if is_win else "Принцеса загинула."
    message = "Ви вийшли з лісу.\n" + info_text + "\nГра завершена."
    game_over(message, is_win)


def item_handler(item: Icon):
    global player

    match item:
        case Icon.PRINCESS:
            if player["has_key"]:
                player["has_princess"] = True
                show_player_info(player, "Ви звільнили принцесу. Вона пішла з вами.")
            else:
                info_text = "Ви знайшли принцесу. Але у вас немає ключа від башти. Принцеса залишилась в лісі."
                show_player_info(player, info_text)
        case Icon.DRAGON:
            if player["has_princess"]:
                game_over("Принцесу з'їв дракон. Ви не впорались із завданням.", False)
            elif player["has_sword"]:
                show_player_info(player, "Ви перемогли дракона. Ліс став безпечний")
            else:
                game_over("Вас з'їв дракон. Ви не впорались із завданням.", False)
        case Icon.KEY:
            player["has_key"] = True
            show_player_info(player, "Ви знайшли ключ.")
        case Icon.SWORD:
            player["has_sword"] = True
            show_player_info(player, "Ви знайшли меч.")


def occupied(event: tk.Event):
    global player, occupied_seats, forest, images, old_item

    old_place: tuple[int, int] = (event.y, event.x)
    player_place: tuple[int, int] = player["place"]  # type: ignore[assignment]
    item: Icon = occupied_seats[player_place]
    if old_item == Icon.PRINCESS and not player["has_princess"]:
        occupied_seats[old_place] = Icon.PRINCESS
    else:
        del occupied_seats[old_place]
    occupied_seats[player_place] = Icon.PLAYER
    update_forest_cell(forest, player_place, Icon.PLAYER, images)
    if old_item == Icon.PRINCESS and not player["has_princess"] and not fog_of_war:
        update_forest_cell(forest, old_place, Icon.PRINCESS, images)
        old_item = Icon.TREE
    else:
        update_forest_cell(forest, old_place, Icon.TREE, images)
    old_item = item
    item_handler(item)


def continue_game(event: tk.Event):
    global player, occupied_seats, forest, images, old_item

    old_place: tuple[int, int] = (event.y, event.x)
    player_place: tuple[int, int] = player["place"]  # type: ignore[assignment]
    if old_item == Icon.PRINCESS and not player["has_princess"]:
        occupied_seats[old_place] = Icon.PRINCESS
    else:
        del occupied_seats[old_place]
    occupied_seats[player_place] = Icon.PLAYER
    if old_item == Icon.PRINCESS and not player["has_princess"] and not fog_of_war:
        update_forest_cell(forest, old_place, Icon.PRINCESS, images)
        old_item = Icon.TREE
    else:
        update_forest_cell(forest, old_place, Icon.TREE, images)
    update_forest_cell(forest, player_place, Icon.PLAYER, images)


# script_path = os.path.dirname(__file__)

SIZE = 5
FOREST_CELL_SIZE = 96
FOREST_SIZE = (FOREST_CELL_SIZE + 4) * SIZE
TP_WITH = 207
MAIN_WINDOWS_GEOMETRY = f"{FOREST_SIZE + TP_WITH}x{FOREST_SIZE}+48+48"
BB_HEIGHT = 150
IB_HEIGHT = FOREST_SIZE - BB_HEIGHT
occupied_seats: dict[tuple[int, int], Icon] = {}
player: dict[str, Union[tuple[int, int], bool]] = {}
old_item: Icon = Icon.TREE


main_window = tk.Tk()

images = create_images(main_window, resource_path("images"))
btn_icons = create_btn_ico_images(main_window, resource_path("images"))

main_window.protocol(
    "WM_DELETE_WINDOW", on_closing
)  # Перехоплення події закриття головного вікна
main_window.title("Врятуй принцесу")
main_window.resizable(False, False)  # Забороняє змінювати розмір вікна
main_window.wm_attributes("-topmost", True)  # Робить вікно - завжди зверху
main_window.iconbitmap(os.path.join(resource_path("images"), "princess.ico"))
main_window.geometry(MAIN_WINDOWS_GEOMETRY)

game_panel = tk.Frame(main_window, height=FOREST_SIZE, width=FOREST_SIZE, bg="green")
game_panel.place(x=0, y=0)

btn_bar = tk.Frame(
    main_window, height=BB_HEIGHT, width=TP_WITH, bg="red", padx=8, pady=5
)
btn_bar.place(x=FOREST_SIZE, y=0, width=TP_WITH, height=BB_HEIGHT)

info_bar = tk.Frame(
    main_window, height=IB_HEIGHT, width=TP_WITH, bg="blue", padx=8, pady=5
)
info_bar.place(x=FOREST_SIZE, y=BB_HEIGHT, width=TP_WITH, height=IB_HEIGHT)

btn_start = create_btn(btn_bar, 0, 0, 6, text="Розпочати гру")
btn_stop = create_btn(btn_bar, 0, 6, 6, text="Завершити гру", state="disabled")

btn_up = create_btn(btn_bar, 1, 5, 2, state="disabled", image=btn_icons["btn_up"])
btn_left = create_btn(btn_bar, 2, 3, 2, state="disabled", image=btn_icons["btn_left"])
btn_right = create_btn(btn_bar, 2, 7, 2, state="disabled", image=btn_icons["btn_right"])
btn_down = create_btn(btn_bar, 3, 5, 2, state="disabled", image=btn_icons["btn_down"])


player_info = tk.Label(info_bar, text="", wraplength=TP_WITH - 16)
player_info.pack(anchor="n", side="top", fill="x", expand=True)

forest = create_forest(SIZE, game_panel)

fog_of_war = True

# Прив'язуємо події до віджетів
main_window.bind("<Control-f>", set_fog_of_war)

btn_start["command"] = lambda: start_game(SIZE, forest)
btn_stop["command"] = lambda: stop_game(SIZE, forest)

btn_up["command"] = lambda: player_step(Dirs.NORTH, game_panel, SIZE)
btn_left["command"] = lambda: player_step(Dirs.WEST, game_panel, SIZE)
btn_right["command"] = lambda: player_step(Dirs.EAST, game_panel, SIZE)
btn_down["command"] = lambda: player_step(Dirs.SOUTH, game_panel, SIZE)

main_window.bind("w", lambda event: player_step(Dirs.NORTH, game_panel, SIZE))
main_window.bind("a", lambda event: player_step(Dirs.WEST, game_panel, SIZE))
main_window.bind("d", lambda event: player_step(Dirs.EAST, game_panel, SIZE))
main_window.bind("s", lambda event: player_step(Dirs.SOUTH, game_panel, SIZE))

main_window.bind("<Up>", lambda event: player_step(Dirs.NORTH, game_panel, SIZE))
main_window.bind("<Left>", lambda event: player_step(Dirs.WEST, game_panel, SIZE))
main_window.bind("<Right>", lambda event: player_step(Dirs.EAST, game_panel, SIZE))
main_window.bind("<Down>", lambda event: player_step(Dirs.SOUTH, game_panel, SIZE))

game_panel.bind("<<OutOfForest>>", out_forest)
game_panel.bind("<<Occupied>>", occupied)
game_panel.bind("<<ContinueGame>>", continue_game)

main_window.mainloop()
