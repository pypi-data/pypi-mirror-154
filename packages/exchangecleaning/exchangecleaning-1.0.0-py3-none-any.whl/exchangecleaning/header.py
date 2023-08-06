import pandas as pd
import re

class Header():
    # 所有交易所处理类的基类

    def __init__(self):
        # 初始数据集
        self.original_data = {
            "register_information": pd.DataFrame(),
            "chongbi_record": pd.DataFrame(),
            "tibi_record": pd.DataFrame(),
            "login_information": pd.DataFrame(),
            "law_bi_trade_record": pd.DataFrame(),
            "bi_to_bi_trade": pd.DataFrame(),
            "txt": {"dizhi": [],
                    "haxi": []}
        }

        # 清洗后的数据集
        self.cleaned_data = {
            "register_information": pd.DataFrame(),
            "chongbi_record": pd.DataFrame(),
            "tibi_record": pd.DataFrame(),
            "login_information": pd.DataFrame(),
            "law_bi_trade_record": pd.DataFrame(),
            "bi_to_bi_trade": pd.DataFrame(),
            "picture":
                {"dizhi": {"eth": pd.DataFrame(),
                           "tron": pd.DataFrame(),
                           "bite": pd.DataFrame()},
                 "haxi": {"eth": pd.DataFrame(),
                          "tron": pd.DataFrame(),
                          "bite": pd.DataFrame()}
                 },
            "summary":
                {"dizhi":{"eth": pd.DataFrame(),
                          "tron": pd.DataFrame(),
                          "bite": pd.DataFrame()},
                 "haxi": {"eth": pd.DataFrame(),
                          "tron": pd.DataFrame(),
                          "bite": pd.DataFrame()}
                },
            # 记录无效的地址和哈希
            "invalid": {"dizhi": [],
                        "haxi": []}
        }
        # 身份证号对应行政区划数据
        self.df_idcard2address = pd.read_excel(
            "config_data/身份证号对应行政区划表.xlsx", dtype=str, sheet_name="Sheet1")
        self.df_idcard2address = self.df_idcard2address.fillna("")
        self.get_idcard2city()
        self.get_idcard2province()

    def get_idcard2city(self) -> None:
        # 具体到市的身份证对应
        df_flog = self.df_idcard2address[["身份证号代码", "省(直辖市)", "市"]]
        df_flog["身份证号代码"] = df_flog["身份证号代码"].apply(lambda x: x[:4])
        df_flog = df_flog.drop_duplicates(inplace=False)
        self.df_idcard2city = df_flog

    def get_idcard2province(self) -> None:
        # 具体到省的身份证对应
        df_flog = self.df_idcard2address[["身份证号代码", "省(直辖市)"]]
        df_flog["身份证号代码"] = df_flog["身份证号代码"].apply(lambda x: x[:2])
        df_flog = df_flog.drop_duplicates(inplace=False)
        self.df_idcard2province = df_flog

    def id_card_search(self, id_card: str) -> dict:
            # 输入一个身份证号，返回对应的行政区划
            # 省市县匹配不到就去匹配省市
            # 省市匹配不到就去匹配省
            # 再匹配不到就设为空
            IDCards_pattern = r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$'

            try:
                person_id_card_real = re.findall(IDCards_pattern, id_card, flags=0)[0][0]
            except:
                person_id_card_real = None

            result_dict = {
                "身份证归属地": "",
                "省(直辖市)": "",
                "市": "",
                "县": ""
            }
            if person_id_card_real is not None:
                result_list = self.df_idcard2address[
                    self.df_idcard2address["身份证号代码"] == person_id_card_real[:6]].values.tolist()
                if len(result_list) > 0:
                    # 保证能匹配到身份证归属地
                    each_result = result_list[0]
                    result_dict["身份证归属地"] = each_result[1]
                    result_dict["省(直辖市)"] = each_result[2]
                    result_dict["市"] = each_result[3]
                    result_dict["县"] = each_result[4]
                else:
                    # 匹配不到县，去匹配市
                    result_list = self.df_idcard2city[
                        self.df_idcard2city["身份证号代码"] == person_id_card_real[:4]].values.tolist()
                    if len(result_list) > 0:
                        each_result = result_list[0]
                        result_dict["身份证归属地"] = each_result[1] + each_result[2]
                        result_dict["省(直辖市)"] = each_result[1]
                        result_dict["市"] = each_result[2]
                        result_dict["县"] = ""
                    else:
                        # 匹配不到市，去匹配省
                        result_list = self.df_idcard2province[
                            self.df_idcard2province["身份证号代码"] == person_id_card_real[:2]].values.tolist()
                        if len(result_list) > 0:
                            each_result = result_list[0]
                            result_dict["身份证归属地"] = each_result[1]
                            result_dict["省(直辖市)"] = each_result[1]
                            result_dict["市"] = ""
                            result_dict["县"] = ""
            return result_dict

    def merge_original_data(self, df_dict):
        # 对初始数据进行整理
        for key, value in df_dict.items():
            if key == "txt":
                self.original_data["txt"] = value
            else:
                df_flog = pd.DataFrame()
                if len(value) > 0:
                    for each_value in value:
                        if each_value.shape[0] > 0:
                            # 保证 df 里有数据
                            df_flog = pd.concat([df_flog, each_value], ignore_index=True)
                self.original_data[key] = df_flog
