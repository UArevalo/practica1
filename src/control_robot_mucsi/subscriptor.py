import rospy
from std_msgs.msg import String

def cb_string(data: String) -> None:
    print(data.data)

rospy.init_node("subscriptor", anonymous=True)

suscriptor = rospy.Subscriber("pruebas", String, cb_string)

rospy.spin()