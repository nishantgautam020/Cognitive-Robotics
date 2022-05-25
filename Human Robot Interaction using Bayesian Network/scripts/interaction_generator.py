#!/usr/bin/env python

import rospy
import random
import numpy as np
from cr_week8_test.msg import object_info
from cr_week8_test.msg import human_info




def interaction_generator(): 
    pub1 = rospy.Publisher('object_info', object_info, queue_size=10)  # First Topic Defined
    pub2 = rospy.Publisher('human_info', human_info, queue_size=10)   # Second Topic Defined
    rospy.init_node('interaction_generator')                          #initializing publisher
    rate= rospy.Rate(10)                                     #printing messages after 10 second

    obj = object_info()
    hum = human_info()
    int_d = 1
    while not rospy.is_shutdown():
	obj.id= int_d
        obj.object_size = round(np.random.uniform(1,3))

        hum.id = int_d
        hum.human_expression = round(np.random.uniform(1,3))
        hum.human_action = round(np.random.uniform(1,3))

	rospy.loginfo(obj)     
	rospy.loginfo(hum)
     
	pub1.publish(obj)
	pub2.publish(hum)
	rospy.sleep(10)             
 
        int_d = int_d+1

if __name__ == '__main__':
    try:
        interaction_generator()
    except rospy.ROSInterruptException:                            
        pass
