import tkinter as tk   # Import tkinter for GUI
import random          # Import random module for random tile placement

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Puzzle Game (Tkinter)")     # Set window title
        self.root.configure(bg="#faf8ef")                 # Set background color

        # Initialize score variable
        self.score = 0

        # Label to display score
        self.score_label = tk.Label(root, text=f"Score: {self.score}",
                                    font=("Arial", 16, "bold"), bg="#faf8ef")
        self.score_label.pack(pady=10)

        # Create a frame for 4x4 grid
        self.frame = tk.Frame(root, bg="#bbada0", bd=5)
        self.frame.pack(pady=10)

        # Create 4x4 board filled with zeros
        self.board = [[0 for _ in range(4)] for _ in range(4)]

        # Store label references for each tile
        self.tiles = [[None for _ in range(4)] for _ in range(4)]

        # Create labels (tiles) for each cell in 4x4 grid
        for r in range(4):
            for c in range(4):
                label = tk.Label(self.frame, text="", width=4, height=2,
                                 font=("Arial", 20, "bold"),
                                 bg="lightgray", fg="#776e65",
                                 relief="ridge", bd=4)
                label.grid(row=r, column=c, padx=5, pady=5)  # Place in grid
                self.tiles[r][c] = label                     # Save reference

        # Start game with two random tiles
        self.add_random_tile()
        self.add_random_tile()
        self.update_board()

        # Bind arrow keys to movement functions
        self.root.bind("<Left>", lambda event: self.key_press("Left"))
        self.root.bind("<Right>", lambda event: self.key_press("Right"))
        self.root.bind("<Up>", lambda event: self.key_press("Up"))
        self.root.bind("<Down>", lambda event: self.key_press("Down"))

    # -------------------- GAME LOGIC FUNCTIONS --------------------

    # Add a random tile (2 or 4) in an empty cell
    def add_random_tile(self):
        empty = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] == 0]  # Find empty spots
        if empty:
            r, c = random.choice(empty)             # Pick random empty cell
            self.board[r][c] = random.choice([2, 4])  # Place 2 or 4

    # Update the GUI grid based on board values
    def update_board(self):
        # Define color scheme for different tile values
        colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
            128: "#edcf72", 256: "#edcc61", 512: "#edc850",
            1024: "#edc53f", 2048: "#edc22e"
        }

        # Loop through all cells to update label text & color
        for r in range(4):
            for c in range(4):
                val = self.board[r][c]               # Get current tile value
                label = self.tiles[r][c]             # Get label reference
                label.config(
                    text=str(val) if val != 0 else "",            # Show number or empty
                    bg=colors.get(val, "#3c3a32"),                # Get color from dict
                    fg="#776e65" if val <= 4 else "white"         # Text color
                )

        # Update score label text
        self.score_label.config(text=f"Score: {self.score}")

    # Move all non-zero numbers to the left (compress)
    def compress(self, row):
        new_row = [i for i in row if i != 0]        # Remove zeros
        new_row += [0] * (4 - len(new_row))         # Fill remaining with zeros
        return new_row

    # Merge adjacent equal numbers in a row
    def merge(self, row):
        for i in range(3):                          # Loop till 3rd element
            if row[i] != 0 and row[i] == row[i + 1]:  # Check for merge condition
                row[i] *= 2                         # Double the number
                self.score += row[i]                # Add to score
                row[i + 1] = 0                      # Set next to zero
        return row

    # Move left operation
    def move_left(self):
        moved = False
        new_board = []
        for row in self.board:
            compressed = self.compress(row)         # Step 1: Remove zeros
            merged = self.merge(compressed)         # Step 2: Merge equal numbers
            new_row = self.compress(merged)         # Step 3: Compress again
            new_board.append(new_row)
            if new_row != row:                      # Check if anything changed
                moved = True
        self.board = new_board                      # Update board
        return moved

    # Move right operation
    def move_right(self):
        moved = False
        new_board = []
        for row in self.board:
            reversed_row = row[::-1]                # Reverse row for right move
            compressed = self.compress(reversed_row)
            merged = self.merge(compressed)
            new_row = self.compress(merged)[::-1]   # Reverse back
            new_board.append(new_row)
            if new_row != row:
                moved = True
        self.board = new_board
        return moved

    # Move up operation
    def move_up(self):
        self.board = [list(x) for x in zip(*self.board)]  # Transpose to treat cols as rows
        moved = self.move_left()                          # Use left move logic
        self.board = [list(x) for x in zip(*self.board)]  # Transpose back
        return moved

    # Move down operation
    def move_down(self):
        self.board = [list(x) for x in zip(*self.board)]  # Transpose
        moved = self.move_right()                         # Use right move logic
        self.board = [list(x) for x in zip(*self.board)]  # Transpose back
        return moved

    # Handle key presses (arrow keys)
    def key_press(self, direction):
        moved = False

        # Determine which direction to move
        if direction == "Left":
            moved = self.move_left()
        elif direction == "Right":
            moved = self.move_right()
        elif direction == "Up":
            moved = self.move_up()
        elif direction == "Down":
            moved = self.move_down()

        # If board changed, add a new random tile and update display
        if moved:
            self.add_random_tile()
            self.update_board()

# -------------------- RUN THE GAME --------------------

if __name__ == "__main__":
    root = tk.Tk()            # Create main window
    game = Game2048(root)     # Initialize game class
    root.mainloop()           # Start Tkinter event loop
