import pandas as pd
import sys
sys.path.append("..")
from exchangecleaning.DataBody import *
from exchangecleaning.Ip2Region import ip_search
from exchangecleaning.header import Header


def handle_for_digit(id_card: str) -> str or None:
    '''
    uid、银行卡号等前面可能会出现非数字
    需要把前面的非数字部分去掉
    :param id_card: uid 或者 银行卡
    :return:
    '''
    try:
        id_card = str(id_card)
        if id_card.isdigit() is True:
            # 全是数字
            return id_card
        else:
            # 存在不为数字的情况
            # 依次判断每个字符是否为数字
            # 出现数字则停止，取后面部分(包含这个数字部分),并返回
            for i in range(len(id_card)):
                if id_card[i].isdigit() is True:
                    # 发现某个字符为数字，则将其与之后面的字符全部返回
                    return id_card[i:]
            # 传入的字符串没有数字，则返回其本身
            return id_card
    except:
        return None

def judge_sex(id_card: str) -> str or None:
    '''
    根据身份证判断性别
    :param id_card: 身份证
    :return:
    '''
    id_card_str = str(id_card)
    if len(id_card_str) == 18 or len(id_card_str) == 19:
        sex_number = int(id_card_str[-2])
        if sex_number % 2 == 0:
            return "女"
        else:
            return "男"
    else:
        return "None"

def judge_bizhong(address: str) -> str or None:
    '''
    判断地址来自于哪条链上的
    :param address: 要判断的地址
    :return:
    '''
    address = str(address)
    if len(address) == 0:
        return

    if (len(address) == 42 and address[:2] == "0x") or len(address) == 40:
        # 以太坊地址
        return "yitai"
    elif (len(address) == 34 and address[0] == "T") or len(address) == 33:
        # 波场币地址
        return "bochang"
    elif address[0] == "1" and 26 <= len(address) <= 34:
        # 比特币传统地址
        return "bite chuantong"
    elif address[0] == "3" and len(address) == 34:
        # 比特币多签地址
        return "bite duoqian"
    elif address[0:3] == 'bc1' and len(address) in [42, 62]:
        # 比特币隔离见证地址
        return "bite jianzheng"
    else:
        return "qita"


