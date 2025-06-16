import tkinter as tk
from tkinter import *
import random
# добавить поворот налево

start_positions = [
    {'x': 20, 'y': 115, 'direction': 'right',},
    {'x': 20, 'y': 315, 'direction': 'right'},
    {'x': 20, 'y': 515, 'direction': 'right'},
    {'x': 20, 'y': 715, 'direction': 'right'},
    {'x': 715, 'y': 815, 'direction': 'up'},
    {'x': 515, 'y': 815, 'direction': 'up'},
    {'x': 315, 'y': 815, 'direction': 'up'},
    {'x': 115, 'y': 815, 'direction': 'up'},
]

class Vehicle:
    all_vehicles = []
    def __init__(self, canvas, images_dict, x, y, speed, overtake):
        self.overtake = overtake
        self.canvas = canvas
        self.images = images_dict  # словарь с изображениями по направлениям
        self.current_image = self.images['right']  # начальное изображение
        self.img_width = self.current_image.width()
        self.img_height = self.current_image.height()
        self.image_id = self.canvas.create_image(x, y, anchor='nw', image=self.current_image)
        self.root = self.canvas.winfo_toplevel()
        self.speed = speed
        self.direction = 'right'  # текущее направление
        Vehicle.all_vehicles.append(self)  # добавляем в общий список



    @classmethod
    def add_vehicle(cls, canvas, root):
        vehicle_types = [
            ("passenger", car_images, random.randint(2, 5), random.choice([True, False]), random.randint(1, 5)),
            ("passenger", bike_images, random.randint(3, 6), True, random.randint(1, 2)),
            ("passenger", bus_images, random.randint(1, 3), False, random.randint(10, 40)),
            ("truck", truck_images, random.randint(1, 3), False, random.randint(10, 30)),
        ]
        vtype, images, speed, overtake, extra = random.choice(vehicle_types)
        cls.create_vehicle(vtype, canvas, images, speed, overtake, extra)
        # Запланировать следующее появление через 1-3 секунды
        root.after(random.randint(5000, 7000), lambda: cls.add_vehicle(canvas, root))

    @classmethod
    def create_vehicle(cls, vtype, canvas, images, speed, overtake, new):
        pos = random.choice(start_positions)
        x, y, direction = pos['x'], pos['y'], pos['direction']
        if vtype == "truck":
            vehicle = Truck(canvas, images, x, y, speed, overtake, weight=new)
        else:
            vehicle = PassengerCar(canvas, images, x, y, speed, overtake, passengers=new)
        vehicle.set_direction(direction)
        vehicle.move_image()
        return vehicle

    def get_other_vehicles(self):
        return [v for v in Vehicle.all_vehicles if v != self]


    def set_direction(self, direction):
        if direction in self.images and direction != self.direction:
            x, y = self.canvas.coords(self.image_id)
            self.direction = direction
            self.current_image = self.images[direction]
            self.canvas.coords(self.image_id, x, y)
            self.canvas.itemconfig(self.image_id, image=self.current_image)

    def set_random_start(self):
        pos = random.choice(start_positions)
        self.start_x = pos['x']
        self.start_y = pos['y']
        self.set_direction(pos['direction'])
        self.canvas.coords(self.image_id, self.start_x, self.start_y)

    def DelVehicle(self):
        self.all_vehicles.remove(self)

    def move_image(self):
        intersections = [(85,115),(85, 285), (85, 515), (85, 715),  (285, 515), (285, 715),
                         (110,115), (110, 515), (110, 715),(310, 515), (310, 715),
                         (485, 515), (485, 715), (685, 115), (685, 315), (685, 515), (685, 715),
                         (110,285), (515, 515), (515, 715), (715, 315), (715, 515), (715, 715), (715, 715),]
        x, y = self.canvas.coords(self.image_id)
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        # Проверяем, достигли ли перекрёстка (с допуском 8 пикселей)
        at_intersection = False
        for ix, iy in intersections:
            if abs(x - ix) < 4 and abs(y - iy) < 4:
                at_intersection = True
                break

        if at_intersection:
            # Меняем направление один раз при входе на перекрёсток
            x, y = self.canvas.coords(self.image_id)
            opposites = {
                'up': 'down',
                'down': 'up',
                'left': 'right',
                'right': 'left'
            }

            last_direction = self.direction
            directions = ['up', 'down', 'left', 'right']

            # Исключаем противоположное направление
            directions.remove(opposites[last_direction])

            new_direction = random.choice(directions)
            self.set_direction(new_direction)

            if self.direction == 'down':
                y += 40
                if last_direction == 'left':
                    x -= 28
                if last_direction == 'right':
                    x += 5

            elif self.direction == 'up':
                y -= 40
                if last_direction == 'right':
                    x += 30

            elif self.direction == 'left':
                x -= 40
                if last_direction == 'up':
                    y -= 28


            elif self.direction == 'right':
                x += 40


            self.canvas.coords(self.image_id, x, y)


        # Движение в зависимости от направления
        if self.direction == 'right':
            if x + self.speed < width:
                self.canvas.move(self.image_id, self.speed, 0)
            else:
                self.DelVehicle()
                self.set_random_start()


        elif self.direction == 'down':
            if y + self.speed < height:
                self.canvas.move(self.image_id, 0, self.speed)
            else:
                self.set_random_start()

        elif self.direction == 'up':
            if y - self.speed > 0:
                self.canvas.move(self.image_id, 0, -self.speed)
            else:
                self.set_random_start()

        if self.direction == 'left':
            if x - self.speed > 0:
                self.canvas.move(self.image_id, -self.speed, 0)
            else:
                self.set_random_start()




        self.root.after(30, self.move_image)

