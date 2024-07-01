##############|IMPORTS|##############
from random import randint, shuffle
import colorama
import math
from copy import deepcopy
from treelib import Node, Tree

##############|CLASSES|#############

class Grid():

    # Initialisation
    def __init__(self, simulated:bool=False) -> None:
        self.grid = [['   ' for _ in range(3)] for _ in range(3)]
        self.players = [' X ', ' O ']
        self.winner = -1
        self.last_pawn_added = -1
        self.simulated = simulated # A simulated Grid is a grid that has no need to have next legal_actions
        if not self.simulated:
            self.legal_actions = self.generate_legal_actions()
        else:
            self.legal_actions = []
    
    # Getters
    def get_players(self) -> list:
        return self.players
    def get_winner(self) -> int:
        return self.winner
    def get_grid(self) -> list:
        return self.grid
    def get_legal_actions(self) -> list:
        return self.legal_actions
    def get_simulated(self) -> bool:
        return self.simulated
    # Setters
    def set_grid(self, grid:list):
        self.grid = deepcopy(grid)
    def set_players(self, players:list) -> None:
        self.players = players
    def set_winner(self, winner:int) -> None:
        self.winner = winner
    def set_simulated(self, simulated:bool) -> None:
        if self.simulated and not simulated:
            self.generate_legal_actions()
        self.simulated = simulated


    # Methods

    def print(self) -> None:
        print()
        for i in range(len(self.grid)):
            print(f"{2-i} ", end='')
            print("|".join(self.grid[i]))
            if i < 2:
                print("  -----------")
        print("   0   1  2 \n")

    def is_in_initial_state(self) -> bool:
        empty = True
        line = 0; column = 0
        while empty and line < len(self.grid):
            while empty and column < len(self.grid[line]):
                if 'X' not in self.grid[line][column] and 'O' not in self.grid[line][column]:
                    column += 1
                else:
                    empty = False
            line += 1
        return empty
    
    def add_pawn(self, player:int, coord:tuple) -> bool:
        if 0 <= player <= len(self.players)-1:
            if self.grid[len(self.grid)-coord[1]-1][coord[0]] == '   ':
                self.grid[len(self.grid)-coord[1]-1][coord[0]] = self.players[player]
                self.last_pawn_added = player
                return True
            else:
                return False
        else:
            return False

    def generate_legal_actions(self) -> list:   # FOR SOME REASON THE set_grid() METHOD SEEMS TO ACT WEIRD
        possible_actions = []
        for line in range(3):
            for column in range(3):
                temp_grid = Grid(True)
                temp_grid.set_grid(self.grid) # BUG
                temp_grid.add_pawn((self.last_pawn_added+1)%2, (column, line))
                if temp_grid.get_grid() != self.grid:
                    possible_actions.append(temp_grid)
        return possible_actions

    def is_in_final_state(self) -> bool:
        final = False
        line = 0; column = 0
        while not final and line < len(self.grid):
            while not final and column < len(self.grid[line]):
                current_player_tested = self.grid[line][column]
                if current_player_tested != '   ':
                    # Right diagonal
                    if (line,column) == (0,0) and current_player_tested == self.grid[line][column] and current_player_tested == self.grid[line+1][column+1] and current_player_tested == self.grid[line+2][column+2]:
                        self.winner = self.players.index(current_player_tested)
                        final = True
                    # Left diagonal
                    if (line,column) == (2,0) and current_player_tested == self.grid[line][column] and current_player_tested == self.grid[line-1][column+1] and current_player_tested == self.grid[line-2][column+2]:
                        self.winner = self.players.index(current_player_tested)
                        final = True
                    # Columns
                    if line == 0 and current_player_tested == self.grid[line][column] and current_player_tested == self.grid[line+1][column] and current_player_tested == self.grid[line+2][column]:
                        self.winner = self.players.index(current_player_tested)
                        final = True 
                    # Rows
                    if column == 0 and current_player_tested == self.grid[line][column] and current_player_tested == self.grid[line][column+1] and current_player_tested == self.grid[line][column+2]:
                        self.winner = self.players.index(current_player_tested)
                        final = True
                column += 1
            line += 1
        return final


