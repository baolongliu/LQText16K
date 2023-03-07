import os
import cv2
import json
import numpy as np
# fil_list = ['晟', '舟', '仁', '迁', '+', '逸', '毫', '潥', 'K', '卫', "'", '前', '鞍', '沪', '得']

def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                return True
        else:
                return False

def is_str_chinese(new_label):
    for index,char_ in enumerate(new_label):
        if not is_chinese(char_):
            break
    if index+1 == len(new_label):
        return True
    else:
        return False
 
def is_number(uchar):
        """判断一个unicode是否是数字"""
        if uchar >= u'\u0030' and uchar<=u'\u0039':
                return True
        else:
                return False
 
def is_alphabet(uchar):
        """判断一个unicode是否是英文字母"""
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
                return True
        else:
                return False
        

# 将字符后提
def modify_label(label:str):
    
    from string import ascii_letters
    tr_table = str.maketrans({c:None for c in ascii_letters})

    new_label = label.translate(tr_table)

    for key in label:
        if is_alphabet(key):
            new_label += key
    
    res = new_label
    
    return str(res).upper()

# 修改s1类型的字符顺序 
def modify_s1(label:str):
    label = modify_label(label)
    if not is_chinese(label[0]): 
        new_label = label[::-1]
    else:
        new_label = label
    
    # 如果全中文
    if is_str_chinese(new_label):
        new_label = new_label[::-1]

    # 删除拼音重新根据中文生成拼音,如果首字母为拼音
    if is_alphabet(new_label[0]):
        import pinyin
        flag = True
        for index,char_l in enumerate(new_label) :
            if not is_alphabet(char_l) and flag:
                final_label = new_label[index:]
                flag = False
        for char_ in final_label:
            if is_chinese(char_):
                pinyin_char:str = pinyin.get(char_,format='strip')
                final_label += pinyin_char.upper()
        return final_label
    else:
        return new_label
    
fontText = ImageFont.truetype("/media/data1/yrq/pan_pp.pytorch/simsun.ttc", 30, encoding="utf-8")

from PIL import Image, ImageDraw, ImageFont,ImageOps
def deal_img(json_file, jpg_path, out_path):

    image_polygs = Image.open(jpg_path)
    draw = ImageDraw.Draw(image_polygs)
   
    out_path_img = os.path.join(out_path,'images')
    if not os.path.exists(out_path_img):
        os.makedirs(out_path_img)
    with open(json_file, "r", encoding="utf-8") as f:
        strF = f.read()
        if len(strF) > 0:
            datas = json.loads(strF)
        else:
            datas = {}
      
        for index, i in enumerate(datas['shapes']):
            
            boxx1 = round(i['points'][0][0])
            boxy1 = round(i['points'][0][1])
            boxx2 = round(i['points'][1][0])
            boxy2 = round(i['points'][1][1])
            boxx3 = round(i['points'][2][0])
            boxy3 = round(i['points'][2][1])
            boxx4 = round(i['points'][3][0])
            boxy4 = round(i['points'][3][1])
            cnt = np.array([[boxx1, boxy1], [boxx2, boxy2], [boxx3, boxy3], [boxx4, boxy4]])

            try:
                if i['label'] == '*'  or '*' in str(i['label']):
                     continue
                
                tmp =  str(i['label']).split('-')
                if len(tmp) > 2 :
                    cls = tmp[0]
                    tmp_label = tmp[2:]
                    label = tmp[1]
                    for i in list(tmp_label):
                        label = label + '-' + i
                elif len(tmp) == 2:
                     cls , label = tmp

                if cls == '0' or cls == '6' :
                    continue

                if 's1' in cls:
                    label = modify_s1(label)
                else:
                    label = modify_label(label)
                
                
                x_max,y_max = np.amax(cnt, axis=0)
                draw.polygon(cnt.reshape(-1).tolist(), outline=(255, 0, 0),width=1)

                draw.text((x_max, y_max), label, (0, 255, 0), font=fontText)

            except Exception as e:
                print(e)
                print(i['label'],json_file)

    save_path = "poly.jpg"
    image_polygs.save(save_path)