#!/usr/bin/env python

from __future__ import print_function
import sys
import rospy
from cr_week8_test.msg import *
from cr_week8_test.srv import predict_robot_expression
from cr_week8_test.srv import predict_robot_expressionResponse
from bayesian.bbn import *
from bayesian.exceptions import *
import message_filters


def robot_expression_prediction():
    try:	
	rospy.init_node('robot_expression_prediction')
    	prob_exp = rospy.Service('predict_robot_expression', predict_robot_expression, compute_prob)
    	print('service expression prediction')
    	rospy.spin()        
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


def compute_prob(req):
	O = req.object_size
	HA = req.human_action
	HE = req.human_expression
	print(O,HA,HE)
	robot_bbn = build_bbn(
			Ob_size,
			H_act,
			H_exp,
			R_exp,
			domains=dict(
				O = [ 1 ,  2 ],		
				HA = [ 1 ,  2 ,  3 ],
				HE = [ 1 ,  2 ,  3 ],
				RE = [ 1 ,  2 ,  3 ]))	
	
	if O == 0 and HA == 0 and HE == 0:
		rb = robot_bbn.query()
	elif O == 0 and HA == 0:
		rb = robot_bbn.query(HE=HE)
	elif O == 0 and HE == 0:
		rb = robot_bbn.query(HA=HA)
	elif HA == 0 and HE == 0:
		rb = robot_bbn.query(O=O)
	elif HE == 0:
		rb = robot_bbn.query(O=O, HA=HA)
	elif HA == 0:
		rb = robot_bbn.query(O=O, HE=HE)
	elif O == 0:
		rb = robot_bbn.query(HA=HA, HE=HE)
	else:
		rb = robot_bbn.query(O=O, HA=HA, HE=HE)

	prb = {n[1]:v for n,v in rb.items() if n[0]=='RE'}	
	
	return predict_robot_expressionResponse(prb[1], prb[2], prb[3])



def Ob_size(O):
	return 1.0/2.0

def H_act(HA):
	return 1.0/3.0

def H_exp(HE):
	return 1.0/3.0

def R_exp(O, HA, HE, RE):
	if RE == 1 :
		if HE == 1 and HA == 1 :
			if O == 1 :
				return 0.8
			elif O == 2 :
				return 1
		if HE == 1  and HA == 2 :
			if O == 1 :
				return 0.8
			elif O == 2 :
				return 1
		if HE == 1  and HA == 3 :
			if O == 1 :
				return 0.6
			elif O == 2 :
				return 0.8
		
		if HE == 2  and HA == 1 :
			if O == 1 :
				return 0.0
			elif O == 2 :
				return 0
		if HE == 2  and HA == 2 :
			if O == 1 :
				return 0.0
			elif O == 2 :
				return 0.1
		if HE == 2  and HA == 3 :
			if O == 1 :
				return 0.0
			elif O == 2 :
				return 0.2

		if HE == 3  and HA == 1 :
			if O == 1 :
				return 0.7
			elif O == 2 :
				return 0.8
		if HE == 3  and HA == 2 :
			if O == 1 :
				return 0.8
			elif O == 2 :
				return 0.9
		if HE == 3  and HA == 3 :
			if O == 1 :
				return 0.6
			elif O == 2 :
				return 0.7
	
	if RE == 2 :
		if HE == 1  and HA == 1 :
			if O == 1 :
				return 0.2
			elif O == 2 :
				return 0.0
		if HE == 1  and HA == 2 :
			if O == 1 :
				return 0.2
			elif O == 2 :
				return 0.0
		if HE == 1  and HA == 3 :
			if O == 1 :
				return 0.2
			elif O == 2 :
				return 0.2
		
		if HE == 2  and HA == 1 :
			if O == 1 :
				return 0.0
			elif O == 2 :
				return 0.0
		if HE == 2  and HA == 2 :
			if O == 1 :
				return 0.1
			elif O == 2 :
				return 0.1
		if HE == 2  and HA == 3 :
			if O == 1 :
				return 0.2
			elif O == 2 :
				return 0.2

		if HE == 3  and HA == 1 :
			if O == 1 :
				return 0.3
			elif O == 2 :
				return 0.2
		if HE == 3  and HA == 2 :
			if O == 1 :
				return 0.2
			elif O == 2 :
				return 0.1
		if HE == 3  and HA == 3 :
			if O == 1 :
				return 0.2
			elif O == 2 :
				return 0.2
	if RE == 3 :
		if HE == 1  and HA == 1 :
			if O == 1 :
				return 0.0
			elif O == 2 :
				return 0.0
		if HE == 1  and HA == 2 :
			if O == 1 :
				return 0.0
			elif O == 2 :
				return 0.0
		if HE == 1  and HA == 3 :
			if O == 1 :
				return 0.2
			elif O == 2 :
				return 0.0
		
		if HE == 2  and HA == 1 :
			if O == 1 :
				return 1.0
			elif O == 2 :
				return 1.0
		if HE == 2  and HA == 2 :
			if O == 1 :
				return 0.9
			elif O == 2 :
				return 0.8
		if HE == 2  and HA == 3 :
			if O == 1 :
				return 0.8
			elif O == 2 :
				return 0.6

		if HE == 3  and HA == 1 :
			if O == 1 :
				return 0.0
			elif O == 2 :
				return 0.0
		if HE == 3  and HA == 2 :
			if O == 1 :
				return 0.0
			elif O == 2 :
				return 0.0
		if HE == 3  and HA == 3 :
			if O == 1 :
				return 0.2
			elif O ==  2 :
				return 0.1

if __name__ == '__main__':
    try:
        robot_expression_prediction()
    except rospy.ROSInterruptException:
        pass
