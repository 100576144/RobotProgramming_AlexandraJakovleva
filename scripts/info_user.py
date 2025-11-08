#!/usr/bin/env python3

import rospy
from game_control.msg import user_msg

class InfoUser:
    def __init__(self):
        rospy.init_node('info_user', anonymous=True)
        self.pub = rospy.Publisher('user_information', user_msg, queue_size=10)
        rospy.loginfo("Info User node started")
        
    def get_user_info(self):
        rospy.loginfo("=== USER INFORMATION ===")
        
        name = input("Enter your name: ")
        username = input("Enter your username: ")
        age = int(input("Enter your age: "))
        
        user_info = user_msg()
        user_info.name = name
        user_info.username = username
        user_info.age = age
        
        rospy.sleep(1)  # Wait for subscribers
        self.pub.publish(user_info)
        rospy.loginfo("User information published!")
        
        rospy.sleep(2)  # Keep node alive

if __name__ == '__main__':
    try:
        node = InfoUser()
        node.get_user_info()
    except rospy.ROSInterruptException:
        pass