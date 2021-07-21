# Image_Detection_at_Video
This source code is find the video time and frame count that matches the image template pattern you have entered.

This source code makes for windows 10.

## use
* Select the video files folder.
* Copy the image file with the pattern you want to find to the '/template' folder. (please input only one image.)
* Press the Start Button or Keyboard F2 Button.
* Whenever matching pattern is found at file, timestamp result is printed in the result window.
* When the work starts, it scans all media files in the selected folder.

## result
* At the beginning of each file scan, the file name is printed first.
* Result text print like "playtime / total seconds" by the result window. (e.g. : 4:30 / 270)
* If all files have been work done. print "process finished" by the result window.

## requirements
* OpenCV
* PyQt5
