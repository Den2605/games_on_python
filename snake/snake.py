import random
from tkinter import *

# Ширина экрана
WIDTH = 800
# Высота экрана
HEIGHT = 600
# Размер сегмента змеи
SEG_SIZE = 20
# Переменная, отвечающая за состояние игры
IN_GAME = False


# Функция для управления игровым процессом
def main():
    """Моделируем игровой процесс"""
    global IN_GAME
    if IN_GAME:
        s.move()
        # Определяем координаты головы
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords

        # столкновения с краями игрового поля
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
            s.reset_snake()
            c.delete(BLOCK)

        # Поедание яблока
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()

        # Поедание змейки
        else:
            for index in range(len(s.segments) - 1):
                if head_coords == c.coords(s.segments[index].instance):
                    IN_GAME = False
                    s.reset_snake()
                    c.delete(BLOCK)

        # скорость змейки
        root.after(150, main)
    # Не IN_GAME -> останавливаем игру, удаляем змейку и выводим сообщения
    else:
        set_state(restart_text, "normal")
        set_state(close_but, "normal")


# Вспомогательная функция
def create_block():
    """Создаем еду для змейки."""
    global BLOCK
    posx = SEG_SIZE * random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE)
    BLOCK = c.create_oval(
        posx,
        posy,
        posx + SEG_SIZE,
        posy + SEG_SIZE,
        fill="red",
    )


class Score(object):
    """Отображение очков."""

    def __init__(self):
        self.score = 0
        self.x = 55
        self.y = 15
        c.create_text(
            self.x,
            self.y,
            text="Счёт: {}".format(self.score),
            font="Arial 25",
            fill="green",
            tag="score",
            state="hidden",
        )

    def increment(self):
        """Подсчёт очков."""
        c.delete("score")
        self.score += 1
        c.create_text(
            self.x,
            self.y,
            text="Счёт: {}".format(self.score),
            font="Arial 25",
            fill="green",
            tag="score",
        )

    def reset(self):
        """Сброс очков при начале новой игры."""
        c.delete("score")
        self.score = 0


class Segment(object):
    """Сегмент змейки."""

    def __init__(self, x, y):
        self.instance = c.create_oval(
            x,
            y,
            x + SEG_SIZE,
            y + SEG_SIZE,
            fill="green",
        )


class Snake(object):
    """Класс змейки."""

    def __init__(self, segments):
        self.segments = segments
        # Варианты движения
        self.mapping = {
            "Down": (0, 1),
            "Right": (1, 0),
            "Up": (0, -1),
            "Left": (-1, 0),
        }
        # инициируем направление движения
        self.vector = self.mapping["Right"]

    def move(self):
        """Двигаем змейку в заданном направлении."""
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index + 1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(
            self.segments[-1].instance,
            x1 + self.vector[0] * SEG_SIZE,
            y1 + self.vector[1] * SEG_SIZE,
            x2 + self.vector[0] * SEG_SIZE,
            y2 + self.vector[1] * SEG_SIZE,
        )

    def add_segment(self):
        """Добавляем сегмент змейки."""
        score.increment()
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):
        """Изменение направления движения змейки."""
        # Не реагируем на нажатие кнопки в противоход движения змейки
        button = 1
        if event.keysym in self.mapping:
            if abs(self.vector[0]) == abs(self.mapping[event.keysym][0]) and abs(
                self.vector[1]
            ) == abs(self.mapping[event.keysym][1]):
                button = None
        if event.keysym in self.mapping and button:
            self.vector = self.mapping[event.keysym]

    def reset_snake(self):
        """Удаление змейки."""
        for segment in self.segments:
            c.delete(segment.instance)


def set_state(item, state):
    """Вывод сообщений."""
    c.itemconfigure(item, state=state)


def clicked(event):
    """Новая игра."""
    score.reset()
    c.itemconfigure(restart_text, state="hidden")
    c.itemconfigure(close_but, state="hidden")
    start_game()


def start_game():
    """Старт игры."""
    global IN_GAME
    global s
    IN_GAME = True
    create_block()
    s = create_snake()
    c.bind("<KeyPress>", s.change_direction)
    main()


# Создаем сегменты и змейку
def create_snake():
    """Создание сегментов и змейки."""
    segments = [
        Segment(SEG_SIZE, SEG_SIZE),
        Segment(SEG_SIZE * 2, SEG_SIZE),
        Segment(SEG_SIZE * 3, SEG_SIZE),
    ]
    return Snake(segments)


# выход из игры
def close_win(root):
    """Выход из игры."""
    exit()


if __name__ == "__main__":
    # Настройка главного окна
    root = Tk()
    # Название окна
    root.title("Змейка")

    # Создаем экземпляр класса Canvas
    c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#42aaff")
    c.grid()

    # Захватываем фокус для отлавливания нажатий клавиш
    c.focus_set()

    # Текст начала новой игры после проигрыша
    restart_text = c.create_text(
        WIDTH / 2,
        HEIGHT - HEIGHT / 3,
        font="Arial 25",
        fill="green",
        text="Начать новую игру",
        state="hidden",
    )

    # Текст выхода из программы после проигрыша
    close_but = c.create_text(
        WIDTH / 2,
        HEIGHT - HEIGHT / 5,
        font="Arial 25",
        fill="green",
        text="Выход из игры",
        state="hidden",
    )

    # Отработка событий при нажимания кнопок
    c.tag_bind(restart_text, "<Button-1>", clicked)
    c.tag_bind(close_but, "<Button-1>", close_win)

    # Считаем очки
    score = Score()

    # Запускаем игру
    main()
    # запускаем окно
    root.mainloop()
