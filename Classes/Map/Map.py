# # Import Another Classes
from Classes.Map.Goal import *
from Classes.Map.Objective import *
from Classes.Map.Player import *
from random import randrange

class Map:
    def __init__(self, size):
        # Init Map Size, Init Player, Init Goals Count
        self.size = size
        self.player = Player(0,0)
        self.goals_count = 0
        self.objectives = Objective(3,3)
        self.goals = Goal(4,4)

        # Build Empty Array
        self.tiles = []
        for i in range(size):
            self.tiles.append([0 for j in range(size)])

        # Print Results
        print("Map Initialized With Size",size)
        self.print_map()

    def print_map(self):
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[0])):
                print("[" + str(self.tiles[i][j]) + "]", end="");
            print("")

    def player_move(self, direction):
        if direction == "up" or direction == "UP":
            self.tiles[self.player.y][self.player.x] = 0
            self.player.move_up()
            self.player.steps += 1
            if self.player.y <= 0:
                self.player.move_down()
                self.player.steps -= 1
            elif self.tiles[self.player.y][self.player.x] == 1:
                self.player.move_down()
                self.player.steps -= 1
            elif self.tiles[self.player.y][self.player.x] == 3:
                self.objectives.move_up()
                if self.tiles[self.objectives.y][self.objectives.x] == 1:
                    self.objectives.move_down()
                    self.player.move_down()
                    self.player.steps -= 1
            self.tiles[self.goals.y][self.goals.x] = 4
            self.tiles[self.objectives.y][self.objectives.x] = 3
            self.tiles[self.player.y][self.player.x] = 2
        elif direction == "down" or direction == "DOWN":
            self.tiles[self.player.y][self.player.x] = 0
            self.player.move_down()
            self.player.steps += 1
            if self.player.y >= (len(self.tiles[0]) - 1):
                self.player.move_up()
                self.player.steps -= 1
            elif self.tiles[self.player.y][self.player.x] == 1:
                self.player.move_up()
                self.player.steps -= 1
            elif self.tiles[self.player.y][self.player.x] == 3:
                self.objectives.move_down()
                if self.tiles[self.objectives.y][self.objectives.x] == 1:
                    self.objectives.move_up()
                    self.player.move_up()
                    self.player.steps -= 1
            self.tiles[self.goals.y][self.goals.x] = 4
            self.tiles[self.objectives.y][self.objectives.x] = 3
            self.tiles[self.player.y][self.player.x] = 2
        elif direction == "left" or direction == "LEFT":
            self.tiles[self.player.y][self.player.x] = 0
            self.player.move_left()
            self.player.steps += 1
            if self.player.x <= 0:
                self.player.move_right()
                self.player.steps -= 1
            elif self.tiles[self.player.y][self.player.x] == 1:
                self.player.move_right()
                self.player.steps -= 1
            elif self.tiles[self.player.y][self.player.x] == 3:
                self.objectives.move_left()
                if self.tiles[self.objectives.y][self.objectives.x] == 1:
                    self.objectives.move_right()
                    self.player.move_right()
                    self.player.steps -= 1
            self.tiles[self.goals.y][self.goals.x] = 4
            self.tiles[self.objectives.y][self.objectives.x] = 3
            self.tiles[self.player.y][self.player.x] = 2
        elif direction == "right" or direction == "RIGHT":
            self.tiles[self.player.y][self.player.x] = 0
            self.player.move_right()
            self.player.steps += 1
            if self.player.x >= (len(self.tiles) - 1):
                self.player.move_left()
                self.player.steps -= 1
            elif self.tiles[self.player.y][self.player.x] == 1:
                self.player.move_left()
                self.player.steps -= 1
            elif self.tiles[self.player.y][self.player.x] == 3:
                self.objectives.move_right()
                if self.tiles[self.objectives.y][self.objectives.x] == 1:
                    self.objectives.move_left()
                    self.player.move_left()
                    self.player.steps -= 1
            self.tiles[self.goals.y][self.goals.x] = 4
            self.tiles[self.objectives.y][self.objectives.x] = 3
            self.tiles[self.player.y][self.player.x] = 2

class Map_Builder:
    def __init__(self):
        print("Map Builder is Initialized")

    def build_map(self,level):
        print("Building Map",level)
        new_map = Map(5)
        self.build_walls(new_map)
        self.place_player(new_map)
        new_map.tiles[new_map.objectives.y][new_map.objectives.x] = 3
        return new_map

    def build_random_map(self):
        print("Building Random Map")
        random_size = randrange(7,15)
        new_map = Map(random_size)
        self.build_walls(new_map)
        self.place_player(new_map)
        self.place_random_goal(new_map)
        self.place_random_objective(new_map)
        return new_map

    def build_walls(self, map):
        tiles = map.tiles
        for i in range(len(tiles)):
            for j in range(len(tiles[0])):
                if i == 0 or j == 0 or i == len(tiles)-1 or j == len(tiles[0])-1:
                    tiles[i][j] = 1
        print("Build Walls Success")

    def place_player(self, map):
        map.player = Player(randrange(1,len(map.tiles[0])-2), randrange(1,len(map.tiles)-2))
        map.tiles[map.player.y][map.player.x] = 2
        print("Place Player Success")

    def place_random_goal(self, map):
        rand_x = 0
        rand_y = 0

        while map.tiles[rand_y][rand_x] != 0:
            rand_x = randrange(1,len(map.tiles[0])-2)
            rand_y = randrange(1,len(map.tiles)-2)
        map.goals = Goal(rand_x,rand_y)
        map.tiles[map.goals.y][map.goals.x] = 4

    def place_random_objective(self, map):
        rand_x = 0
        rand_y = 0
        while map.tiles[rand_y][rand_x] != 0:
            rand_x = randrange(2,len(map.tiles[0])-3)
            rand_y = randrange(2,len(map.tiles)-3)
        map.objectives = Objective(rand_x, rand_y)
        map.tiles[map.objectives.y][map.objectives.x] = 3
