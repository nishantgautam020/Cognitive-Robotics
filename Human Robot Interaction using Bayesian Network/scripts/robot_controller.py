#!/usr/bin/env python

from __future__ import print_function
import message_filters
import sys
import rospy
import numpy as np
from cr_week8_test.srv import predict_robot_expression
from cr_week8_test.srv import predict_robot_expressionResponse
from cr_week8_test.msg import object_info, human_info
from cr_week8_test.msg import perceived_info
from cr_week8_test.msg import robot_info


def callback(data):   
	pro = service_expression(data.object_size, data.human_action, data.human_expression)
	pub = rospy.Publisher('robot_info', robot_info, queue_size=10)
	inf = robot_info()	
	inf.id = data.id
	inf.p_happy = pro[0]
	inf.p_sad = pro[1]
	inf.p_neutral = pro[2]
	rospy.loginfo(inf)
    	pub.publish(inf)

def robot_controller():
	rospy.init_node('robot_controller')
    	info = rospy.Subscriber('perceived_info', perceived_info, callback)	
    	rospy.spin()
	
def service_expression(object_size, human_action, human_expression):
    print('service call')
    rospy.wait_for_service('predict_robot_expression')
    try:
        compute_exp = rospy.ServiceProxy('predict_robot_expression', predict_robot_expression)
        resp1 = compute_exp(object_size, human_action, human_expression)
        return resp1.p_happy, resp1.p_sad, resp1.p_neutral
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


if __name__ == '__main__':
    try:
        robot_controller()
    except rospy.ROSInterruptException:
        pass
