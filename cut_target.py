import os
import cv2

path = 'C:/Users/FA FA/Desktop/result/hole-detect2'  # jpg图片和对应的生成结果的txt标注文件放在一个文件夹下
path2 = 'C:/Users/FA FA/Desktop/result/origin_image_crop'  # 被挖空目标框的原图
path3 = 'C:/Users/FA FA/Desktop/result/target_box'  # 裁剪出来的小图保存的根目录

os.makedirs(path2, exist_ok=True)
os.makedirs(path3, exist_ok=True)

file = os.listdir(path)
img_postfix = ".jpeg"
img_total = []
txt_total = []

fail_dection=[]

for filename in file:
    first, last = os.path.splitext(filename)
    if last == img_postfix :  # 图片的后缀名
        img_total.append(first)
    else:
        txt_total.append(first)

sum_num =len(img_total)
cur_num=1
for img_name in img_total:
    if img_name in txt_total:
        print('{}/{}'.format(cur_num,sum_num))
        cur_num+=1

        filename_img = img_name + img_postfix
        path1 = os.path.join(path, filename_img)
        img = cv2.imread(path1)
        h, w = img.shape[0], img.shape[1]
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_CUBIC)  # resize 图像大小，否则roi区域可能会报错
        filename_txt = img_name + ".txt"
        n = 1

        txt_content=[]
        with open(os.path.join(path, filename_txt), "r+", encoding="utf-8", errors="ignore") as f:
            for line in f:
                txt_content.append(line)
                coordinate = line.split(" ")
                x_center = w * float(coordinate[1])  # coordinate[1]为目标框中心点相对横坐标，x_center为中心点实际横坐标
                y_center = h * float(coordinate[2])  # coordinate[2]为目标框中心点相对纵坐标
                width = int(w * float(coordinate[3]))  # coordinate[3]为目标框相对宽
                height = int(h * float(coordinate[4]))  # coordinate[4]为目标框相对高

                lefttopx = int(x_center - width / 2.0) # 目标框左上角实际横坐标
                lefttopy = int(y_center - height / 2.0) # 目标框左上角实际纵坐标
                filename_last = img_name + "_" + str(n) + img_postfix # 裁剪出来的小图文件名
                roi = img[(lefttopy + 1):(lefttopy + height + 3) , (lefttopx + 1):(lefttopx + width + 1)]
                cv2.imwrite(os.path.join(path3, filename_last), roi)
                n = n + 1

        # 等裁剪完全部目标框再填充白像素，防止裁剪的目标框中含有白像素
        for line in txt_content: # 不for line in f:是因为这种写法不能重复，指针已经读到文件尾部了，除非再重新读文件一次，但浪费时间
            coordinate = line.split(" ")
            x_center = w * float(coordinate[1])  # coordinate[1]为目标框中心点相对横坐标，x_center为中心点实际横坐标
            y_center = h * float(coordinate[2])  # coordinate[2]为目标框中心点相对纵坐标
            width = int(w * float(coordinate[3]))  # coordinate[3]为目标框相对宽
            height = int(h * float(coordinate[4]))  # coordinate[4]为目标框相对高

            lefttopx = int(x_center - width / 2.0) # 目标框左上角实际横坐标
            lefttopy = int(y_center - height / 2.0) # 目标框左上角实际纵坐标

            img[(lefttopy + 1):(lefttopy + height + 3), (lefttopx + 1):(lefttopx + width + 1)] = (255, 255, 255)

        filename_last = img_name + "_crop" + img_postfix
        cv2.imwrite(os.path.join(path2, filename_last), img)
    else:
        print(img_name)
        fail_dection.append(img_name)
        continue

for t_img_name in fail_dection:
    print(t_img_name)