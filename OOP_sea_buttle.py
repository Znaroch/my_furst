import random
from random import randint

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Не стрелять за пределы поля!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже сюда стреляли!"

class BoardWrongShipException(BoardException):
    pass


class FieldOccupied(Exception):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:
    def __init__(self,  dot, length, direction):
        self.length = length
        self.dot = dot
        self.direction = direction
        self.hp = length

    @property
    def dots(self):
        dots_ship = []
        for i in range(self.length):
            current_x = self.dot.x
            current_y = self.dot.y
            if self.direction == 0:
                current_x += i
            elif self.direction == 1:
                current_y += i

            dots_ship.append(Dot(current_x, current_y))

        return dots_ship

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.count = count = 0
        self.hid = hid
        self.life = 0
        self.busy = []
        self.ships = []
        self.field = [["◌"] * self.size for i in range(self.size)]

    def __str__(self):
        field_play = ""
        field_play += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, j in enumerate(self.field):
            field_play += f"\n{i+1} | " + " | ".join(j) + " |"

        if self.hid:
            field_play = field_play.replace("■", "◌")
        return field_play

    def out(self, dot):
        return not((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def contour(self, ship, verb=False):
        near_field = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0 , 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near_field:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for i in ship.dots:
            if self.out(i) or i in self.busy:
                raise BoardWrongShipException()
        for i in ship.dots:
            self.field[i.x][i.y] = "■"
            self.busy.append(i)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, pop):
        if self.out(pop):
            raise BoardOutException()

        if pop in self.busy:
            raise BoardUsedException()

        self.busy.append(pop)

        for ship in self.ships:
            if pop in ship.dots:
                ship.hp -= 1
                self.field[pop.x][pop.y] = "X"
                if ship.hp == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[pop.x][pop.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []


board = Board()


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Dot(randint(0, board.size-1), randint(0, board.size-1))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ходите: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()