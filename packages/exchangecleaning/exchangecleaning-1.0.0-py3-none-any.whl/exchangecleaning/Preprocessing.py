import os
import pandas as pd
import openpyxl
import xlrd
import warnings
from xlsx2csv import Xlsx2csv

warnings.filterwarnings("ignore")

def xlsx2csv(xlsx_address: str, csv_address: str) -> None:
    # 把excel文件转化为csv文件
    xlsxfile = xlsx_address
    csvpath = csv_address
    Xlsx2csv(xlsxfile, outputencoding="utf-8", floatformat=str).convert(csvpath, sheetid=0)

def bianli(rootDir: str) -> list:
    address_all = []
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            if file != "__MACOS" and file != "__MACOS":
                address_all.append(os.path.join(root, file))
                for dir in dirs:
                    bianli(dir)
    return address_all

class Preprocessing_Handle():
    # 文件读取的预处理类

    def __init__(self):
        pass

    def preprocessing_handle(self, df: pd.DataFrame) -> pd.DataFrame:
        # 对传入的 df 处理
        # 包含
        # 1.字段两边去空格(仅仅指 字段值为 str的情况，字段值为数值型则不处理)
        # 2.空值使用pd.NA代替
        # 3.所有数据两边去空格
        # 4.去除空行

        # step 1
        columns_new = [x.strip() if isinstance(x, str) else x for x in df.columns]
        df.columns = columns_new

        # step 2(one part)
        df = df.fillna("")

        # step 3
        def func(x):
            try:
                x = str(x).strip()
            except:
                x = ""
            return x
        df = df.applymap(func)

        # step 2(other part)
        # def func(x):
        #     if x == "":
        #         result = pd.NA
        #     else:
        #         result = x
        #     return result
        # df = df.applymap(func)

        # step 4
        df = df.dropna(axis=0, how="all")

        return df

    def read_for_standardized(self, filename: str) -> dict or pd.DataFrame:
        # 对能直接用 pandas 读取的文件读取和处理
        # 处理包含
        # 1.读取
        # 2.字段两边去空格
        # 3.空值使用空字符串代替
        # 4.所有数据a两边去空格
        # 5.去除空行
        # 是 csv 文件则返回处理完的 df
        # 是 excel文件(xlsx或xls)则返回一个字典，键是表名，值是对应的 df
        # 否则返回 空 df
        if ".csv" in os.path.split(filename)[1]:
            # 是 csv 文件
            df = pd.read_csv(filename, dtype=str)
            df = self.preprocessing_handle(df)
            return df
        elif ".xls" in os.path.split(filename)[1] \
            or ".xlsx" in os.path.split(filename)[1]:
            xl = pd.ExcelFile(filename)
            sheet_names = xl.sheet_names
            result_dict = {}
            for sheet_name in sheet_names:
                df = xl.parse(sheet_name, dtype=str)
                df = self.preprocessing_handle(df)
                result_dict[sheet_name] = df
            return result_dict
        else:
            return pd.DataFrame()

    def read_for_unstandardized(self, filename):
        # 对不能直接用 pandas 读取的文件进行处理
        pass

    def read_excel_for_big_data(self, filename: str, backup_address: str) -> tuple:
        # 读取文件较大的excel文件
        # 将其转为 csv 文件后进行读取,
        # 如果转化失败，则进行正常读取
        if ".xlsx" in os.path.split(filename)[1]:
            # 删除备份文件夹下可能存在的文件
            print("正在读取", filename, "...")
            filelist = bianli(backup_address)
            if len(filelist) > 0:
                for each_filename in filelist:
                    os.remove(each_filename)

            try:
                xlsx2csv(filename, backup_address)
                file_list = bianli(backup_address)
                result_dict = {}
                for file in file_list:
                    df = self.read_for_standardized(file)
                    key = os.path.split(file)[1].split(".")[0]
                    result_dict[key] = df

                print(filename, "读取完成")
                # 获取到数据后删除备份文件夹下的文件
                filelist = bianli(backup_address)
                if len(filelist) > 0:
                    for each_filename in filelist:
                        os.remove(each_filename)

                return result_dict, "success"

            except:
                # 转化失败
                result_dict = self.read_for_standardized(filename)
                return result_dict, "fail"

if __name__ == "__main__":
    handle_object = Preprocessing_Handle()
    root = r"C:\Users\13868471663\Desktop\数据清洗\数据集\火币\1202\1/"
    backup_address = r"C:\Users\13868471663\Desktop\数据清洗\backup/"
    result, flog = handle_object.read_excel_for_big_data(root + "514_1.xlsx", backup_address)
    print(flog)
    for key, value in result.items():
        print(key, value.shape)
