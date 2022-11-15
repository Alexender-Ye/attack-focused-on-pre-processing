import os
import xml.dom.minidom
import csv
TEMP_CATEGORY = 'temp\\'
CATEGORY = 'photography\\'
DOWNLOAD_PATH = 'F:\\temp_application\\'
MODEL_PATH = "\\assets\\"

PATH_FAILED_PATH = "F:\\temp_application\\log\\PATH_FAILED.txt"
TFLITE_LOG_PATH = "F:\\temp_application\\log\\tflite_app.txt"
FIREBASE_LOG_PATH = "F:\\temp_application\\log\\firebase_app.txt"
XML_FILE_NAME = "\\AndroidManifest.xml"
FIREBASE_STAT_CSV_PATH = "F:\\temp_application\\log\\firebase_stat.csv"

def analysis_app():
    # total apps
    total_app = 0
    tf_app = 0
    tf_using_mlkit = 0
    # open target file
    files = os.listdir(DOWNLOAD_PATH + CATEGORY)
    firebase_file_list= []
    firebase_final_list= []
    firebase_tflite_list = []
    for file in files:

        if os.path.isdir(DOWNLOAD_PATH + CATEGORY + file):
            total_app += 1
                # judge model path
            if os.path.exists(DOWNLOAD_PATH + CATEGORY + file + MODEL_PATH):

                # find tflite model
                tflite_list = findTffile(DOWNLOAD_PATH + CATEGORY + file + MODEL_PATH)
                if len(tflite_list) != 0:
                    tf_app += 1
                    #tflist_final_list.append(tflite_list)
                    with open(TFLITE_LOG_PATH, 'a+') as f:  # 设置文件对象
                        f.write(file + "\n")
                        f.writelines(tflite_list)
                        f.write("\n")
                    # find fssd model | xml file
                    mlkit_list = findMLkit(DOWNLOAD_PATH + CATEGORY + file + XML_FILE_NAME)
                    if len(mlkit_list) != 0:
                        tf_using_mlkit += 1
                        firebase_file_list.append(file)
                        firebase_final_list.append(",".join(mlkit_list))
                        firebase_tflite_list.append(",".join(tflite_list))
                        with open(FIREBASE_LOG_PATH, 'a+') as f:  # 设置文件对象
                            f.write(file + "\n")
                            f.writelines(mlkit_list)
                            f.write("\n")
                            # categorize the function of firebase
            else:
                # print()
                # print("MODEL PATH ERROR")
                with open(PATH_FAILED_PATH, 'a+') as f:  # 设置文件对象
                    f.write(file + "\n")
    writeToTargetCSV(firebase_file_list,firebase_final_list,firebase_tflite_list)
    return [total_app,tf_app,tf_using_mlkit]


def writeToTargetCSV(firebase_file_list, firebase_final_list, firebase_tflite_list):
    result = []
    header = ['App_name', 'xml_content', 'tflite_name']

    for i in range(len(firebase_file_list)):
        cur_list = list()
        cur_list.append(firebase_file_list[i])
        cur_list.append(firebase_final_list[i])
        cur_list.append(firebase_tflite_list[i])

        result.append(cur_list)

    with open(FIREBASE_STAT_CSV_PATH, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(result)


    #         tflite
    #         1. identify firebase
    #         xml -> mlkit
    #
    #         2. identify tensorflow obfuscation
    #         加壳与否？
    # iterate apps
    # invoke bak file(decompile_apktool.bat)
    #
    # 0. identify tf model
    #
    # tflite
    # 1. identify firebase
    # xml -> mlkit
    #
    # 2. identify tensorflow obfuscation
    # 加壳与否？


def findTffile(base):
    tf_file = []
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.tflite') or f.endswith('.pb') or \
                    f.endswith('.lite') or f.endswith("ckpt") or f.endswith("pbtxt"):
                fullname = os.path.join(root, f)
                tf_file.append(fullname)
    return tf_file


def findMLkit(path):
    dom = xml.dom.minidom.parse(path)

    root = dom.documentElement

    application_nodes = root.getElementsByTagName('application')

    service_nodes = application_nodes[0].getElementsByTagName('service')
    cur_result = []
    for node in service_nodes:
        service_name = node.getAttribute("android:name")

        if service_name.find("com.google.mlkit") != -1:

            metadata_nodes = node.getElementsByTagName("meta-data")
            for metadata in metadata_nodes:
                metadata_attr = metadata.getAttribute("android:name")
                cur_result.append(metadata_attr + "//111")
        if service_name.find("com.google.firebase") != -1:
            metadata_nodes = node.getElementsByTagName("meta-data")
            for metadata in metadata_nodes:
                if metadata.getAttribute("android:name").find(".ml") != -1:
                    cur_result.append(metadata.getAttribute("android:name") + "//222")

    return cur_result


def main():
    result = analysis_app()
    print(result)

if __name__ == "__main__":
    main()
