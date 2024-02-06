import rclpy
from rclpy.node import Node
from rclpy.action.client import ActionClient
from control_msgs.action import FollowJointTrajectory
from control_msgs.msg import JointTolerance
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from std_msgs.msg import String
from builtin_interfaces.msg import Duration
from argparse import ArgumentParser

def main():
    rclpy.init()
    node = Node("maci_node")

    parser = ArgumentParser(prog="maci_node")
    parser.add_argument("-j", help="set finger joint", type=float, default=0.0)

    args = parser.parse_args()
    
    ac = ActionClient(node, FollowJointTrajectory, "/gripper_controller/follow_joint_trajectory")
    
    ac.wait_for_server()
    print("server found")
    traj = JointTrajectory()
    traj.joint_names = ["finger_joint"]
    traj.points = [JointTrajectoryPoint(positions=[args.j])]
    
    
    goal = FollowJointTrajectory.Goal()
    goal.trajectory = traj
    goal.goal_time_tolerance = Duration(sec=1)
    
    tol = JointTolerance(name="finger_joint", position=0.001, velocity=0.001)
    
    print(traj)
    goal.path_tolerance = [tol]
    goal.goal_tolerance = [tol]
    
    res = ac.send_goal_async(goal)
    print("waiting for goal complete")
    rclpy.spin_until_future_complete(node, res)
    print('Hi from maci.')
    


if __name__ == '__main__':
    main()
