###########################

class Grid():

    def __init__(self) -> None:
        self.grid = [['   ' for _ in range(3)] for _ in range(3)]
        self.players = [' X ', ' O ']
    
    def get_players(self) -> list:
        return self.players
    def set_players(self, players:list) -> None:
        self.players = players

    def print_grid(self) -> None:
        for i in range(len(self.grid)):
            print(f"{2-i} ", end='')
            print("|".join(self.grid[i]))
            if i < 2:
                print("  -----------")
        print("   0   1  2 ")

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
        
    def is_in_final_state(self) -> bool:
        pass

m_grid = Grid()
m_grid.print_grid()
print(m_grid.is_in_initial_state())
m_grid.add_pawn(1, (1,2))
m_grid.print_grid()
print(m_grid.is_in_initial_state())