class PassengerCar(Vehicle):
    def __init__(self, canvas, images_dict, x, y, speed, overtake, passengers):
        super().__init__(canvas, images_dict, x, y, speed, overtake)
        self.passengers = passengers  # количество пассажиров

    def GetPassengers(self):
        passengers = self.passengers
        return passengers

class Truck(Vehicle):
    def __init__(self, canvas, images_dict, x, y, speed, overtake, weight):
        super().__init__(canvas, images_dict, x, y, speed, overtake)
        self.weight = weight  # вес груза (тонны)

    def GetWeight(self):
        weight = self.weight
        return weight


# Создаем окно и canvas
root = tk.Tk()
root.title("Движущееся изображение с классом")

canvas = tk.Canvas(root, width=800, height=800, bg="white")
canvas.pack()

# Загружаем фон (дорогу)
road = tk.PhotoImage(file="images/road/road1.png")
canvas.create_image(10, 10, anchor='nw', image=road)

# Загружаем изображение машины


# Создаем объект класса Car

car_images = {
    'right': tk.PhotoImage(file="images/right/car.png"),
    'down': tk.PhotoImage(file="images/down/car.png"),
    'left': tk.PhotoImage(file="images/left/car.png"),
    'up': tk.PhotoImage(file="images/up/car.png")
}

bike_images = {
    'right': tk.PhotoImage(file="images/right/bike.png"),
    'down': tk.PhotoImage(file="images/down/bike.png"),
    'left': tk.PhotoImage(file="images/left/bike.png"),
    'up': tk.PhotoImage(file="images/up/bike.png")
}

bus_images = {
    'right': tk.PhotoImage(file="images/right/bus.png"),
    'down': tk.PhotoImage(file="images/down/bus.png"),
    'left': tk.PhotoImage(file="images/left/bus.png"),
    'up': tk.PhotoImage(file="images/up/bus.png")
}

truck_images = {
    'right': tk.PhotoImage(file="images/right/truck.png"),
    'down': tk.PhotoImage(file="images/down/truck.png"),
    'left': tk.PhotoImage(file="images/left/truck.png"),
    'up': tk.PhotoImage(file="images/up/truck.png")
}

# Запускаем анимацию

Vehicle.add_vehicle(canvas, root)




python_image = PhotoImage(file="images/up/qwe.png")

# canvas.create_image(85, 115, anchor=NW, image=python_image)
# canvas.create_image(85, 285, anchor=NW, image=python_image)
# canvas.create_image(85, 515, anchor=NW, image=python_image)
# canvas.create_image(85, 715, anchor=NW, image=python_image)
# canvas.create_image(285, 515, anchor=NW, image=python_image)
# canvas.create_image(285, 715, anchor=NW, image=python_image)
# canvas.create_image(110, 115, anchor=NW, image=python_image)
# canvas.create_image(110, 515, anchor=NW, image=python_image)
# canvas.create_image(110, 715, anchor=NW, image=python_image)
# canvas.create_image(310, 515, anchor=NW, image=python_image)
# canvas.create_image(310, 715, anchor=NW, image=python_image)
# canvas.create_image(485, 515, anchor=NW, image=python_image)
# canvas.create_image(485, 715, anchor=NW, image=python_image)
# canvas.create_image(685, 115, anchor=NW, image=python_image)
# canvas.create_image(685, 315, anchor=NW, image=python_image)
# canvas.create_image(685, 515, anchor=NW, image=python_image)
# canvas.create_image(685, 715, anchor=NW, image=python_image)
# canvas.create_image(110, 285, anchor=NW, image=python_image)
# canvas.create_image(515, 515, anchor=NW, image=python_image)
# canvas.create_image(515, 715, anchor=NW, image=python_image)
# canvas.create_image(715, 315, anchor=NW, image=python_image)
# canvas.create_image(715, 515, anchor=NW, image=python_image)
# canvas.create_image(715, 715, anchor=NW, image=python_image)
# canvas.create_image(715, 715, anchor=NW, image=python_image)




root.mainloop()
