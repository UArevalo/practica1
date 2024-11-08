; Auto-generated. Do not edit!


(cl:in-package practica1-msg)


;//! \htmlinclude Obstaculo.msg.html

(cl:defclass <Obstaculo> (roslisp-msg-protocol:ros-message)
  ((pose_caja
    :reader pose_caja
    :initarg :pose_caja
    :type geometry_msgs-msg:Pose
    :initform (cl:make-instance 'geometry_msgs-msg:Pose))
   (name
    :reader name
    :initarg :name
    :type cl:string
    :initform "")
   (tamaño
    :reader tamaño
    :initarg :tamaño
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass Obstaculo (<Obstaculo>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Obstaculo>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Obstaculo)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name practica1-msg:<Obstaculo> is deprecated: use practica1-msg:Obstaculo instead.")))

(cl:ensure-generic-function 'pose_caja-val :lambda-list '(m))
(cl:defmethod pose_caja-val ((m <Obstaculo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader practica1-msg:pose_caja-val is deprecated.  Use practica1-msg:pose_caja instead.")
  (pose_caja m))

(cl:ensure-generic-function 'name-val :lambda-list '(m))
(cl:defmethod name-val ((m <Obstaculo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader practica1-msg:name-val is deprecated.  Use practica1-msg:name instead.")
  (name m))

(cl:ensure-generic-function 'tamaño-val :lambda-list '(m))
(cl:defmethod tamaño-val ((m <Obstaculo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader practica1-msg:tamaño-val is deprecated.  Use practica1-msg:tamaño instead.")
  (tamaño m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Obstaculo>) ostream)
  "Serializes a message object of type '<Obstaculo>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'pose_caja) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'name))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'tamaño))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'tamaño))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Obstaculo>) istream)
  "Deserializes a message object of type '<Obstaculo>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'pose_caja) istream)
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'tamaño) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'tamaño)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Obstaculo>)))
  "Returns string type for a message object of type '<Obstaculo>"
  "practica1/Obstaculo")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Obstaculo)))
  "Returns string type for a message object of type 'Obstaculo"
  "practica1/Obstaculo")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Obstaculo>)))
  "Returns md5sum for a message object of type '<Obstaculo>"
  "f18e27135568d04082f7d3b8323e1a5b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Obstaculo)))
  "Returns md5sum for a message object of type 'Obstaculo"
  "f18e27135568d04082f7d3b8323e1a5b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Obstaculo>)))
  "Returns full string definition for message of type '<Obstaculo>"
  (cl:format cl:nil "geometry_msgs/Pose pose_caja~%string name~%float32[] tamaño~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Obstaculo)))
  "Returns full string definition for message of type 'Obstaculo"
  (cl:format cl:nil "geometry_msgs/Pose pose_caja~%string name~%float32[] tamaño~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Obstaculo>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'pose_caja))
     4 (cl:length (cl:slot-value msg 'name))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'tamaño) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Obstaculo>))
  "Converts a ROS message object to a list"
  (cl:list 'Obstaculo
    (cl:cons ':pose_caja (pose_caja msg))
    (cl:cons ':name (name msg))
    (cl:cons ':tamaño (tamaño msg))
))
