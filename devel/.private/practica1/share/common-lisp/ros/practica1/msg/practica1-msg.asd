
(cl:in-package :asdf)

(defsystem "practica1-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
)
  :components ((:file "_package")
    (:file "Obstaculo" :depends-on ("_package_Obstaculo"))
    (:file "_package_Obstaculo" :depends-on ("_package"))
  ))