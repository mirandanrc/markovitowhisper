#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

if __name__ == '__main__':
     rospy.init_node('radiotestpy')

     pub = rospy.Publisher("/width_flag", String, queue_size=50)

     rate= rospy.Rate(2)

     while not rospy.is_shutdown():
          msg = String()
          msg.data = "hay_audio"
          pub.publish(msg)
          rate.sleep()

     rospy.loginfo("Node was stopped")