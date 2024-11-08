#!/usr/bin/env python
import copy
import rospy
import yaml
from geometry_msgs.msg import Pose, PoseArray
from practica1.msg import Obstaculo
from sensor_msgs.msg import JointState

# Función que lee la configuración de un yaml y la devuelve.
def get_conf(archivo="/home/laboratorio/ros_workspace/src/practica1/src/practica1/yamls/conf.yaml") -> JointState:
    with open(archivo, "r") as f:
        conf_data = yaml.safe_load(f)
        conf_position = conf_data["conf"]

        conf = JointState()
        conf.header.stamp = rospy.Time.now()
        conf.position = conf_position

    return conf

# Función que lee la pose de un yaml y la devuelve.
def get_pose(archivo="/home/laboratorio/ros_workspace/src/practica1/src/practica1/yamls/pose.yaml") -> Pose:
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

# Función que a partir de una pose crea otra cambiando el eje X
def create_pose(pose_init: Pose) -> Pose:
    new_pose = copy.deepcopy(pose_init)
    new_pose.position.x += 0.1

    return new_pose

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

# Función que crea obstáculos. En este caso el suelo.
def create_obstacle() -> Obstaculo:
    pose_suelo = Pose()
    pose_suelo.position.x = 0.0
    pose_suelo.position.y = 0.0
    pose_suelo.position.z = -0.026

    obstacle = Obstaculo()
    obstacle.pose_caja = pose_suelo
    obstacle.name = 'suelo'
    obstacle.tamaño = [2, 2, .05]

    return obstacle

# Función que publica en los topics las acciones que quiere realizar el usuario.
def publish():
    # Configuración de rospy
    rospy.init_node('publisher', anonymous=True)
    topic_pose = rospy.Publisher("mover_pose", Pose, queue_size=10)
    topic_conf = rospy.Publisher("mover_configuracion", JointState, queue_size=10)
    topic_trajectory = rospy.Publisher("trayectoria_cartesiana", PoseArray, queue_size=10)
    topic_obstacle = rospy.Publisher("añadir_obstaculo", Obstaculo, queue_size=10)
    rate = rospy.Rate(1)

    # Leer los archivos yaml
    conf_init = get_conf()
    pose_init = get_pose()

    print("===============================================")
    print('0 -> Crear obstáculo que sirva como suelo.')
    print('1 -> Mover a la configuración del yaml.')
    print('2 -> Mover a la pose del yaml.')
    print('3 -> Mover según la trayectoria.')
    print("===============================================")

    while not rospy.is_shutdown():

        # Pedir al usuario qué enviar.
        order = int(input("Ingresa la acción: "))

        if order == 0:
            obstacle = create_obstacle()
            topic_obstacle.publish(obstacle)

        elif order == 1:
            topic_conf.publish(conf_init)

        elif order == 2:
            topic_pose.publish(pose_init)

        elif order == 3:
            pose = create_pose(pose_init)
            trajectory_msg = create_trajectory(pose)
            topic_trajectory.publish(trajectory_msg)

        else:
            break

        rate.sleep() 

if __name__ == "__main__":
    try:
        publish()
    except rospy.ROSInterruptException:
        pass