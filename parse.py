import json
import base64
import os


def _find_merge(merge_map, cells, cell):
    for merge in merge_map:
        if cell in merge:
            for c in merge:
                if c == cell:
                    continue
                if c in cells:
                    return cells[c]['value'].replace("\n", "")
                
    return " "

# build map for "merge", then go through the cells, if no related element, search from the "merge" map then duplicate the cell...
def table_handle(item):
    print("handle table")
    merge_map = []
    # build "merge" map if "merge" existed
    if item["merged"]:
        for merge in item["merged"]:
            merged_cells = []
            for cell in merge:
                merged_cells.append(str(cell[0]) + "_" + str(cell[1]))
            merge_map.append(merged_cells)

    print("merge map:")
    print(merge_map)

    row_num = 0
    column_num = 0
    for cell_key in item['cells']:
        row = cell_key.split("_")[0]
        column = cell_key.split("_")[1]
        if int(row) > row_num:
            row_num = int(row)
        if int(column) > column_num:
            column_num = int(column)

    row_num += 1
    column_num += 1
    des = "这是一个" + str(row_num) + "行" + str(column_num) + "列的表格,第一行或者前几行是表头，请自行判断\n表格的名字是：" + item['title'] + "\n"
    for r in range(row_num):
        row_des = "第" + str(r) + "行的内容是："
        for c in range(column_num):
            cell_key = str(r) + "_" + str(c)
            print(item['cells'])
            if cell_key in item['cells']:
                row_des += item['cells'][cell_key]['value'].replace("\n", "") + " "
            else:
                if len(merge_map) != 0:
                    row_des += _find_merge(merge_map, item['cells'], cell_key) + " "

        des += row_des + "\n"
    return des

def paragraph_handle(item):
    print("handle paragraph")
    return item['text'] + "\n"

def image_handle(item, pre_res):
    print("handle paragraph")
    data = item['data']
    imgdata = base64.b64decode(data)
    filename = str(item['page']) + "-" + str(item['index']) + '.jpg'
    filepath = os.path.join("./generated", filename)
    with open(filepath, 'wb') as f:
        f.write(imgdata)

    des = ""
    # if item['title']:
    #     des = item['title']
    # else:
    des = pre_res.replace("\n", "")

    return "此处有图片，图片的名字是：" + des + ", 图片的地址是：http://127.0.0.1:3003/" + str(item['page']) + "-" + str(item['index']) + '.jpg \n'

# Opening JSON file
f = open('res.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
f.close()
# Iterating through the json
# list
txt = ""
for page in data['pdf_elements']:
    pre_res = ""
    for item in page['elements']:
        res = ""
        if item["element_type"] == "paragraphs":
            res = paragraph_handle(item)
        elif item["element_type"] == "images":
            res = image_handle(item, pre_res)

        elif item["element_type"] == "tables":
            res = table_handle(item)

        if item["element_type"] == "paragraphs":
            pre_res = res
        else:
            pre_res = ""
    
        txt += res

txt_path = os.path.join("./generated", "plain.txt")
with open(txt_path, "w") as code:
    code.write(txt)