#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32

# Función que publica en los topics las acciones que quiere realizar el usuario.
def publish():
    # Configuración de rospy
    rospy.init_node('publisher-v0', anonymous=True)
    topic_consigna = rospy.Publisher("consignas", Int32, queue_size=10)
    rate = rospy.Rate(1)

    print("===============================================")
    print('0 -> Crear obstáculo que sirva como suelo.')
    print('1 -> Mover a la configuración del yaml.')
    print('2 -> Mover a la pose del yaml.')
    print('3 -> Mover según la trayectoria.')
    print("===============================================")
    
    # Pedir al usuario qué acción quiere realizar y enviarla.
    while not rospy.is_shutdown():

        order = int(input("Ingresa la acción: "))
        msg = Int32()
        msg.data = order
        topic_consigna.publish(msg)
        rate.sleep() # Esperar según lo indicado en rate.

if __name__ == "__main__":
    try:
        publish()
    except rospy.ROSInterruptException:
        pass