class Game():
    
    # Initialisation:
    def __init__(self, simulated:bool=False) -> None:
        self.grid = Grid()
        self.turn = 0
        self.players = self.grid.get_players()
        self.simulated = simulated
    
    # Getters
    def get_turn(self) -> int:
        return self.turn
    def get_players(self) -> list:
        return self.players
    def get_simulated(self) -> bool:
        return self.simulated
    # Setters
    def set_turn(self, turn:int) -> bool:
        if type(turn) == int and turn >= 0:
            self.turn = turn
            return True
        else:
            return False


    # Methods

    def play_turn(self) -> bool:
        # Human player's turn
        if self.turn%2 == 0:
            player_played = False
            while not player_played:
                correct_input = False
                while not correct_input:
                    try:
                        x,y = input(">>> Enter coordinates x and y separated by a dot: ").split('.')
                        x = int(x); y = int(y)
                        if 0 <= x <= 2 and 0 <= y <= 2:
                            correct_input = True
                        else:
                            print(colorama.Fore.RED + "/!\ Incorrect input, try again.\n" + colorama.Style.RESET_ALL)
                    except:
                        print(colorama.Fore.RED + "/!\ Incorrect input, try again.\n" + colorama.Style.RESET_ALL)

                player_played = self.grid.add_pawn(0, (x,y))
            print(f"{self.players[0]}'s turn.")
            self.grid.print()
        # IA player's turn
        else:
            print(f"{self.players[1]}'s turn.")
            # TEMPORARY
            ia_played = False
            while not ia_played:
                ia_played = self.grid.add_pawn(1, (randint(0,2),randint(0,2)))
            self.grid.print()
        self.turn += 1

        # Check if game is final_state:
        return self.grid.is_in_final_state()

    def start_game(self) -> None:
        end = False
        while not end:
            end = self.play_turn()
        print(f"Winner is{self.players[self.grid.get_winner()]}")

class My_Node():

    def __init__(self, parent=None, content:Grid=Grid(), wins:float=0, visits:int=0) -> None:
        self.children = []
        self.parent = parent
        self.content = content # The content of a Node is a Grid object
        self.wins = wins
        self.visits = visits
        self.untried_actions = self.content.get_legal_actions()
        shuffle(self.untried_actions)

    # Getters
    def get_children(self) -> list:
        return self.children
    def get_parent(self):
        return self.parent
    def get_content(self) -> Grid:
        return self.content
    def get_wins(self) -> float:
        return self.wins
    def get_visits(self) -> int:
        return self.visits
    def get_ratio(self) -> str:
        return f"{self.wins}/{self.visits}"
    def get_path_to_root(self) -> list:
        path = []
        selected_node = self
        end = selected_node.is_root()
        while not end:
            path.insert(0, selected_node)
            selected_node = selected_node.get_parent()
        return path
    # Setters
    def set_wins(self, v:float) -> None:
        self.wins = v
    def set_visits(self, v:int) -> None:
        self.visits = v
    def set_parent(self, parent) -> None:
        self.parent = parent


    # Methods

    def add_child(self, node) -> None:
        self.children.append(node)

    def is_leaf(self) -> bool:
        return self.children == []
    
    def is_root(self) -> bool:
        return self.parent == None
    
    def expand(self) -> None:
        child_node = self.untried_actions.pop()
        child_node.set_simulated(False); child_node.set_parent(self)
        self.children.append(child_node)
        return child_node
    


