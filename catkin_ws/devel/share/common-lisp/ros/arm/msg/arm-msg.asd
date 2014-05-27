
(cl:in-package :asdf)

(defsystem "arm-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "constant_move" :depends-on ("_package_constant_move"))
    (:file "_package_constant_move" :depends-on ("_package"))
    (:file "cartesian_move" :depends-on ("_package_cartesian_move"))
    (:file "_package_cartesian_move" :depends-on ("_package"))
    (:file "constant_move_time" :depends-on ("_package_constant_move_time"))
    (:file "_package_constant_move_time" :depends-on ("_package"))
    (:file "cartesian_moves" :depends-on ("_package_cartesian_moves"))
    (:file "_package_cartesian_moves" :depends-on ("_package"))
  ))