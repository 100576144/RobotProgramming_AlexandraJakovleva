#!/usr/bin/env python3

import rospy
from game_control.msg import user_msg
from std_msgs.msg import String, Int64
import os

class MazeGameNode:
    def __init__(self):
        rospy.init_node('game_node', anonymous=True)
        
        # Subscribers
        self.user_sub = rospy.Subscriber('user_information', user_msg, self.user_callback)
        self.control_sub = rospy.Subscriber('keyboard_control', String, self.control_callback)
        
        # Publishers
        self.score_pub = rospy.Publisher('result_information', Int64, queue_size=10)
        
        # Game state
        self.user_info = None
        self.current_direction = None
        self.phase = "welcome"
        
        # Maze game setup
        self.setup_maze()
        
        rospy.loginfo("Maze Game node initialized - Waiting for user information...")
    
    def setup_maze(self):
        """Initialize maze structure and game variables"""
        # 10x10 maze (0 = path, 1 = wall, 2 = start, 3 = end)
        self.maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 3, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        # Find start and end positions
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if self.maze[y][x] == 2:  # Start
                    self.player_x, self.player_y = x, y
                elif self.maze[y][x] == 3:  # End
                    self.end_x, self.end_y = x, y
        
        self.move_count = 0
        self.score = 100  # Start with 100 points, lose points for moves
        self.game_completed = False
    
    def user_callback(self, data):
        """Handle incoming user information"""
        if self.phase == "welcome":
            self.user_info = data
            self.welcome_phase()
    
    def control_callback(self, data):
        """Handle incoming movement commands"""
        if self.phase == "game" and not self.game_completed:
            self.current_direction = data.data
            self.game_phase()
    
    def welcome_phase(self):
        """Phase 1: Welcome - Display game introduction"""
        rospy.loginfo("=== WELCOME PHASE STARTED ===")
        rospy.loginfo(f"Welcome to the Maze Game, {self.user_info.name}!")
        rospy.loginfo(f"Username: {self.user_info.username}, Age: {self.user_info.age}")
        rospy.loginfo("Navigate through the maze from START to END using arrow keys")
        rospy.loginfo("Avoid walls and find the shortest path!")
        rospy.loginfo("Starting score: 100 | Each move: -1 point")
        
        self.phase = "game"
        self.display_maze()
        rospy.loginfo("=== GAME PHASE STARTED ===")
    
    def is_valid_move(self, x, y):
        """Check if the move is valid (not a wall)"""
        return (0 <= x < len(self.maze[0]) and 
                0 <= y < len(self.maze) and 
                self.maze[y][x] != 1)
    
    def game_phase(self):
        """Phase 2: Game - Process movements and update game state"""
        if self.phase != "game" or not self.current_direction or self.game_completed:
            return
        
        rospy.loginfo(f"Movement: {self.current_direction}")
        
        # Calculate new position
        new_x, new_y = self.player_x, self.player_y
        
        if self.current_direction == "UP":
            new_y -= 1
        elif self.current_direction == "DOWN":
            new_y += 1
        elif self.current_direction == "LEFT":
            new_x -= 1
        elif self.current_direction == "RIGHT":
            new_x += 1
        
        # Check if move is valid
        if self.is_valid_move(new_x, new_y):
            old_x, old_y = self.player_x, self.player_y
            
            # Update player position
            self.player_x, self.player_y = new_x, new_y
            self.move_count += 1
            self.score = max(0, self.score - 1)  # Lose 1 point per move
            
            rospy.loginfo(f"Move to position: ({self.player_x}, {self.player_y})")
            rospy.loginfo(f"Moves: {self.move_count} | Score: {self.score}")
            
            self.display_maze()
            
            # Check if player reached the end
            if self.player_x == self.end_x and self.player_y == self.end_y:
                rospy.loginfo("🎉 Congratulations! You reached the end of the maze!")
                self.final_phase()
        else:
            rospy.loginfo("Invalid move! You hit a wall.")
    
    def final_phase(self):
        """Phase 3: Final - Calculate final score and publish results"""
        rospy.loginfo("=== FINAL PHASE STARTED ===")
        
        # Bonus for completing the maze
        completion_bonus = 50
        self.score += completion_bonus
        self.game_completed = True
        
        rospy.loginfo(f"Maze completed in {self.move_count} moves!")
        rospy.loginfo(f"Final score: {self.score} (including {completion_bonus} bonus points)")
        
        # Publish final score
        score_msg = Int64()
        score_msg.data = self.score
        self.score_pub.publish(score_msg)
        
        rospy.loginfo("Score published to result_information topic!")
        self.display_final_stats()
        self.phase = "completed"
    
    def display_maze(self):
        """Display the current maze state with player position"""
        os.system('clear')
        print("=== MAZE GAME ===")
        print(f"Player: {self.user_info.username} | Moves: {self.move_count} | Score: {self.score}")
        print(f"Position: ({self.player_x}, {self.player_y}) | Target: ({self.end_x}, {self.end_y})")
        print()
        
        for y in range(len(self.maze)):
            row_display = ""
            for x in range(len(self.maze[0])):
                if x == self.player_x and y == self.player_y:
                    row_display += "😊 "  # Player
                elif x == self.end_x and y == self.end_y:
                    row_display += "🏁 "  # End
                elif self.maze[y][x] == 2:
                    row_display += "🚩 "  # Start
                elif self.maze[y][x] == 1:
                    row_display += "██ "  # Wall
                else:
                    row_display += "·  "  # Path
            
            print(row_display)
        
        print("\nControls: Arrow Keys to move | 'q' to quit control node")
        print("Legend: 😊=You 🚩=Start 🏁=End ██=Wall ·=Path")
    
    def display_final_stats(self):
        """Display final game statistics"""
        os.system('clear')
        print("🎉 MAZE COMPLETED! 🎉")
        
        # Performance rating
        if self.score >= 120:
            rating = "🏆 MAZE MASTER! Perfect navigation!"
        elif self.score >= 100:
            rating = "⭐ EXPORT EXPLORER! Excellent pathfinding!"
        elif self.score >= 80:
            rating = "👍 SKILLED NAVIGATOR! Well done!"
        else:
            rating = "💪 MAZE COMPLETED! Good effort!"
        
        print(f"Rating: {rating}")
        print("\nCheck the result_node terminal for final ROS results!")

if __name__ == '__main__':
    try:
        node = MazeGameNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass