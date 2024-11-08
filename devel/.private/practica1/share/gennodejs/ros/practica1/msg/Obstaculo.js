// Auto-generated. Do not edit!

// (in-package practica1.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------

class Obstaculo {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.pose_caja = null;
      this.name = null;
      this.tamaño = null;
    }
    else {
      if (initObj.hasOwnProperty('pose_caja')) {
        this.pose_caja = initObj.pose_caja
      }
      else {
        this.pose_caja = new geometry_msgs.msg.Pose();
      }
      if (initObj.hasOwnProperty('name')) {
        this.name = initObj.name
      }
      else {
        this.name = '';
      }
      if (initObj.hasOwnProperty('tamaño')) {
        this.tamaño = initObj.tamaño
      }
      else {
        this.tamaño = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Obstaculo
    // Serialize message field [pose_caja]
    bufferOffset = geometry_msgs.msg.Pose.serialize(obj.pose_caja, buffer, bufferOffset);
    // Serialize message field [name]
    bufferOffset = _serializer.string(obj.name, buffer, bufferOffset);
    // Serialize message field [tamaño]
    bufferOffset = _arraySerializer.float32(obj.tamaño, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Obstaculo
    let len;
    let data = new Obstaculo(null);
    // Deserialize message field [pose_caja]
    data.pose_caja = geometry_msgs.msg.Pose.deserialize(buffer, bufferOffset);
    // Deserialize message field [name]
    data.name = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [tamaño]
    data.tamaño = _arrayDeserializer.float32(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.name);
    length += 4 * object.tamaño.length;
    return length + 64;
  }

  static datatype() {
    // Returns string type for a message object
    return 'practica1/Obstaculo';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'f18e27135568d04082f7d3b8323e1a5b';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    geometry_msgs/Pose pose_caja
    string name
    float32[] tamaño
    ================================================================================
    MSG: geometry_msgs/Pose
    # A representation of pose in free space, composed of position and orientation. 
    Point position
    Quaternion orientation
    
    ================================================================================
    MSG: geometry_msgs/Point
    # This contains the position of a point in free space
    float64 x
    float64 y
    float64 z
    
    ================================================================================
    MSG: geometry_msgs/Quaternion
    # This represents an orientation in free space in quaternion form.
    
    float64 x
    float64 y
    float64 z
    float64 w
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Obstaculo(null);
    if (msg.pose_caja !== undefined) {
      resolved.pose_caja = geometry_msgs.msg.Pose.Resolve(msg.pose_caja)
    }
    else {
      resolved.pose_caja = new geometry_msgs.msg.Pose()
    }

    if (msg.name !== undefined) {
      resolved.name = msg.name;
    }
    else {
      resolved.name = ''
    }

    if (msg.tamaño !== undefined) {
      resolved.tamaño = msg.tamaño;
    }
    else {
      resolved.tamaño = []
    }

    return resolved;
    }
};

module.exports = Obstaculo;
