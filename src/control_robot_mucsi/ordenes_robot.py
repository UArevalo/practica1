import rospy
from std_msgs.msg import String, Int16
from geometry_msgs.msg import Pose, PoseArray
from sensor_msgs.msg import JointState

rospy.init_node("nodo_ordenes", anonymous=True)

publisher_consignas = rospy.Publisher("consignas", Int16, queue_size=10)
publisher_mover_pose = rospy.Publisher("mover_pose", Pose, queue_size=10)
publisher_mover_configuracion = rospy.Publisher("mover_configuracion", JointState, queue_size=10)
publisher_trayectoria_cartesiana = rospy.Publisher("trayectoria_cartesiana", PoseArray, queue_size=10)
publisher_añadir_obstaculo = rospy.Publisher("añadir_obstaculo", String, queue_size=10)

rospy.sleep(.5)
consignas = Int16()
consignas.data = 0
publisher_mover_pose = Pose
publisher_mover_pose.position.x = 0.5
publisher_mover_pose.position.y = 0.5
publisher_mover_pose.position.z = 0.5

sleep_compensador = rospy.Rate(10)

while True:
    publisher_consignas.publish(consignas)
    sleep_compensador.sleep()
    print("Elegir que tipo de movimiento realizar")
    print("0-Salir")
    print("1-Añadir obstáculo")
    print("2-Mover a pose")
    print("3-Mover a configuración")
    print("4-Mover por trayectoria")