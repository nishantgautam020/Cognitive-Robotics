#!/usr/bin/env python


import sys
import message_filters
from std_msgs.msg import Int64, Float64
import numpy as np
import rospy
from cr_week8_test.msg import object_info
from cr_week8_test.msg import human_info
from cr_week8_test.msg import perceived_info


def perception_filter():
    rospy.init_node('perception_filter')
    object_p = message_filters.Subscriber('object_info', object_info) 
    human_p = message_filters.Subscriber('human_info', human_info)
#   print(object_p)
#   print(human_p)
    tsyn = message_filters.ApproximateTimeSynchronizer([object_p, human_p], 10, 0.1, allow_headerless=True)
    tsyn.registerCallback(callback)
    rospy.spin()

def callback(object_info, human_info):    
    pub = rospy.Publisher('perceived_info', perceived_info, queue_size=10)
    info = perceived_info()
    O = object_info.object_size
    HA = human_info.human_action
    HE = human_info.human_expression 

    rand_var = round(np.random.uniform(1.9))
    print(rand_var)

    if rand_var == 1:
		O = 0
    elif rand_var == 2:
		HA = 0
    elif rand_var == 3:
		HE = 0
    elif rand_var == 4:
		O = 0
		HA = 0
    elif rand_var == 5:
		O = 0
		HE = 0
    elif rand_var == 6:
		HA = 0
		HE = 0
    elif rand_var == 7:
		O = 0
		HA = 0
		HE = 0

    info.id = object_info.id
    info.object_size = O
    info.human_action = HA
    info.human_expression = HE    
    rospy.loginfo(info)	
    pub.publish(info)



if __name__ == '__main__':
    try:
        perception_filter()
    except rospy.ROSInterruptException:
        pass
