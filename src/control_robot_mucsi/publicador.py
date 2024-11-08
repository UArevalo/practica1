import rospy
from std_msgs.msg import String

rospy.init_node("publicador", anonymous=True)

publisher = rospy.Publisher("pruebas", String, queue_size=10)

rospy.sleep(.5)
msg_enviar = String()
msg_enviar.data = "Hola mundo"

sleep_compensador = rospy.Rate(10)

while True:
    publisher.publish(msg_enviar)
    sleep_compensador.sleep()
