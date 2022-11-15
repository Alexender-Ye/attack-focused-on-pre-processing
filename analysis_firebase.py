import re
import os
import csv
import time
prefix = "F:\\temp_application\photography\\"
log_file_path = "F:\\temp_application\\log\\firebase_stat.csv"

FIREBASE_STAT_TXT_PATH = "F:\\temp_application\\log\\constructor.txt"


def analyze(firebase):
    for t1 in firebase:
        current_path = prefix + t1 + "\\"
        total_dir = os.listdir(prefix + t1 + "\\");
        smali_dir = list()
        for temp in total_dir:
            if temp.find("smali") != -1:
                smali_dir.append(temp)
        for smali in smali_dir:
            for root, ds, fs in os.walk(current_path + smali):
                if root.find("kotlin\\") != -1:
                    continue
                if root.find("android\\") != -1:
                    continue
                if root.find("androidx\\") != -1:
                    continue
                if root.find("kotlinx\\") != -1:
                    continue
                if root.find("okhttp3\\") != -1:
                    continue
                if root.find("javax\\") != -1:
                    continue
                if root.find("okio\\") != -1:
                    continue
                if root.find("facebook\\") != -1:
                    continue
                if root.find("amazonaws\\") != -1:
                    continue
                for f in fs:
                    try:
                        if f.endswith('.smali'):
                            fullname = os.path.join(root, f)
                            f1 = open(fullname, "r")
                            content = f1.read()
                            smali_path = getSmaliPath(fullname)

                            # pattern = "(.method private constructor)(?:[\s\S]+?)(iput-object p1, p0, L" + smali_path + ";->[\w]{0,7}:Landroid/graphics/Matrix;)(?:[\s\S]+?return-void)"
                            # pattern2 = "(.method private constructor)(?:[\s\S]+?)(iput-object p5, p0, L" + smali_path + ";->[\w]{0,7}:Landroid/graphics/Matrix)(?:[\s\S]+?return-void)"
                            #变量数字变为\d
                            # pattern = "((?:.*)const/4 v2, 0x0(?:\s*)const v3, 0x32315659(?:\s*)if-eq p5, v3, :cond_1(?:.*))"
                            #
                            # pattern2 = "(.method [\w]{6,9} constructor[\s\S]+?getWidth[\s\S]+?getHeight[\s\S]+?)(const/4 p1, -0x1\s*)(iput p1, p0, L" + smali_path + ";->[\w]{0,7}:I\s*)(?:[\s\S]+?return-void)"
                            #
                            # pattern3 = "(.method [\w]{6,9} constructor[\s\S]+?)(const/16 p1, 0x23\s*)(iput p1, p0, L" + smali_path + ";->[\w]{0,7}:I\s*)(?:[\s\S]+?return-void)"

                            pattern = "((?:.*)const/4 v\d, 0x0(?:\s*)const v\d, 0x32315659(?:\s*)if-eq p\d, v\d, :cond_1(?:.*))"

                            pattern2 = "(.method [\w]{6,9} constructor[\s\S]+?getWidth[\s\S]+?getHeight[\s\S]+?)(const/4 p\d, -0x1\s*)(iput p\d, p\d, L" + smali_path + ";->[\w]{0,30}:I\s*)(?:[\s\S]+?return-void)"

                            pattern3 = "(.method [\w]{6,9} constructor[\s\S]+?)(const/16 p\d, 0x23\s*)(iput p\d, p\d , L" + smali_path + ";->[\w]{0,30}:I\s*)(?:[\s\S]+?return-void)"

                            # temp_result = re.findall(r"((?:.*)Imag   e dimension, ByteBuffer size(?:.*))", content)# 版本问题？
                            temp_result = re.findall(pattern, content)
                            temp_result2 = re.findall(pattern2, content)
                            temp_result3 = re.findall(pattern3, content)
                            #
                            if len(temp_result) != 0:
                                print(temp_result, fullname + "\n")
                            if len(temp_result2) != 0:
                                if temp_result2[0][0].find("return") == -1:
                                    print(temp_result2[0][1:], fullname + "\n")
                            if len(temp_result3) != 0:
                                if temp_result3[0][0].find("return") == -1:
                                    print(temp_result3[0][1:], fullname + "\n")
                                # outputToCsv(temp_result, fullname)

                    except BaseException:
                        continue


def outputToCsv(temp_result, fullname):
    with open(FIREBASE_STAT_TXT_PATH, 'a+') as f:
        f.write(temp_result + "111, " + fullname + "\n")


def read_csv_file():
    with open(log_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        column = [row[0] for row in reader]

    return column

def getSmaliPath(ori):
    b = ori.split("\\")
    target_index = 0
    for i in range(len(b)):
        if b[i].find("smali") != - 1:
            target_index = i
            break
    temp_result = b[target_index+1:]
    result = ""
    for temp in temp_result:
        result += temp + "/"
    return result[0:-7]

if __name__ == "__main__":
    firebase = read_csv_file()
    analyze(firebase[1:])


