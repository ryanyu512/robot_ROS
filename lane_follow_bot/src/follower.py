import rospy
import cv2, cv_bridge
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

class Follower():
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        cv2.namedWindow("raw", 1)
        cv2.namedWindow("mask", 1)
        self.image_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
        self.twist = Twist()

    def image_callback(self, msg):
        #get raw image
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding = 'bgr8')
        #convert to hsv image
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        #obtain yellow path
        lower_yellow = np.array([ 10,  10,  10])
        upper_yellow = np.array([ 30, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        #define region of interest
        h, w, c = image.shape
        lb_h = int(3/4*h)
        ub_h = lb_h + 20

        mask[0:lb_h, 0:w] = 0
        mask[ub_h:h, 0:w] = 0

        M = cv2.moments(mask)
        print(M['m00'])
        if M['m00'] > 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(image, (cx, cy), 20, (0,0,255), -1)

            err = cx - w/2.
            self.twist.linear.x  = 0.2
            self.twist.angular.z = -float(err)/100. 

            self.cmd_vel_pub.publish(self.twist)

        
        cv2.imshow("mask", mask)
        cv2.imshow("raw", image)
        cv2.waitKey(3)        

rospy.init_node('follower')
follower = Follower()
rospy.spin()