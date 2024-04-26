import os, shutil
from sklearn.model_selection import train_test_split

val_size = 0.1
test_size = 0.2

annotation_postfix = 'txt'
image_postfix = 'jpeg'
image_postfix_len=len(image_postfix)+1

imgpath = './MyData/origin/Image'
txtpath = './MyData/origin/Annotation'

split_root_path='./MyData/split/'
os.makedirs(split_root_path+'images/train', exist_ok=True)
os.makedirs(split_root_path+'images/valid', exist_ok=True)
os.makedirs(split_root_path+'images/test', exist_ok=True)
os.makedirs(split_root_path+'labels/train', exist_ok=True)
os.makedirs(split_root_path+'labels/valid', exist_ok=True)
os.makedirs(split_root_path+'labels/test', exist_ok=True)

listdir = os.listdir(imgpath)
train, test = train_test_split(listdir, test_size=test_size, shuffle=True, random_state=0)
train, val = train_test_split(train, test_size=val_size, shuffle=True, random_state=0)

for i in train:
    shutil.copy('{}/{}.{}'.format(imgpath, i[:-image_postfix_len], image_postfix), split_root_path+'images/train/{}.{}'.format(i[:-image_postfix_len], image_postfix))
    shutil.copy('{}/{}.{}'.format(txtpath, i[:-image_postfix_len],annotation_postfix), split_root_path+'labels/train/{}.{}'.format(i[:-image_postfix_len], annotation_postfix))

for i in val:
    shutil.copy('{}/{}.{}'.format(imgpath, i[:-image_postfix_len], image_postfix), split_root_path+'images/valid/{}.{}'.format(i[:-image_postfix_len], image_postfix))
    shutil.copy('{}/{}.{}'.format(txtpath, i[:-image_postfix_len],annotation_postfix), split_root_path+'labels/valid/{}.{}'.format(i[:-image_postfix_len], annotation_postfix))

for i in test:
    shutil.copy('{}/{}.{}'.format(imgpath, i[:-image_postfix_len], image_postfix), split_root_path+'images/test/{}.{}'.format(i[:-image_postfix_len], image_postfix))
    shutil.copy('{}/{}.{}'.format(txtpath, i[:-image_postfix_len],annotation_postfix), split_root_path+'labels/test/{}.{}'.format(i[:-image_postfix_len], annotation_postfix))