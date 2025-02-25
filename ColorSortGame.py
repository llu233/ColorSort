import tkinter as tk
from tkinter import messagebox
import copy

class BallSortGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Ball Sort Puzzle")
        
        # Define levels
        self.levels = [
            {  # Level 1
                "tubes": [
                    ["yellow", "green", "blue", "red"],
                    ["red", "blue", "green", "yellow"],
                    [],
                    [],
                    []
                ]
            },
            {  # Level 2
                "tubes": [
                    ["red", "blue", "green"],
                    ["green", "red", "blue"],
                    ["blue", "green", "red"],
                    [],
                    []
                ]
            },
            {  # Level 3
                "tubes": [
                    ["yellow", "blue", "red", "green"],
                    ["green", "red", "blue", "yellow"],
                    ["blue", "yellow", "green", "red"],
                    ["red", "green", "yellow", "blue"],
                    [],
                    []
                ]
            }
        ]
        self.current_level = 0  # Start at Level 1
        self.tubes = copy.deepcopy(self.levels[self.current_level]["tubes"])  # Initialize tubes for the current level
        self.selected_tube = None  # No tube is selected initially
        
        # Create a canvas to draw the tubes and balls
        self.canvas = tk.Canvas(self.root, width=600, height=300, bg="white")  # Increased width for more tubes
        self.canvas.pack()
        
        # Bind the canvas to handle mouse clicks
        self.canvas.bind("<Button-1>", self.on_tube_click)
        
        # Add buttons for reset and next level
        self.reset_btn = tk.Button(self.root, text="Reset Level", command=self.reset_level)
        self.reset_btn.pack(side=tk.LEFT)
        
        self.next_level_btn = tk.Button(self.root, text="Next Level", command=self.next_level, state=tk.DISABLED)
        self.next_level_btn.pack(side=tk.RIGHT)
        
        # Draw the initial state of the tubes
        self.draw_tubes()
    
    def draw_tubes(self):
        """Draw the tubes and balls on the canvas."""
        self.canvas.delete("all")  # Clear the canvas before redrawing
        for i, tube in enumerate(self.tubes):
            x = 50 + i * 90  # Adjusted spacing for more tubes
            color = "blue" if self.selected_tube == i else "black"  # Highlight selected tube
            self.canvas.create_rectangle(x, 50, x + 40, 265, outline=color, width=3)  # Draw the tube
            for j, ball_color in enumerate(tube):  # Draw balls from bottom to top
                y = 230 - j * 40  # Y position of the ball
                self.canvas.create_oval(x + 5, y, x + 35, y + 30, fill=ball_color, outline="black")  # Draw the ball
    
    def on_tube_click(self, event):
        """Handle mouse clicks on the canvas."""
        x, y = event.x, event.y
        tube_index = (x - 50) // 90  # Determine which tube was clicked (adjusted spacing for more tubes)
        if 0 <= tube_index < len(self.tubes):  # Ensure the click is within a valid tube
            self.select_tube(tube_index)
    
    def select_tube(self, index):
        """Select a tube or move a ball to the selected tube."""
        if self.selected_tube is None:  # If no tube is selected, select this one
            if self.tubes[index]:  # Only select if the tube is not empty
                self.selected_tube = index
        else:  # If a tube is already selected, move the ball
            self.move_ball(self.selected_tube, index)
            self.selected_tube = None  # Deselect the tube after moving
        self.draw_tubes()  # Redraw the tubes to reflect the changes
        self.check_win()  # Check if the player has won
    
    def move_ball(self, from_idx, to_idx):
        """Move the top ball from one tube to another."""
        if from_idx == to_idx:  # Cannot move to the same tube
            messagebox.showwarning("Invalid Move", "You cannot move a ball to the same tube.")
            return
        
        if not self.tubes[from_idx]:  # Cannot move from an empty tube
            messagebox.showwarning("Invalid Move", "The source tube is empty.")
            return
        
        moving_ball = self.tubes[from_idx][-1]  # Get the top ball from the source tube (last element in the list)
        
        # Debugging: Print the moving ball and the top ball of the destination tube
        print(f"Moving ball: {moving_ball}")
        if self.tubes[to_idx]:
            print(f"Top ball of destination tube: {self.tubes[to_idx][-1]}")
        
        if not self.tubes[to_idx]:  # Destination tube is empty
            self.tubes[to_idx].append(self.tubes[from_idx].pop())  # Move the ball
        elif self.tubes[to_idx][-1] == moving_ball:  # Destination tube has a ball of the same color
            self.tubes[to_idx].append(self.tubes[from_idx].pop())  # Move the ball
        else:
            messagebox.showwarning("Invalid Move", "You can only place a ball on top of the same color or an empty tube.")
        
        self.draw_tubes()  # Redraw the tubes to reflect the changes
    
    def check_win(self):
        """Check if the player has won the game."""
        for tube in self.tubes:
            if tube:  # If the tube is not empty
                if len(tube) < 2 or len(set(tube)) > 1:  # If the tube has fewer than 2 balls or balls of different colors
                    return  # The level is not completed
        
        # If all tubes are either empty or contain at least 2 balls of the same color, the level is completed
        messagebox.showinfo("Congratulations!", f"You completed Level {self.current_level + 1}!")
        self.next_level_btn.config(state=tk.NORMAL)  # Enable the "Next Level" button
    
    def reset_level(self):
        """Reset the current level to its initial state."""
        self.tubes = copy.deepcopy(self.levels[self.current_level]["tubes"])  # Reset tubes for the current level
        self.selected_tube = None
        self.next_level_btn.config(state=tk.DISABLED)  # Disable the "Next Level" button
        self.draw_tubes()
    
    def next_level(self):
        """Advance to the next level."""
        self.current_level += 1  # Move to the next level
        if self.current_level >= len(self.levels):  # If all levels are completed
            messagebox.showinfo("Game Over", "You have completed all levels!")
            self.current_level = 0  # Restart from Level 1
        
        self.tubes = copy.deepcopy(self.levels[self.current_level]["tubes"])  # Load tubes for the next level
        self.selected_tube = None
        self.next_level_btn.config(state=tk.DISABLED)  # Disable the "Next Level" button
        self.draw_tubes()

if __name__ == "__main__":
    root = tk.Tk()
    game = BallSortGame(root)
    root.mainloop()