# coding:utf-8
import json
import os.path
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement


def parse_xml(folder_text, filename_text, path_text, width_text, height_text, name_text,
               xmin_text, ymin_text, xmax_text, ymax_text, output_name):
    root = Element('annotation')

    folder = SubElement(root, 'folder')
    folder.text = folder_text

    filename = SubElement(root, 'filename')
    filename.text = filename_text

    path = SubElement(root, 'path')
    path.text = path_text

    source = SubElement(root, 'source')
    database = SubElement(source, 'database')
    database.text = 'NEU-DET'

    size = SubElement(root, 'size')
    width = SubElement(size, 'width')
    height = SubElement(size, 'height')
    depth = SubElement(size, 'depth')
    width.text = width_text
    height.text = height_text
    depth.text = '3'

    segmented = SubElement(root, 'segmented')
    segmented.text = '0'

    object = SubElement(root, 'object')
    name = SubElement(object, 'name')
    name.text = name_text
    pose = SubElement(object, 'pose')
    pose.text = 'Unspecified'
    truncated = SubElement(object, 'truncated')
    truncated.text = '0'
    difficult = SubElement(object, 'difficult')
    difficult.text = '0'
    bndbox = SubElement(object, 'bndbox')
    xmin = SubElement(bndbox, 'xmin')
    xmin.text = xmin_text
    ymin = SubElement(bndbox, 'ymin')
    ymin.text = ymin_text
    xmax = SubElement(bndbox, 'xmax')
    xmax.text = xmax_text
    ymax = SubElement(bndbox, 'ymax')
    ymax.text = ymax_text

    tree = ET.ElementTree(root)

    pretty_xml(root, '\t', '\n')  # 执行美化方法

    # write out xml data
    tree.write(output_name, encoding='utf-8')


def pretty_xml(element, indent, newline, level=0):
    # 判断element是否有子元素
    if element:
        # 如果element的text没有内容
        if element.text is None or element.text.isspace():
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # 此处两行如果把注释去掉，Element的text也会另起一行
    # else:
    # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将element转成list
    for sub_element in temp:
        # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
        if temp.index(sub_element) < (len(temp) - 1):
            sub_element.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            sub_element.tail = newline + indent * level
            # 对子元素进行递归操作
        pretty_xml(sub_element, indent, newline, level=level + 1)


if __name__ == '__main__':
    with open('list.txt', 'r') as f:
        name_list = f.readlines()
        id_list = [name.strip('\n').split(".jpg")[0] for name in name_list]
    folder_text = 'desensitized'
    width_text = '1440'
    height_text = '1920'
    folder_path = os.path.join('/home', folder_text)
    annotation_path = 'Annotations'
    image_type = '.jpg'
    with open('train_label_public.json', 'r', encoding='utf8') as fp:
        train_label = json.load(fp)

    label_data = train_label['data']

    image_list = []
    for (key, value) in label_data.items():
        image_id = value['image_id']
        if image_id not in id_list:
            continue
        image_list.append(image_id + image_type)
        board_contour = value['board_contour']
        x_list = [item[0] for item in board_contour]
        x_list.sort()
        y_list = [item[1] for item in board_contour]
        y_list.sort()
        xmin_text = str(x_list[0])
        ymin_text = str(y_list[0])
        xmax_text = str(x_list[len(x_list) - 1])
        ymax_text = str(y_list[len(y_list) - 1])

        filename_text = image_id + image_type
        name_text = image_id
        path_text = os.path.join(folder_path, filename_text)
        output_name = os.path.join(annotation_path, image_id + '.xml')
        parse_xml(folder_text=folder_text, filename_text=filename_text, path_text=path_text, width_text=width_text,
                  height_text=height_text, name_text=name_text, xmin_text=xmin_text, ymin_text=ymin_text,
                  xmax_text=xmax_text, ymax_text=ymax_text, output_name=output_name)
