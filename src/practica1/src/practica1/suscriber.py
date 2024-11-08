#!/usr/bin/env python
import rospy
import sys
from geometry_msgs.msg import Pose, PoseArray, PoseStamped
from moveit_commander import MoveGroupCommander, PlanningSceneInterface, RobotCommander, roscpp_initialize
from moveit_commander.conversions import pose_to_list
from sensor_msgs.msg import JointState
from typing import List
from practica1.msg import Obstaculo


# Clase que contiene las funciones que mueven al robot
class ControlRobot:
    def __init__(self) -> None:
        # Configuración del robot
        roscpp_initialize(sys.argv)
        rospy.init_node("control_robot", anonymous=True)
        self.robot = RobotCommander()
        self.scene = PlanningSceneInterface()
        self.group_name = 'robot'
        self.move_group = MoveGroupCommander(self.group_name)

        # Configuración de rospy
        self.pose_subscriber = rospy.Subscriber("mover_pose", Pose, self.pose_callback)
        self.conf_subscriber = rospy.Subscriber("mover_configuracion", JointState, self.conf_callback)
        self.trajectory_subscriber = rospy.Subscriber("trayectoria_cartesiana", PoseArray, self.trajectory_callback)
        self.obstacle_subscriber = rospy.Subscriber("añadir_obstaculo", Obstaculo, self.obstacle_callback)

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

    # Callback que mueve el robot a una Pose
    def pose_callback(self, pose: Pose) -> None:
        print("Moviendo a la pose deseada...")
        self.pose = pose
        self.move_to_pose(self.pose)

    # Callback que mueve el robot a una configuración
    def conf_callback(self, conf: JointState) -> None:
        print("Moviendo a la configuración")
        self.position = conf.position
        self.move_motors(self.position)
    
    # Callback que mueve el robot en una trayectoria
    def trajectory_callback(self, trajectory: PoseArray) -> None:
        print("Siguiendo trayectoria deseada...")
        # Añado la Pose actual como primera Pose.
        self.waypoints = trajectory.poses
        self.waypoints.insert(0, self.get_pose())
        self.move_trajectory(poses=self.waypoints, wait=True)

    # Callback que añade un obstáculo
    def obstacle_callback(self, obstacle: Obstaculo) -> None:
        print("Se ha añadido un obstaculo.")
        self.add_to_planning_scene(obstacle.pose_caja, obstacle.name, tuple(obstacle.tamaño))


if __name__ == "__main__":
    control = ControlRobot()
    rospy.spin()