
(cl:in-package :asdf)

(defsystem "neuro_recv-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "dish_state" :depends-on ("_package_dish_state"))
    (:file "_package_dish_state" :depends-on ("_package"))
  ))