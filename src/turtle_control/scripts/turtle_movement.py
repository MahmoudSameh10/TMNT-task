#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import sys, select, termios, tty

SPEED =5
# Key mappings
move_bindings = {
    'w': (SPEED, 0, 0, 0),
    's': (-SPEED, 0, 0, 0),
    'a': (0, 0, SPEED, 0),
    'd': (0, 0, -SPEED, 0),
}

def get_key():#to read inputs from the user without having to press enter
    tty.setraw(sys.stdin.fileno()) #switch terminal into raw mode, terminal reads byte by byte without buffering
    select.select([sys.stdin], [], [], 0) #to see if there is any input
    key = sys.stdin.read(1) #to read a byte from the terminal
    #termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)  incase we need to return terminal into its original setting
    return key

def main():
    rospy.init_node('turtle_wasd_control')

    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)


    global settings
    settings = termios.tcgetattr(sys.stdin) #takes current settings of the terminal

    print("Use WASD keys to move the turtle!")
    print("Press Ctrl+C to exit.")

    while not rospy.is_shutdown():
        key = get_key()

        if key in move_bindings.keys():
            x, y, z, th = move_bindings[key]
        else:
            x, y, z, th = 0, 0, 0, 0
            if key == '\x03':  # Ctrl+C
                break

        twist = Twist()
        twist.linear.x = x
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = z

        pub.publish(twist)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
