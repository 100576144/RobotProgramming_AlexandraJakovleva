#!/usr/bin/env python3

import rospy
from game_control.msg import user_msg
from std_msgs.msg import Int64

class ResultNode:
    def __init__(self):
        rospy.init_node('result_node', anonymous=True)
        
        # Subscribers (receives from BOTH info_user AND game_node)
        self.user_sub = rospy.Subscriber('user_information', user_msg, self.user_callback)
        self.score_sub = rospy.Subscriber('result_information', Int64, self.score_callback)
        
        # Store received data
        self.user_data = None
        self.final_score = None
        
        rospy.loginfo("Result node initialized - Waiting for game results...")
        
    def user_callback(self, data):
        self.user_data = data
        rospy.loginfo(f"Received user data: {data.name}")
        self.display_final_results()
    
    def score_callback(self, data):
        self.final_score = data.data
        rospy.loginfo(f"Received final score: {data.data}")
        self.display_final_results()
    
    def display_final_results(self):
        # Only display when we have BOTH user info AND score
        if self.user_data and self.final_score is not None:
            print("\n" + "="*50)
            print("🎉🎉🎉 FINAL GAME RESULTS 🎉🎉🎉")
            print("="*50)
            print(f"Player: {self.user_data.name}")
            print(f"Username: @{self.user_data.username}")
            print(f"Age: {self.user_data.age}")
            print(f"Final Score: {self.final_score}")
            print("-"*50)
            
            # Performance rating
            if self.final_score >= 70:
                rating = "🏆 MASTER NAVIGATOR! 🏆"
            elif self.final_score >= 50:
                rating = "⭐ EXPERT EXPLORER! ⭐"
            elif self.final_score >= 30:
                rating = "👍 SKILLED ADVENTURER! 👍"
            else:
                rating = "💪 GAME COMPLETED! 💪"
                
            print(f"Rating: {rating}")
            print("="*50)
            print("\n")

if __name__ == '__main__':
    try:
        node = ResultNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass