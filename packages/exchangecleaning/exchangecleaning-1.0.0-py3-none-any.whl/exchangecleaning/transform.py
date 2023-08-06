import os
import pandas as pd
from Preprocessing import Preprocessing_Handle
from huobi.transform_huobi import transform_huobi
#
# def get_txt_information(filefold: list) -> tuple:
#     '''
#     获取txt文件中的内容
#     :param filefold:
#     :return:
#     '''
#     haxi_txt = []
#     dizhi_txt = []
#     codelist = ["utf-8", "gbk", "gb2312"]
#     for filename in filefold:
#         if filename[-3:] == "txt":
#             for code in codelist:
#                 try:
#                     with open(filename, encoding=code) as f:
#                         flog = 0
#                         for i in f:
#                             if i[:-1] == "钱包地址":
#                                 flog = 1
#                             elif i[:-1] == "交易哈希":
#                                 flog = 2
#                             break
#                         for i in f:
#                             if flog == 1:
#                                 dizhi_txt.append(i[:-1])
#                             elif flog == 2:
#                                 haxi_txt.append(i[:-1])
#                     break
#                 except:
#                     continue
#     return haxi_txt, dizhi_txt
#
# def bianli(rootDir: str) -> list:
#     address_all = []
#     for root, dirs, files in os.walk(rootDir):
#         for file in files:
#             if file != "__MACOS" and file != "__MACOS":
#                 address_all.append(os.path.join(root, file))
#                 for dir in dirs:
#                     bianli(dir)
#     return address_all
#
#
# def transform_bi_an(filefold: str) -> dict:
#     '''
#     将火币的原始数据组合成要输出的文件的格式
#     :param filefold: 文件的路径
#     :return:
#     '''
#     pass

def transform_all(file_dict: dict, backup_address: str) -> dict:
    '''
    对指定路径中的文件进行读取
    :param file_dict: 文件路径所在的字典
    :param backup_address:
    :return:
    '''
    result = {}
    for key, value in file_dict.items():
        if key == "huobi":
            result["huobi"] = transform_huobi(value, backup_address)
        elif key == "bi_an":
            result["bi_an"] = transform_bi_an(value)
    return result


if __name__ == "__main__":
    # 放入一个字典, 键为 交易所,
    # 值为一个路径，这个路径下的所有文件均为该交易所的调证数据以及txt文件
    # 返回一个 文件内部数据的字典，可以直接去 handle
    backup_address = r"C:\Users\13868471663\Desktop\数据清洗\backup/"
    huobi_address = r"C:\Users\13868471663\Desktop\数据清洗\数据集\火币\1202/"
    file_dict = {"huobi": huobi_address}
    print(transform_all(file_dict, backup_address))
