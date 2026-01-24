from tkinter import *
from tkinter import messagebox
import os


def on_closing():
    if messagebox.askokcancel("Вихід із застосунку", "Хочете вийти із застосунку?"):
        tk.destroy()


SCRIPT_PATH = os.path.dirname(__file__)
SIZE = 5
FOREST_CELL_SIZE = 96
FOREST_SIZE = (FOREST_CELL_SIZE + 4) * SIZE
TOOLS_PANEL_WITH = 207
MAIN_WINDOWS_GEOMETRY = f"{FOREST_SIZE + TOOLS_PANEL_WITH}x{FOREST_SIZE}+48+48"
BTN_BAR_HEIGHT = 200
INFO_BAR_HEIGHT = FOREST_SIZE - BTN_BAR_HEIGHT

tk = Tk()
tk.protocol("WM_DELETE_WINDOW", on_closing)  # Перехоплення події закриття головного вікна
tk.title("Врятуй принцесу")
tk.resizable(False, False)  # Забороняє змінювати розмір вікна
tk.wm_attributes("-topmost", True)  # Робить вікно - завжди зверху
tk.iconbitmap(os.path.join(SCRIPT_PATH, "images", "princess.ico"))
tk.geometry(MAIN_WINDOWS_GEOMETRY)

game_panel = Frame(tk, height=FOREST_SIZE, width=FOREST_SIZE)
game_panel.place(x=0, y=0)
tools_panel = Frame(tk, height=FOREST_SIZE, width=TOOLS_PANEL_WITH, bg="yellow")
tools_panel.place(x=FOREST_SIZE, y=0)

btn_bar = Frame(tools_panel, height=BTN_BAR_HEIGHT, width=TOOLS_PANEL_WITH, bg="red", padx=8, pady=5)
btn_bar.place(x=0, y=0, width=TOOLS_PANEL_WITH, height=BTN_BAR_HEIGHT)

btn_start = Button(btn_bar, text="Розпочати гру")
btn_start.grid(row=0, column=0, padx=2, pady=5)

btn_stop = Button(btn_bar, text="Завершити гру")
btn_stop.grid(row=0, column=1, padx=2, pady=5)

info_bar = Frame(tools_panel, height=INFO_BAR_HEIGHT, width=TOOLS_PANEL_WITH, bg="blue", padx=8, pady=5)
info_bar.place(x=0, y=BTN_BAR_HEIGHT, width=TOOLS_PANEL_WITH, height=INFO_BAR_HEIGHT)

player_info = Label(info_bar, text="Ви зайшли в ліс. В лісі ви можете зустріти дракона. Бережіть себе.",
                    wraplength=TOOLS_PANEL_WITH - 16)
player_info.pack(anchor="n", side="top", fill="x", expand=True)

prince_img = PhotoImage(file=os.path.join(SCRIPT_PATH, "images", "prince.png"))
tree_img = PhotoImage(file=os.path.join(SCRIPT_PATH, "images", "Tree.png"))
forest: list[list[None | Label]] = [[None for _ in range(SIZE)] for _ in range(SIZE)]
for row in range(SIZE):
    for col in range(SIZE):
        forest[row][col] = Label(master=game_panel, height=FOREST_CELL_SIZE, width=FOREST_CELL_SIZE,
                                 name=f"label_{row}_{col}", bg="#0d0")
        forest[row][col].grid(row=row, column=col)
for row in range(SIZE):
    for col in range(SIZE):
        forest[row][col]["image"] = tree_img
        forest[row][col].grid(row=row, column=col)
forest[0][0]["image"] = prince_img


tk.mainloop()
