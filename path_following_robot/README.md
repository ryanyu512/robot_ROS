Instruction

1. cd path_following_robot
2. catkin_make
3. roslaunch turtlebot3_gazebo turtlebot3_yellow_lane_world.launch


follower.py: Define a follower class subscribing to the camera and publishing velocity command which is calculated based on P control. 

