#!/usr/bin/env python
import sys
import copy
import yaml
import rospy
from moveit_commander import MoveGroupCommander, RobotCommander, roscpp_initialize, PlanningSceneInterface
import moveit_msgs.msg
from math import pi, tau, dist, fabs, cos
from std_msgs.msg import String, Int32, Header
from moveit_commander.conversions import pose_to_list
from typing import List
from geometry_msgs.msg import Pose, PoseStamped, PoseArray
from sensor_msgs.msg import JointState


# Clase que contiene las funciones que mueven al robot
class ControlRobot:
    def __init__(self) -> None:
        # Configuración del robot
        roscpp_initialize(sys.argv)
        rospy.init_node("control_robot-v0", anonymous=True)
        self.robot = RobotCommander()
        self.scene = PlanningSceneInterface()
        self.group_name = 'robot'
        self.move_group = MoveGroupCommander(self.group_name)

        # Configuración de rospy
        self.order = rospy.Subscriber("consignas", Int32, self.callback)

    # Función que devuelve la configuración de los motores
    def get_motor_angles(self) -> list: 
        return self.move_group.get_current_joint_values()

    # Función que mueve el robot a una configuración de motores
    def move_motors(self, joint_goal: List[float]) -> bool:
        return self.move_group.go(joint_goal, wait=True) # wait=True para que el programa espere hasta finalizar movimiento antes de seguir.

    # Función que devuelve la pose actual del robot
    def get_pose(self) -> Pose: 
        return self.move_group.get_current_pose().pose

    # Función que mueve el robot a una Pose
    def move_to_pose(self, pose_goal: Pose)-> bool:
        self.move_group.set_pose_target(pose_goal)
        return self.move_group.go(wait=True) # wait=True para que el programa espere hasta finalizar movimiento antes de seguir.

    # Función que añade un obstáculo al entorno
    def add_to_planning_scene(self, pose_caja: Pose, name: str, tamaño: tuple = (.1, .1, .1)) -> None:
        box_pose = PoseStamped()
        box_pose.header.frame_id = 'base_link'
        box_pose.pose = pose_caja
        box_name = name
        self.scene.add_box(box_name, box_pose, size=tamaño)

    # Función que planifica y ejecuta una trayectoria
    def move_trajectory(self, poses: List[Pose], wait: bool = True) -> bool:
        (plan, fraction) = self.move_group.compute_cartesian_path(poses, 0.01, 0)

        if fraction != 1.0:
            print("Trayectoria Fallida")
            return False
        
        self.move_group.execute(plan, wait=wait)

    # Función que añade suelo
    def add_floor(self) -> None:
        pose_suelo = Pose()
        pose_suelo.position.z = -0.025 # Para no chocar con la base
        self.add_to_planning_scene(pose_suelo, 'suelo', (2, 2, .05)) 
    
    # Función que lee la configuración de un yaml y la devuelve.
    def get_conf_yaml(archivo="/home/laboratorio/ros_workspace/src/practica1/src/practica1/yamls/conf.yaml") -> JointState:
        with open(archivo, "r") as f:
            conf_data = yaml.safe_load(f)
            conf_position = conf_data["conf"]

            conf = JointState()
            conf.header.stamp = rospy.Time.now()
            conf.position = conf_position

        return conf

    # Función que lee la pose de un yaml y la devuelve.
    def get_pose_yaml(archivo="/home/laboratorio/ros_workspace/src/practica1/src/practica1/yamls/pose.yaml") -> Pose:
        with open(archivo, "r") as f:
            pose_data = yaml.safe_load(f)
            
        x_position = pose_data["pose"]["position"]["x"]
        y_position = pose_data["pose"]["position"]["y"]
        z_position = pose_data["pose"]["position"]["z"]
        w_orientation = pose_data["pose"]["orientation"]["w"]
        x_orientation = pose_data["pose"]["orientation"]["x"]
        y_orientation = pose_data["pose"]["orientation"]["y"]
        z_orientation = pose_data["pose"]["orientation"]["z"]

        # Pasar a tipo Pose
        pose = Pose()
        pose.position.x = x_position
        pose.position.y = y_position
        pose.position.z = z_position
        pose.orientation.w = w_orientation
        pose.orientation.x = x_orientation
        pose.orientation.y = y_orientation
        pose.orientation.z = z_orientation

        return pose
    
    # Función que a partir de una pose crea una trayectoria.
    def create_trajectory(pose: Pose) -> PoseArray:
        waypoints = [pose]

        pose.position.z -= 0.05
        waypoints.append(copy.deepcopy(pose))

        pose.position.x += 0.1
        waypoints.append(copy.deepcopy(pose))

        trajectory = PoseArray()
        trajectory.header.stamp = rospy.Time.now()
        trajectory.header.frame_id = "base_link"
        trajectory.poses = waypoints

        return trajectory

    def callback(self, data: Int32) -> None:
        msg = data.data

        if msg == 1:
            print('Añadiendo obstáculo que sirva como suelo')
            self.add_floor()

        elif msg == 2:
            print('Moviendo a la configuración deseada')
            self.position = self.get_conf_yaml()
            self.move_motors(self.position)

        elif msg == 3:
            print('Moviendo a la pose deseada')
            self.pose = self.get_pose_yaml()
            self.move_to_pose(self.pose)

        else:
            print('Realizando trayectoria')
            self.pose = self.get_pose()
            self.trajectory = self.create_trajectory(self.pose)
            self.move_trajectory(poses=self.trajectory, wait=True)            


if __name__ == "__main__":
    control = ControlRobot()
    rospy.spin()