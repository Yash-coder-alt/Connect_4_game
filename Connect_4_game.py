import tkinter as tk
from tkinter import messagebox
import random

# Constants for the game
ROWS = 6  # Number of rows on the game board
COLS = 7  # Number of columns on the game board
PLAYER = "🔵"  # Player's token
COMPUTER = "🔴"  # Computer's token


class ConnectFour:
    def __init__(self, root):
        # Initialize the game window
        self.root = root
        self.root.title("Connect Four")

        # Create an empty game board
        self.board = [["" for _ in range(COLS)] for _ in range(ROWS)]

        # List to hold the column selection buttons
        self.buttons = []

        # Create widgets for the game (buttons and labels)
        self.create_widgets()

    def create_widgets(self):
        # Create buttons for each column at the top
        for col in range(COLS):
            button = tk.Button(
                self.root, text="⬇", font=("Arial", 18),
                command=lambda c=col: self.player_move(c)  # Bind button to player's move
            )
            button.grid(row=0, column=col)  # Place the button in the first row
            self.buttons.append(button)

        # Create labels for the game grid
        self.labels = [
            [tk.Label(self.root, text="", font=("Arial", 24), width=4, height=2, bg="white", borderwidth=1,
                      relief="solid")
             for _ in range(COLS)] for _ in range(ROWS)
        ]

        # Place the labels on the grid
        for row in range(ROWS):
            for col in range(COLS):
                self.labels[row][col].grid(row=row + 1, column=col)  # Start from the second row

    def player_move(self, col):
        # Handle the player's move
        if self.drop_piece(col, PLAYER):  # Drop the player's token in the chosen column
            if self.check_winner(PLAYER):  # Check if the player has won
                messagebox.showinfo("Game Over", "You win!")  # Show a message if the player wins
                self.reset_game()  # Reset the game board
            else:
                self.computer_move()  # Let the computer take its turn

    def computer_move(self):
        # Handle the computer's move
        valid_moves = [col for col in range(COLS) if self.is_valid_column(col)]  # Get all valid columns

        # Check if the computer can win
        for col in valid_moves:
            if self.simulate_move(col, COMPUTER):  # Simulate a move for the computer
                self.drop_piece(col, COMPUTER)  # Place the winning token
                messagebox.showinfo("Game Over", "Computer wins!")  # Show a message if the computer wins
                self.reset_game()  # Reset the game board
                return

        # Block the player's winning move
        for col in valid_moves:
            if self.simulate_move(col, PLAYER):  # Simulate a move for the player
                self.drop_piece(col, COMPUTER)  # Block the player's winning move
                return

        # If no winning or blocking move, choose a random column
        col = random.choice(valid_moves)
        if self.drop_piece(col, COMPUTER):  # Place the token
            if self.check_winner(COMPUTER):  # Check if the computer has won
                messagebox.showinfo("Game Over", "Computer wins!")  # Show a message if the computer wins
                self.reset_game()  # Reset the game board

    def drop_piece(self, col, chip):
        # Drop a token into the lowest available row in the selected column
        for row in range(ROWS - 1, -1, -1):  # Start from the bottom row
            if self.board[row][col] == "":  # Find the first empty row
                self.board[row][col] = chip  # Place the token
                self.labels[row][col].config(text=chip,
                                             bg="lightblue" if chip == PLAYER else "lightpink")  # Update the label
                return True  # Return True to indicate success
        return False  # Return False if the column is full

    def is_valid_column(self, col):
        # Check if a column is valid for a move (not full)
        return self.board[0][col] == ""

    def simulate_move(self, col, chip):
        # Simulate a move and check if it results in a win
        for row in range(ROWS - 1, -1, -1):  # Start from the bottom row
            if self.board[row][col] == "":  # Find the first empty row
                self.board[row][col] = chip  # Temporarily place the token
                win = self.check_winner(chip)  # Check for a win
                self.board[row][col] = ""  # Undo the move
                return win  # Return True if it results in a win
        return False  # Return False if no win is possible

    def check_winner(self, chip):
        # Check for a win in horizontal, vertical, and diagonal directions
        for row in range(ROWS):
            for col in range(COLS - 3):  # Horizontal check
                if all(self.board[row][col + i] == chip for i in range(4)):
                    return True
        for row in range(ROWS - 3):
            for col in range(COLS):  # Vertical check
                if all(self.board[row + i][col] == chip for i in range(4)):
                    return True
        for row in range(ROWS - 3):
            for col in range(COLS - 3):  # Diagonal (bottom-right)
                if all(self.board[row + i][col + i] == chip for i in range(4)):
                    return True
        for row in range(ROWS - 3):
            for col in range(3, COLS):  # Diagonal (bottom-left)
                if all(self.board[row + i][col - i] == chip for i in range(4)):
                    return True
        return False  # Return False if no winner

    def reset_game(self):
        # Reset the game board for a new game
        for row in range(ROWS):
            for col in range(COLS):
                self.board[row][col] = ""  # Clear the board data
                self.labels[row][col].config(text="", bg="white")  # Reset the labels


# Create the game window
root = tk.Tk()
game = ConnectFour(root)
root.mainloop()