class My_Tree():
    
    def __init__(self, root) -> None:
        self.root = root
        self.visualization_tree = Tree()
        self.visualization_tree.create_node(tag=f"{self.root.get_ratio()}", identifier=0, parent=None, data=self.root.get_content())

    # Getters
    def get_root(self) -> My_Node:
        return self.root
    def get_visualization_tree(self) -> Tree:
        return self.visualization_tree


    # Methods

    def find_grid_in_all_nodes(self, goal_grid:Grid) -> tuple: # TODO Test this
        queue = []
        selected_node = self.root
        end = selected_node.is_leaf(); found = False
        while not end:
            # We add every child of the selected node in queue
            for child in selected_node.get_children():
                queue.append(child)
            selected_node = queue.pop(0)
            if selected_node.get_content().get_grid() != goal_grid.get_grid():
                end = True; found = True
            else:
                end = selected_node.is_leaf()
        return found, selected_node
    
    def get_all_nodes(self, path:list=[]) -> list:  # TODO Test this
        temp_path = path
        if temp_path == []: temp_path.append(self.root)
        selected_node = path[-1]
        if selected_node.is_leaf():
            return [selected_node]
        else:
            temp_path += [selected_node]
            for child in selected_node.get_children():
                temp_path += self.get_all_nodes([child])
            return temp_path
        
    def visualize_tree(self, show_tree:bool=True) -> None: # TODO Test this
        all_nodes = self.get_all_nodes()
        for i in range(1, len(all_nodes)):
            node = all_nodes[i]
            self.visualization_tree.create_node(tag=f"{node.get_ratio()}", identifier=i, parent=node.get_parent(), data=node.get_content())
        if show_tree: self.visualization_tree.show()


class MCTS():
    
    def __init__(self, tree:My_Tree, c:float=math.sqrt(2)) -> None:
        self.tree = tree
        self.c = c

    # Getters
    def get_tree(self) -> My_Tree:
        return self.tree
    # Setters
    def set_c(self, c:float=math.sqrt(2)) -> None:
        self.c = c


    # Methods


    # Step 1 - Selection
    def selection(self, beginning_node:My_Node=None) -> My_Node:
        if beginning_node == None:
            selected_node = self.tree.get_root()
        else:
            selected_node = beginning_node

        # Repeat until the node that has been selected using the UCT formula is a leaf of the tree
        while not selected_node.is_leaf():
            max = float('-inf'); selected_node = None
            for child in selected_node.get_children():
                # UCT formula: w/n + c*sqrt(ln(N)/n)
                val = child.get_wins()/child.get_visits()+self.c*math.sqrt(math.log(child.get_parent().get_visits())/child.get_visits())
                if val > max:
                    max = val; selected_node = child
        return selected_node

    # Step 2 - Expansion
    def expansion(self, selected_node:My_Node) -> My_Node:
        return selected_node.expand()

    # Step 3 - Simulation
    def simulation(self) -> float:  # TODO
        pass

    # Step 4 - Retropropagation
    def retropropagation(self, expanded_Node:My_Node, result:float) -> None:
        is_root = False
        current_node = expanded_Node
        while not is_root:
            current_node.set_visits(current_node.get_visits()+1) # Visits += 1
            current_node.set_visits(current_node.get_visits()+1) # Wins += result (0, 1 or 0.5)
            current_node = current_node.get_parent()
            is_root = current_node.is_root()




m_tree = My_Tree(My_Node())
new_grid = Grid(); new_grid.add_pawn(1, (randint(0,2),randint(0,2)))
m_tree.get_root().add_child(My_Node(m_tree.get_root(), new_grid, 0, 0))
all_nodes = m_tree.get_all_nodes()
for node in all_nodes:
    print(node.get_content().get_grid())    # BUG Adds two children instead of one (it adds the root as a child of the root + the desired node)
#m_tree.visualize_tree()





# m_mcts = MCTS(m_tree, math.sqrt(2))
# root = m_mcts.get_tree().get_root().get_content()
# print(root.get_legal_actions())
# for grid in root.get_legal_actions():
#     print(grid.get_grid())
#print(m_mcts.selection().get_ratio()) # Prints the win/visits ratio of the node selected in step 1 (so the root in this case)