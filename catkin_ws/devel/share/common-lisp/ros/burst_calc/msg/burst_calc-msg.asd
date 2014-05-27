
(cl:in-package :asdf)

(defsystem "burst_calc-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :neuro_recv-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "burst" :depends-on ("_package_burst"))
    (:file "_package_burst" :depends-on ("_package"))
    (:file "cat" :depends-on ("_package_cat"))
    (:file "_package_cat" :depends-on ("_package"))
    (:file "ranges" :depends-on ("_package_ranges"))
    (:file "_package_ranges" :depends-on ("_package"))
    (:file "ca" :depends-on ("_package_ca"))
    (:file "_package_ca" :depends-on ("_package"))
  ))