class Handle_Exchange_Huobi(Header):
    # 处理火币数据的类

    def __init__(self, df_dict):
        super(Handle_Exchange_Huobi, self).__init__()
        # 对原始数据进行整合
        self.merge_original_data(df_dict)

    def __clean_register_information(self) -> pd.DataFrame:
        # 清洗用户注册信息
        def func(x):
            result = {}
            result["交易所"] = "huobi"
            result["UID"] = x["UID"]
            result["姓名"] = x["姓名"]
            result["身份证号/护照号"] = x["身份证号/护照号"]
            # 中国台湾、中国香港、中国澳门 需要统一改为中国
            result["国家"] = "中国" if "中国" in x["国家"] else x["国家"]

            id_card_address_dict = self.id_card_search(x["身份证号/护照号"])
            result["身份证归属地"] = id_card_address_dict["身份证归属地"]
            result["省(直辖市)"] = id_card_address_dict["省(直辖市)"]
            result["市"] = id_card_address_dict["市"]
            result["县"] = id_card_address_dict["县"]

            result["持仓总量"] = x["持仓总量"]
            result["手机号"] = x["手机号"]
            result["邮箱"] = x["邮箱"]
            result["注册时间"] = x["注册时间"]

            # 银行卡号、微信、支付宝 这三列原始数据可能不给
            # 需要额外进行判断
            # 银行卡号需要去掉前面可能出现的非数字
            result["银行卡号"] = handle_for_digit(x["银行卡号"]) if "银行卡号" in x.index else ""
            result["支付宝"] = x["支付宝"] if "支付宝" in x.index else ""
            result["微信"] = x["微信"] if "微信" in x.index else ""

            # 用户地址 可能不给,需要额外进行判断
            # 如果给的话需要判断 地址所属链 是否为 eth
            # 如果 地址所属链 为 eth 且 用户地址 不为 空, 则前面加上 0x
            if "用户地址" in x.index:
                # 给定了 用户地址
                if x["地址所属链"] == "eth" and x["用户地址"] != "":
                    # 判断为以太坊且地址栏不为空
                    result["用户地址"] = "0x" + x["用户地址"]
                else:
                    # 其他情况
                    result["用户地址"] = x["用户地址"]
            else:
                # 不给用户地址
                result["用户地址"] = ""

            result["地址所属链"] = x["地址所属链"]
            result["地址所属币种"] = x["地址所属币种"]

            return pd.Series(result)
        df_flog = self.original_data["register_information"].apply(func, axis=1)
        self.cleaned_data["register_information"] = df_flog

        # 其他输出表需要用到的数据单独拿出来
        df_important = df_flog[["姓名", "身份证号/护照号", "身份证归属地",
                                "UID", "手机号", "邮箱",
                                "用户地址", "地址所属链"]]


        # 对这些数据进行处理以及简单去重
        def func(x):
            if judge_bizhong(x) == "yitai":
                return small_write(x)
            else:
                return x

        df_important["用户地址"] = df_important["用户地址"].apply(func)


        df_important["用户地址"] = \
            df_important["用户地址"].apply(
                clear_no_meaning_string, args=(1,))
        df_important[[each_column for each_column in df_important.columns if
                      each_column not in ["身份证归属地", "用户地址"]]] = \
            df_important[[each_column for each_column in df_important.columns if
                          each_column not in ["身份证归属地", "用户地址"]]].applymap(
                lambda x: clear_no_meaning_string(x, handle_mode=2))

        df_important = df_important.drop_duplicates(inplace=False)
        return df_important

    def __clean_chongbi_record(self, df_important: pd.DataFrame) -> None:
        # 清洗充币记录
        if self.original_data["chongbi_record"].shape[0] > 0:
            # 保证有充币记录的数据
            # 每条充币记录去对应到个人信息
            df_flog = pd.merge(left=self.original_data["chongbi_record"],
                               right=df_important, on="UID", how="left")
            def func(x):
                result = {}
                result["交易所"] = "huobi"
                result["UID"] = x["UID"]
                result["姓名"] = x["姓名"]
                result["身份证"] = x["身份证号/护照号"]
                result["身份证归属地"] = x["身份证归属地"]

                # 个人信息一般会有多个地址, 不确定充币是充到哪个本方地址
                # 所以这里本方地址留空，如果后续找到比较好的对应方法
                # 可以填入相应的本方地址
                result["本方地址"] = ""

                # 币种为以太坊, 地址前面要加 0x
                if x["币种"] in ["eth", "ETH"] and x["来源地址/目标地址"] != "":
                    result["来源地址"] = "0x" + x["来源地址/目标地址"]
                else:
                    result["来源地址"] = x["来源地址/目标地址"]

                # 币种为以太坊, 如果哈希前面没有 0x,需要加上 0x
                if x["币种"] in ["eth", "ETH"] and x["订单号"] != "" \
                    and "0x" not in x["订单号"]:
                        result["订单号"] = "0x" + x["订单号"]
                else:
                    result["订单号"] = x["订单号"]

                result["充值方向"] = "充币"
                result["币种"] = x["币种"]
                result["时间"] = x["时间"]
                result["数量"] = x["数量"]

                return pd.Series(result)

            df_result = df_flog.apply(func, axis=1)
            self.cleaned_data["chongbi_record"] = df_result

    def __clean_tibi_record(self, df_important: pd.DataFrame) -> None:
        # 清洗提币记录
        if self.original_data["tibi_record"].shape[0] > 0:
            # 保证有提币记录的数据
            # 每条提币记录去对应到个人信息
            df_flog = pd.merge(left=self.original_data["tibi_record"],
                               right=df_important, on="UID", how="left")
            def func(x):
                result = {}
                result["交易所"] = "huobi"
                result["UID"] = x["UID"]
                result["姓名"] = x["姓名"]
                result["身份证"] = x["身份证号/护照号"]
                result["身份证归属地"] = x["身份证归属地"]

                # 币种为以太坊, 地址前面要加 0x
                if x["币种"] in ["eth", "ETH"] and x["来源地址/目标地址"] != "":
                    result["去向地址"] = "0x" + x["来源地址/目标地址"]
                else:
                    result["去向地址"] = x["来源地址/目标地址"]

                # 币种为以太坊, 如果哈希前面没有 0x,需要加上 0x
                if x["币种"] in ["eth", "ETH"] and x["订单号"] != "" \
                        and "0x" not in x["订单号"]:
                    result["订单号"] = "0x" + x["订单号"]
                else:
                    result["订单号"] = x["订单号"]

                result["充值方向"] = "提币"
                result["币种"] = x["币种"]
                result["时间"] = x["时间"]
                result["数量"] = x["数量"]

                return pd.Series(result)

            df_result = df_flog.apply(func, axis=1)
            self.cleaned_data["tibi_record"] = df_result

    def __clean_login_information(self, df_important: pd.DataFrame) -> None:
        # 清洗登录信息
        if self.original_data["login_information"].shape[0] > 0:
            # 保证有登录信息的数据
            # 每条登录信息去对应到个人信息
            df_flog = pd.merge(left=self.original_data["login_information"],
                               right=df_important, on="UID", how="left")
            def func(x):
                result = {}
                result["交易所"] = "huobi"
                result["UID"] = x["UID"]
                result["姓名"] = x["姓名"]
                result["身份证"] = x["身份证号/护照号"]
                result["身份证归属地"] = x["身份证归属地"]
                result["手机号"] = x["手机号"]
                result["登录时间"] = x["登录时间"]
                result["登录端"] = x["登录端"]
                result["IP地址"] = x["IP地址"]

                # IP地址去找对应的 国家、区域、省份、城市和 ISP
                ip2address_result = ip_search(x["IP地址"])
                result["国家"] = ip2address_result["国家"]
                result["区域"] = ip2address_result["区域"]
                result["省份"] = ip2address_result["省份"]
                result["城市"] = ip2address_result["城市"]
                result["ISP"] = ip2address_result["ISP"]

                return pd.Series(result)

            df_result = df_flog.apply(func, axis=1)
            self.cleaned_data["login_information"] = df_result

    def __clean_law_bi_trade_record(self, df_important: pd.DataFrame) -> None:
        # 清洗法币交易记录
        if self.original_data["law_bi_trade_record"].shape[0] > 0:
            # 保证有法币交易记录数据
            # 每条法币交易记录去对应到个人信息
            df_flog = pd.merge(left=self.original_data["law_bi_trade_record"],
                               right=df_important, on="UID", how="left")
            def func(x):
                result = {}
                result["交易所"] = "huobi"
                result["UID"] = x["UID"]
                result["姓名"] = x["姓名"]
                result["身份证"] = x["身份证号/护照号"]
                result["身份证归属地"] = x["身份证归属地"]
                result["订单号"] = x["订单号"]
                result["币种"] = x["币种"]
                result["数量"] = x["数量"]
                result["价格"] = x["价格"]
                result["法币"] = x["法币"]
                result["交易额"] = x["交易额"]
                result["时间"] = x["时间"]
                result["买卖方向"] = x["买卖方向"]

                return pd.Series(result)

            df_result = df_flog.apply(func, axis=1)
            self.cleaned_data["law_bi_trade_record"] = df_result

    def __clean_bi_to_bi_trade(self, df_important: pd.DataFrame) -> None:
        # 清洗币币交易记录
        if self.original_data["bi_to_bi_trade"].shape[0] > 0:
            # 保证有币币交易记录数据
            # 每条币币交易记录去对应到个人信息
            df_flog = pd.merge(left=self.original_data["bi_to_bi_trade"],
                               right=df_important, on="UID", how="left")
            def func(x):
                result = {}
                result["交易所"] = "huobi"
                result["UID"] = x["UID"]
                result["姓名"] = x["姓名"]
                result["身份证"] = x["身份证号/护照号"]
                result["身份证归属地"] = x["身份证归属地"]
                result["订单类型"] = x["订单类型"]
                result["价格"] = x["价格"]
                result["数量"] = x["数量"]
                result["交易额"] = x["交易额"]
                result["订单号"] = x["订单号"]
                result["时间"] = x["时间"]
                result["币对"] = x["币对"]
                result["买卖方向"] = x["买卖方向"]
                return pd.Series(result)

            df_result = df_flog.apply(func, axis=1)
            self.cleaned_data["bi_to_bi_trade"] = df_result

    def __summary_dizhi(self, df_important: pd.DataFrame) -> None:
        # 生成 已调证的地址汇总表
        # 包括 钱包地址调证人员信息整理 和 已调证钱包地址汇总表
        # 已调证地址对所有用户进行统计
        df_flog = df_important[df_important["用户地址"] != ""]  # 获取有地址的数据

        # 获取在txt文本里的地址但是没有在调证文件里的地址，将其作为无效地址
        invalid_address = set(self.original_data["txt"]["dizhi"]) - \
                          set(self.original_data["txt"]["dizhi"]).intersection(set(df_flog["用户地址"]))
        self.cleaned_data["invalid"]["dizhi"] = list(invalid_address)

        if df_flog.shape[0] > 0:
            def func(x):
                result = {}
                result["交易哈希"] = ""
                result["区块高度"] = ""
                result["钱包地址"] = x["用户地址"]

                # 这一部分加上上面的 钱包地址 作为汇总表
                result["UID"] = x["UID"]
                result["姓名"] = x["姓名"]
                result["身份证"] = x["身份证号/护照号"]
                result["身份证归属地"] = x["身份证归属地"]
                result["交易所"] = "huobi"
                result["手机"] = x["手机号"]
                result["邮箱"] = x["邮箱"]

                person_information = "核实-火币-" + x["姓名"] + \
                                     "-" + judge_sex(x["身份证号/护照号"]) + \
                                     "-" + x["身份证号/护照号"] + \
                                     "-" + x["手机号"] + \
                                     "-" + x["身份证归属地"]
                result["本方标签"] = person_information

                result["交易时间"] = ""
                result["交易金额"] = ""
                result["交易余额"] = ""
                result["交易方向"] = ""
                result["对方交易钱包"] = ""
                result["对手标签"] = ""
                result["币种"] = ""

                # print("这是一个用户地址:", x["用户地址"])
                if judge_bizhong(x["用户地址"]) == "yitai":
                    result["type"] = "eth"
                elif judge_bizhong(x["用户地址"]) == "bochang":
                    result["type"] = "tron"
                elif "bite" in judge_bizhong(x["用户地址"]):
                    result["type"] = "bite"
                else:
                    result["type"] = "other"

                return pd.Series(result)

            result_all = df_flog.reset_index(drop=True).apply(func, axis=1)  # 生成要上图的表格以及汇总表

            df_grouped = result_all.groupby("type")
            for each_result in df_grouped:
                each_df = each_result[1]
                # 上图的文件
                picture_df = each_df[["交易哈希", "区块高度", "钱包地址", "本方标签",
                                      "交易时间", "交易金额", "交易余额", "交易方向",
                                      "对方交易钱包", "对手标签", "币种"]]
                # 汇总的文件
                summary_df = each_df[["钱包地址", "UID", "姓名", "身份证",
                                      "身份证归属地", "交易所", "手机", "邮箱"]]
                if each_result[0] == "eth":
                    self.cleaned_data["picture"]["dizhi"]["eth"] = picture_df
                    self.cleaned_data["summary"]["dizhi"]["eth"] = summary_df
                elif each_result[0] == "tron":
                    self.cleaned_data["picture"]["dizhi"]["tron"] = picture_df
                    self.cleaned_data["summary"]["dizhi"]["tron"] = summary_df
                elif each_result[0] == "bite":
                    self.cleaned_data["picture"]["dizhi"]["bite"] = picture_df
                    self.cleaned_data["summary"]["dizhi"]["bite"] = summary_df

    def __summary_haxi(self) -> None:
        # 生成 已调证的哈希汇总表
        # 包括 交易哈希调证人员信息整理 和已调证哈希汇总表
        # 已调证哈希只对txt文档中已有的哈希进行统计
        if len(self.original_data["txt"]["haxi"]) > 0 and \
                len(self.cleaned_data["tibi_record"].shape[0]) > 0:
            # 获取在txt文本里的哈希但是没有在调证文件里的哈希，将其作为无效哈希
            invalid_haxi = set(self.original_data["txt"]["haxi"]) - \
                           set(self.original_data["txt"]["haxi"]).intersection(set(self.cleaned_data["tibi_record"]["订单号"]))
            self.cleaned_data["invalid"]["haxi"] = list(invalid_haxi)

            # 提币的哈希且存在于txt的哈希作为 已调证的哈希
            mask = self.cleaned_data["tibi_record"]["订单号"].isin(self.original_data["txt"]["dizhi"])
            df_flog = self.cleaned_data["tibi_record"][mask]
            # 筛去哈希为空的数据
            df_flog = df_flog[df_flog["订单号"] != ""]
            if df_flog.shape[0] > 0:
                def func(x):
                    result = {}
                    result["交易哈希"] = x["订单号"]
                    result["区块高度"] = ""

                    # 这里作为汇总表的字段
                    result["UID"] = x["UID"]
                    result["姓名"] = x["姓名"]
                    result["身份证"] = x["身份证号/护照号"]
                    result["身份证归属地"] = x["身份证归属地"]
                    result["交易所"] = "huobi"
                    # 这里无法用 哈希 或者 UID 对应到具体的用户注册信息中的地址
                    # 无奈留空
                    result["交易所用户地址"] = ""
                    result["手机"] = x["手机号"]
                    result["邮箱"] = x["邮箱"]

                    # 这里将 去向地址 作为 钱包地址
                    result["钱包地址"] = x["去向地址"]

                    person_information = "付款人-火币-" + x["姓名"] + \
                                         "-" + judge_sex(x["身份证号/护照号"]) + \
                                         "-" + x["身份证号/护照号"] + \
                                         "-" + x["手机号"] + \
                                         "-" + x["身份证归属地"]
                    result["本方标签"] = person_information

                    result["交易时间"] = ""
                    result["交易金额"] = ""
                    result["交易余额"] = ""
                    result["交易方向"] = ""
                    result["对方交易钱包"] = ""
                    result["对手标签"] = ""
                    result["币种"] = ""

                    if judge_bizhong(x["去向地址"]) == "yitai":
                        result["type"] = "eth"
                    elif judge_bizhong(x["去向地址"]) == "bochang":
                        result["type"] = "tron"
                    elif "bite" in judge_bizhong(x["去向地址"]):
                        result["type"] = "bite"
                    else:
                        result["type"] = "other"

                    return pd.Series(result)
                result_all = df_flog.apply(func, axis=1)  # 生成要上图的表格以及汇总表

                df_grouped = result_all.group_by("type")
                for each_result in df_grouped:
                    each_df = each_result[1]
                    # 上图的文件
                    picture_df = each_df[["交易哈希", "区块高度", "钱包地址", "本方标签",
                                          "交易时间", "交易金额", "交易余额", "交易方向",
                                          "对方交易钱包", "对手标签", "币种"]]
                    # 汇总的文件
                    summary_df = each_df[["UID", "姓名", "身份证", "身份证归属地",
                                          "交易所", "交易所用户地址", "手机", "邮箱"]]
                    if each_result[0] == "eth":
                        self.cleaned_data["picture"]["haxi"]["eth"] = picture_df
                        self.cleaned_data["summary"]["haxi"]["eth"] = summary_df
                    elif each_result[0] == "tron":
                        self.cleaned_data["picture"]["haxi"]["tron"] = picture_df
                        self.cleaned_data["summary"]["haxi"]["tron"] = summary_df
                    elif each_result[0] == "bite":
                        self.cleaned_data["picture"]["haxi"]["bite"] = picture_df
                        self.cleaned_data["summary"]["haxi"]["bite"] = summary_df

    def clean(self):
        # 清洗原始数据
        print("处理用户注册信息")
        df_important = self.__clean_register_information()
        print("处理充币记录")
        self.__clean_chongbi_record(df_important)
        print("处理提币记录")
        self.__clean_tibi_record(df_important)
        print("处理登录信息")
        self.__clean_login_information(df_important)
        print("处理法币交易记录")
        self.__clean_law_bi_trade_record(df_important)
        print("处理币币交易记录")
        self.__clean_bi_to_bi_trade(df_important)
        print("处理地址调证信息")
        self.__summary_dizhi(df_important)
        print("处理哈希调证信息")
        self.__summary_haxi()


def get_cleaned_data(df_dict: pd.DataFrame) -> pd.DataFrame:
    '''
    传入多个 df 的字典，键为指定的 df 的类型，值为对应的 df 或多个 df 组成的列表
    返回转化为清洗结果的多个 df 组成的字典(半成品)
    '''
    handle_object = Handle_Exchange_Huobi(df_dict)
    handle_object.clean()


    return handle_object.cleaned_data




if __name__ == "__main__":
    handle_object = Preprocessing.Preprocessing_Handle()
    root = r"数据集\币安/"
    result = handle_object.read_for_standardized(root + "Report_广西贵港公安局_260422_01.xlsx")
    df_dict = {
    "register_information": pd.DataFrame(),
    "chongbi_record": pd.DataFrame(),
    "tibi_record": pd.DataFrame(),
    "login_information": pd.DataFrame(),
    "law_bi_trade_record": pd.DataFrame(),
    "bi_to_bi_trade": pd.DataFrame()}


    for key, value in result.items():
        if "Customer" in key:
            df_dict["register_information"] = value



