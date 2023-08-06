from transform import transform_all
import huobi.handle_huobi as handle_huobi
from DataBody import DataBody

def clean(file_dict, backup_address, output_address):
    '''
    开放给外部使用的函数
    :param file_dict: 要清洗的文件路径字典，键为 交易所名称, 值为该交易所对应文件的路径
            例子: file_dict = {"huobi": "数据集/火币/",
                              "bi_an": "数据集/币安/"}
    :param backup_address: 备份文件路径,
                         面对较大excel文件时(仅指火币文件,别的交易所文件转化时可能会出问题),
                         需要将excel文件转化为 csv 文件再进行读取, 以提高程序运行效率
                         该路径指的是转为 csv 文件时需要临时存放的路径(读取后会将csv文件删除)
            注：程序内有删除操作，该路径下请确保没有其他文件
    :param output_address: 要输出的文件时存放的路径
            注：该路径下最好没有其他文件
    :return:
    '''

    # 读取原始数据
    original_data = transform_all(file_dict, backup_address)
    # 将原始数据整理成要输出的文件的格式
    print("正在生成清洗结果")
    df_dict = handle_huobi.get_cleaned_data(original_data["huobi"])
    # 将整理好的数据放入 databody 中，对内部数值进行处理以及输出
    databody = DataBody()
    databody.append_df_dict(df_dict)
    print("正在输出清洗结果..")
    databody.output_data(output_address, "order")
    print("运行结束")



if __name__ == "__main__":
    # 火币原始文件路径
    huobi_root = r"C:\Users\13868471663\Desktop\数据清洗\数据集\火币/"
    # 备份文件路径
    backup_address = r"C:\Users\13868471663\Desktop\数据清洗\backup/"
    # 输出文件路径
    output_address = r"D:\pywork\101.成功软件\数据清洗linux版本模块化\测试输出/"

    file_dict = {"huobi": huobi_root}
    clean(file_dict, backup_address, output_address)
