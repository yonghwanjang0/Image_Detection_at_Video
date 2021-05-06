import cv2
import os
from function import accuracy_option, time_converter


def check_seconds(current_time, last_second):
    check_frame = False
    current_second = current_time // 1000
    if last_second < current_second:
        check_frame = True
        last_second = current_second

    return last_second, check_frame


class Finder:
    def __init__(self, queue, path):
        self.queue = queue
        self.folder_path = path
        self.file_list = next(os.walk(path))[2]
        self.video = None
        self.template = None
        self.accuracy_criterion = 0.94

    def set_video(self, file):
        self.video = cv2.VideoCapture(file)

    def set_template(self):
        path = "template/"
        file_list = next(os.walk(path))[2]
        
        if len(file_list) == 0:
            self.queue.put(
                ["Please input template image file in template folder."])
        else:
            file_path = path + file_list[0]
            self.template = cv2.imread(file_path)

    def set_accuracy_criterion(self):
        with open(accuracy_option, mode='r') as f:
            value = f.read()

        # set criterion accuracy - default value : 0.94 (94%)
        if value:
            self.accuracy_criterion = float(value)

    def find_start(self):
        first_iteration = True
        self.set_template()
        self.set_accuracy_criterion()

        if self.template is not None:
            for file in self.file_list:
                if not first_iteration:
                    self.queue.put([""])

                self.queue.put([file])
                path = self.folder_path + file
                self.set_video(path)
                self.find_position()

                if first_iteration:
                    first_iteration = False

    def find_position(self):
        last_find_time = -100000
        detect_interval = 10000
        last_seconds = 0
        check_frame = False

        count = 0
        ret = True

        while ret:
            current_play_time = self.video.get(cv2.CAP_PROP_POS_MSEC)
            last_seconds, check_frame = check_seconds(
                current_play_time, last_seconds)

            if not check_frame:
                ret = self.video.grab()
            else:
                ret, frame = self.video.read()
                if ret and count != 0:
                    exists = self.detect_pattern(frame)

                    if exists:
                        current_find_time = current_play_time
                        time_gap = current_find_time - last_find_time

                        if time_gap >= detect_interval:
                            timestamp_str = time_converter(current_find_time)
                            self.queue.put([timestamp_str])
                            last_find_time = current_find_time

            count += 1

    def detect_pattern(self, image):
        value = False
        accuracy_value = self.get_accuracy_value(image)
        if accuracy_value >= self.accuracy_criterion:
            value = True

        return value
    
    def get_accuracy_value(self, image):
        result = cv2.matchTemplate(
            image, self.template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        return max_val


def control_method(queue, folder):
    process = Finder(queue, folder)
    process.find_start()
    queue.put([""])
    queue.put(["process finished."])
