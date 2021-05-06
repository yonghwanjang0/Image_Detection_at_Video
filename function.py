import os


log_save_root = "log/"
accuracy_option = "accuracy.txt"


def make_folder(folder_path):
    folder_check = os.path.isdir(folder_path)
    if folder_check is False:
        os.makedirs(folder_path)


def make_folder_tree(root, time_object, time_string):
    year = str(time_object.tm_year)
    month = str(time_object.tm_mon).zfill(2)
    first_folder_name = year + "y_" + month

    if root[-1] == "/":
        output = "{0}{1}/{2}/".format(root, first_folder_name, time_string)
    else:
        output = "{0}/{1}/{2}/".format(root, first_folder_name, time_string)

    return output


def text_save(path, value):
    with open(path, mode='w') as t:
        t.write(value)


def time_converter(timestamp):
    origin_seconds = int(timestamp) // 1000

    hour = origin_seconds // 3600
    origin_seconds = origin_seconds % 3600

    minute = origin_seconds // 60
    second = origin_seconds % 60

    if hour:
        time_str = "{}:{}:{}".format(
            str(hour), str(minute).zfill(2), str(second).zfill(2))
    elif minute:
        time_str = "{}:{}".format(str(minute), str(second).zfill(2))
    else:
        time_str = "0:{}".format(str(second).zfill(2))

    output_str = "{} / {}".format(time_str, str(origin_seconds))

    return output_str
