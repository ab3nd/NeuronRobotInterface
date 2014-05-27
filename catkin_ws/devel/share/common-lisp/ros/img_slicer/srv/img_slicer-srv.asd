
(cl:in-package :asdf)

(defsystem "img_slicer-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "ImageSlicer" :depends-on ("_package_ImageSlicer"))
    (:file "_package_ImageSlicer" :depends-on ("_package"))
  ))