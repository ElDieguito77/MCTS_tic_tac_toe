##############|IMPORTS|##############
from random import randint
import colorama
import math

##############|CLASSES|#############

class Grid():

    # Initialisation
    def __init__(self) -> None:
        self.grid = [['   ' for _ in range(3)] for _ in range(3)]
        self.players = [' X ', ' O ']
        self.winner = -1
    
    # Getters
    def get_players(self) -> list:
        return self.players
    def get_winner(self) -> int:
        return self.winner
    # Setters
    def set_players(self, players:list) -> None:
        self.players = players
    def set_winner(self, winner:int) -> None:
        self.winner = winner


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
                return True
            else:
                print(f"a{self.grid[len(self.grid)-coord[1]-1][coord[0]]}a")
                return False
        else:
            return False
                            
    def is_in_final_state(self) -> int:
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

    def start_game(self):
        end = False
        while not end:
            end = self.play_turn()
        print(f"Winner is{self.players[self.grid.get_winner()]}")

class Node():

    def __init__(self, parent=None, content=Grid(), wins:int=0, visits:int=0) -> None:
        self.sons = []
        self.parent = parent
        self.content = content
        self.wins = wins
        self.visits = visits

    # Getters
    def get_sons(self) -> list:
        return self.sons
    def get_parent(self):
        return self.parent
    def get_content(self) -> Grid:
        return self.content
    def get_wins(self) -> int:
        return self.wins
    def get_visits(self) -> int:
        return self.visits
    def get_ratio(self) -> str:
        return f"{self.wins}/{self.visits}"
    # Setters
    def set_wins(self, v:int) -> None:
        self.wins = v

    def add_son(self, node) -> None:
        self.sons.append(node)

    def is_leave(self) -> bool:
        return self.sons == []
    
    def is_root(self) -> bool:
        return self.parent == None
    
class Tree():
    
    def __init__(self, root) -> None:
        self.root = root

    def get_root(self):
        return self.root
    
    def find_node(self):
        pass

class MCTS():
    
    def __init__(self, tree:Tree, c:float=math.sqrt(2)) -> None:
        self.tree = tree
        self.c = c

    def selection(self) -> Node:
        selected_node = self.tree.get_root()
        while not selected_node.is_leave():
            max = float('-inf'); selected_node = None
            for son in selected_node.get_sons():
                val = son.get_wins()/son.get_visits()+self.c*math.sqrt(math.log(son.get_parent().get_visits())/son.get_visits())
                if val > max:
                    max = val; selected_node = son
        return selected_node

    def expansion(self) -> Node:
        pass

    def simulation(self) -> float:
        pass

    def retropropagation(self) -> bool:
        pass

my_game = Game()

# TODO (Randomize starter player), add wait times and colors to terminal logs --> END
# my_game.start_game() # Play a game against a random AI
# TODO Implement the MCTS algorithm for tic-tac-toe

m_tree = Tree(Node())
# m_tree.get_root().add_son(Node(m_tree.get_root(), Grid().add_pawn(1, (randint(0,2),randint(0,2))), 0, 0))
m_mcts = MCTS(m_tree, math.sqrt(2))
print(m_mcts.selection().get_ratio())