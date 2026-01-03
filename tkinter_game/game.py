import tkinter as tk
import random
from tkinter import messagebox

SIZE = 5

пусто = ""
Гравець = "🚶"
ключ = "К"
Меч = "M"
Принцеса = "П"
Дракон = "Д"
Вихід = "В"

# Двовимірний масив
Поле = [[пусто for _ in range(SIZE)] for _ in range(SIZE)]
Кнопка = [[None for _ in range(SIZE)] for _ in range(SIZE)]

Ключ = False
є_меч = False
Є_принцеса = False
Позиція_гравця = (0, 0)
player = {}
occupied_seats = {}


def place_random(item):
    while True:
        x = random.randint(0, SIZE - 1)
        y = random.randint(0, SIZE - 1)
        if Поле[x][y] == пусто:
            Поле[x][y] = item
            return (x, y)


def init_game():
    global Позиція_гравця
    Позиція_гравця = place_random(Гравець)
    place_random(ключ)
    place_random(Меч)
    place_random(Принцеса)
    place_random(Дракон)
    place_random(Вихід)
    update_ui()


def update_ui():
    for i in range(SIZE):
        for j in range(SIZE):
            Кнопка[i][j]["text"] = Поле[i][j]


def end_game(text, win):
    if win:
        messagebox.showinfo("Перемога", text)
    else:
        messagebox.showerror("Кінець гри", text)
    root.destroy()


def move(dx, dy):
    global Позиція_гравця, Ключ, є_меч, Є_принцеса

    x, y = Позиція_гравця
    nx, ny = x + dx, y + dy

    if nx < 0 or nx >= SIZE or ny < 0 or ny >= SIZE:
        if Є_принцеса:
            end_game("🎉 Ти вийшов з Принцесою!", True)
        else:
            end_game("Ти вийшов без Принцеси.", False)
        return

    cell = Поле[nx][ny]

    if cell == ключ:
        Ключ = True
    elif cell == Меч:
        є_меч = True
    elif cell == Принцеса and Ключ:
        Є_принцеса = True
    elif cell == Дракон:
        if є_меч and not Є_принцеса:
            pass  # дракон переможений
        else:
            end_game("🐉 Дракон тебе з'їв!", False)
            return
    elif cell == Вихід:
        if Є_принцеса:
            end_game("🎉 Ти знайшов вихід з Принцесою!", True)
        else:
            end_game("Ти знайшов вихід без Принцеси.", False)
        return

    Поле[x][y] = пусто
    Поле[nx][ny] = Гравець
    Позиція_гравця = (nx, ny)
    update_ui()


root = tk.Tk()
root.title("Гра про ліс та дракона")
grid = tk.Frame(root)
grid.pack()

for i in range(SIZE):
    for j in range(SIZE):
        lbl = tk.Label(
            grid, text="", width=10, height=3, font=("Arial", 24), relief="solid"
        )
        lbl.grid(row=i, column=j)
        Кнопка[i][j] = lbl

controls = tk.Frame(root)
controls.pack(pady=10)

tk.Button(controls, text="↑", command=lambda: move(-1, 0)).grid(row=0, column=1)
tk.Button(controls, text="←", command=lambda: move(0, -1)).grid(row=1, column=0)
tk.Button(controls, text="→", command=lambda: move(0, 1)).grid(row=1, column=2)
tk.Button(controls, text="↓", command=lambda: move(1, 0)).grid(row=2, column=1)

init_game()
root.mainloop()
