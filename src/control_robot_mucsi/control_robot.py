#!/usr/bin/python3
import sys
import copy
import rospy
import yaml
from moveit_commander import MoveGroupCommander, RobotCommander, roscpp_initialize, PlanningSceneInterface
import moveit_msgs.msg
from math import pi, tau, dist, fabs, cos
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from typing import List
import rospy
from std_msgs.msg import String, Int16
from geometry_msgs.msg import Pose, PoseArray, PoseStamped
from sensor_msgs.msg import JointState

class ControlRobot:
    def __init__(self) -> None:        
        self.robot = RobotCommander()
        self.scene = PlanningSceneInterface()
        self.group_name = "robot"
        self.move_group = MoveGroupCommander(self.group_name)
        self.add_floor()
        
    def get_motor_angles(self) -> list:
        return self.move_group.get_current_joint_values()
    
    def move_motors(self, joint_goal: list, wait: bool = True) -> bool:
        return self.move_group.go(joint_goal, wait=True) #Esperar a que finalice el movimiento wait=True
    
    def get_pose(self) -> Pose:
        return self.move_group.get_current_pose().pose
    
    def move_to_pose(self, pose_goal: Pose) -> bool:
        self.move_group.set_pose_target(pose_goal)
        return self.move_group.go(wait=True)
    
    def move_to_configuration(self, pose_goal: JointState) -> bool:
        self.move_group.set_pose_target(pose_goal)
        return self.move_group.go(wait=True)
    
    def add_box_to_planning_scene(self, pose_box: Pose, name:str, tamaño:tuple = [.1,.1,.1]) -> None:
        box_pose = PoseStamped()
        box_pose.header.frame_id = "base_link"
        box_pose.pose = pose_box
        box_name = name
        self.scene.add_box(box_name, box_pose, size=tamaño)
    
    def add_floor(self) -> None:
        pose_suelo = Pose()
        pose_suelo.position.z = -0.025
        self.add_box_to_planning_scene(pose_suelo, "suelo", [2,2,.03])
        
    def compute_line(self, waypoints: tuple):
        plan, fraction = self.move_group.compute_cartesian_path(waypoints, 0.01, 0.0)
        return plan, fraction
    
    def execute_move(self, plan) -> None:
        self.move_group.execute(plan, wait=True)
        
    def move_trayectory(self, poses: List[Pose], wait: bool = True) -> bool:
        poses.insert(0, self.get_pose())
        (plan, fraction) = self.move_group.compute_cartesian_path(poses, 0.01)  # jump_threshold
        
        if fraction != 1.0:
            return False

        return self.move_group.execute(plan, wait=wait)
    
    def save_pose(self, name: str, pose:Pose) -> None:
        diccionario_conf = {"Pose guardada": pose}

        with open(name + ".yaml", "+a") as f:
            yaml.dump(diccionario_conf)
            
    def load_pose(self, name: str) -> Pose:
        with open(name + ".yaml", "+r") as f:
            conf = yaml.load(f, yaml.Loader)
        return conf
    
    def save_conf_act(self):
        conf = self.get_motor_angles()

class ComandsRobot():
    def __init__(self) -> None: 
        roscpp_initialize(sys.argv)
        rospy.init_node("control_robot", anonymous=True)       
        rospy.Subscriber("consignas", Int16, self.read_consignas) 
        rospy.Subscriber("mover_pose", Pose, self.read_mover_pose) 
        rospy.Subscriber("mover_configuracion", JointState, self.read_mover_configuracion) 
        rospy.Subscriber("trayectoria_cartesiana", PoseArray, self.read_trayectoria_cartesiana) 
        rospy.Subscriber("añadir_obstaculo", String, self.read_añadir_obstaculo) 

    def read_consignas(self, data: Int16):
        self.consignas = data.data
        if self.consignas == 1:
            control.move_to_pose(self.mover_pose)
        elif self.consignas == 2:
            control.move_to_configuration(self.mover_configuracion)
        elif self.consignas == 3:
            control.move_trayectory(self.trayectoria_cartesiana)
        elif self.consignas == 4:
            control.add_box_to_planning_scene(self.añadir_obstaculo)
            
    def read_mover_pose(self, data: Pose):
        self.mover_pose = data
        
    def read_mover_configuracion(self, data: JointState):
        self.mover_configuracion = data.position
    
    def read_trayectoria_cartesiana(self, data: PoseArray):
        self.trayectoria_cartesiana = data.poses
        
    def read_añadir_obstaculo(self, data: String):
        self.añadir_obstaculo = data.data
            
if __name__ == '__main__':
    control = ControlRobot()
    ordenes = ComandsRobot()
    rospy.spin()
    pose_act = control.get_pose()
    waypoints = []

    pose_act.position.z -= 0.01  # First move up (z)
    pose_act.position.y += 0.02  # and sideways (y)
    waypoints.append(copy.deepcopy(pose_act))

    pose_act.position.x += 0.04  # Second move forward/backwards in (x)
    waypoints.append(copy.deepcopy(pose_act))

    pose_act.position.y -= 0.01  # Third move sideways (y)
    waypoints.append(copy.deepcopy(pose_act))
    #
    #plan, fraction = control.compute_line(waypoints)
    #control.execute_move(plan)
    mov = control.move_trayectory(waypoints)
    if mov:
        print("Movimiento correcto")