from room import Room
from player import Player
from world import World
import random
from ast import literal_eval
from util import Stack
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# get the opposite direction of the current room in order to move rooms
def get_direction(direction):
    if direction == 'n':
        return 's'
    if direction == 's':
        return 'n'
    if direction == 'e':
        return 'w'
    if direction == 'w':
        return 'e'

def bft():
    path = {}
    visited = set()
    s = Stack()

    # for loop that initializes each rooms direction with ?
    for i in range(len(room_graph)):
        path[i] = {'n': '?', 's': '?', 'w': '?', 'e': '?'}
    
    # while loop that'll run only if the length of the visited set is less than the length of the room graph
    while len(visited) < len(room_graph):
        success = False
        # set the starting/current room id to cur_room
        cur_room = player.current_room.id
        # set the current room path/direction to room_path
        room_path = player.current_room.get_exits()
        # check to see if cur_room is in visted, if not add it to the visited set
        if cur_room not in visited:
            visited.add(cur_room)
        # check to see if the direction is in path of the curent room
        for direction in path[cur_room]:
            # if the direction isn't there then set the ? to 0
            if direction not in room_path:
                path[cur_room][direction] = 0

        # count to see how many rooms we don't know
        num_directions = 0
        for direction in path[cur_room]:
            # if the direction is not ? increment by 1
            if path[cur_room][direction] != '?':
            # if a room isnt known then we move rooms towards the direction that is known
                num_directions += 1
            elif not 0:
                 move_rooms = direction
        # if all rooms are known
        if num_directions == 4:
            success = True
        
        # pop the last move in order to go down a differnet path and add where I'm going to the traversal path
        if success is True:
            last_move = s.pop()
            move_rooms = get_direction(last_move)
            traversal_path.append(move_rooms)
            player.travel(move_rooms)
        # if I don't have to backtrack
        else:
            s.push(move_rooms)
            traversal_path.append(move_rooms)
            player.travel(move_rooms)
            # add to the path my next rooms
            next_room = player.current_room.id
            path[cur_room][move_rooms] = next_room
            change_directions = get_direction(move_rooms)
            path[next_room][change_directions] = cur_room
            visited.add(next_room)
            
    
bft()
# print('Starting ROOM ID: ', player.current_room.id)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
