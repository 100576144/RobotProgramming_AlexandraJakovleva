#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import termios
import sys
import tty
import select

class ControlNode:
    def __init__(self):
        rospy.init_node('control_node', anonymous=True)
        self.pub = rospy.Publisher('keyboard_control', String, queue_size=10)
        rospy.loginfo("Control node started - Use arrow keys for movement")
        rospy.loginfo("Press 'q' to quit")
        
    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            [i, o, e] = select.select([sys.stdin], [], [], 0.1)
            if i:
                key = sys.stdin.read(1)
                return key
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def run(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            key = self.get_key()
            if key == '\x1b':  # Arrow keys
                key2 = self.get_key()
                if key2 == '[':
                    key3 = self.get_key()
                    direction_map = {'A': 'UP', 'B': 'DOWN', 'C': 'RIGHT', 'D': 'LEFT'}
                    if key3 in direction_map:
                        msg = String()
                        msg.data = direction_map[key3]
                        self.pub.publish(msg)
                        rospy.loginfo(f"Movement: {msg.data}")
            elif key == 'q':
                rospy.loginfo("Quitting control node")
                break
            rate.sleep()

if __name__ == '__main__':
    try:
        node = ControlNode()
        node.run()
    except rospy.ROSInterruptException:
        pass