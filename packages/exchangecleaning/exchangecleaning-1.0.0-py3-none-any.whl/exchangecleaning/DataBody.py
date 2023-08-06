import datetime
import pandas as pd
from multiprocessing import Pool


def clear_no_meaning_string(string: str, handle_mode: int) -> str or None:
    '''
    去除文本中的无意义字符

    方式 1： 值本身就是无意义字符，返回 None
    方式 2:  去除值内部的无意义字符
    :param string: 要去除无意义字符的字符串
    :param handle_mode: 去除方式 取值 1 or 2
    :return:
    '''
    string = str(string)

    if handle_mode == 1:
        if string in ["None", "none", "nan", "null", "Null",
                      "无", "無", "N/A", "n/a", "未知"] or \
                type(string) is float:
            return None
        else:
            return string
    elif handle_mode == 2:
        if type(string) is not float:
            string = string.replace("None", "")
            string = string.replace("none", "")
            string = string.replace("nan", "")
            string = string.replace("Null", "")
            string = string.replace("null", "")
            string = string.replace("N/A", "")
            string = string.replace("n/a", "")
            # string = string.replace("无", "")
            string = string.replace("無", "")
            return string
        else:
            return None


def str_to_float(num: str) -> float or None:
    '''
    字符型数据转数字型
    :param num: 要转化的字符串
    :return:
    '''
    try:
        num = float(num)
        return num
    except:
        return None


def handle_for_time(timeString: str) -> str or None:
    '''
    时间格式统一
    :param timeString: 要统一的时间的字符串
    :return:
    '''
    # 预先设定可能出现的表示时间的格式
    time_all_geshi = ["%Y-%m-%d %H:%M:%S",        # 2018-01-10 15:50:55
                      "%Y/%m/%d %H:%M:%S",        # 2018/01/10 15:50:55
                      "%a %b %d %H:%M:%S %Z %Y",  # Tue Jul 06 04:51:08 UTC 2021
                      "%Y/%m/%d %H:%M",           # 2018/12/20 12:48
                      "%Y/%m/%d %H:%M:%S"         # 2018/12/20 12:48:28
                      ]

    if timeString is None or type(timeString) is float or timeString == "":
        return None

    for time_geshi in time_all_geshi:
        try:
            timestamp = datetime.datetime.strptime(timeString, time_geshi)

            if time_geshi == "%a %b %d %H:%M:%S %Z %Y":
                # 如果原始数据是标准时，则再加上8个小时
                timestamp = timestamp + datetime.timedelta(hours=8)

            break
        except:
            # 如果格式对不上，则对下一个格式
            continue
    try:
        return timestamp
    except:
        print(type(timeString))
        print("timeString=" + timeString + "没有匹配上")


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


def small_write(s: str or None) -> str or None:
    '''
    字符串转小写
    :param s: 要转的字符串
    :return:
    '''
    if s is None:
        return s
    else:
        return str(s).lower()


def big_write(s: str or None) -> str or None:
    '''
    字符串大写
    :param s: 要转的字符串
    :return:
    '''
    if s is None:
        return s
    else:
        return str(s).upper()


class Header():
    # 定义一些共用的属性

    def __init__(self):
        # 变量名对应的表头
        self.varname_to_header = {
            "bi_to_bi_trade": ["交易所", "UID", "姓名", "身份证", "身份证归属地",
                                 "订单类型",
                                 "价格", "数量", "交易额", "订单号", "时间",
                                 "币对", "买卖方向"],
            "chong_bi_record": ["交易所", "UID", "姓名", "身份证", "身份证归属地",
                                "本方地址", "来源地址", "订单号", "充值方向",
                                "币种", "时间", "数量"],
            "ti_bi_record": ["交易所", "UID", "姓名", "身份证", "身份证归属地",
                             "去向地址", "订单号", "充值方向",
                             "币种", "时间", "数量"],
            "login_information": ["交易所", "UID", "姓名", "身份证", "身份证归属地",
                                  "手机号", "登录时间", "登录端", "IP地址",
                                  "国家", "区域", "省份", "城市", "ISP"],
            "law_bi_trade_record": ["交易所", "UID", "姓名", "身份证", "身份证归属地",
                                     "订单号", "币种", "数量", "价格",
                                     "法币", "交易额", "时间", "买卖方向"],
            "haxi_diaozheng": ["交易哈希", "区块高度", "钱包地址", "本方标签",
                               "交易时间", "交易金额", "交易余额", "交易方向",
                               "对方交易钱包", "对手标签", "币种"],
            "haxi_diaozheng_information_yitai_all":
                ["交易哈希", "区块高度", "钱包地址", "本方标签",
                 "交易时间", "交易金额", "交易余额", "交易方向",
                 "对方交易钱包", "对手标签", "币种"],
            "haxi_diaozheng_information_bochang_all":
                ["交易哈希", "区块高度", "钱包地址", "本方标签",
                 "交易时间", "交易金额", "交易余额", "交易方向",
                 "对方交易钱包", "对手标签", "币种"],
            "haxi_diaozheng_information_bite_all":
                ["交易哈希", "区块高度", "钱包地址", "本方标签",
                 "交易时间", "交易金额", "交易余额", "交易方向",
                 "对方交易钱包", "对手标签", "币种"],
            "haxi_huizong": ["交易哈希", "UID", "姓名", "身份证", "身份证归属地",
                             "交易所", "交易所用户地址", "手机", "邮箱"],
            "haxi_huizong_yitai_all":
                ["交易哈希", "UID", "姓名", "身份证", "身份证归属地",
                 "交易所", "交易所用户地址", "手机", "邮箱"],
            "haxi_huizong_bochang_all":
                ["交易哈希", "UID", "姓名", "身份证", "身份证归属地",
                 "交易所", "交易所用户地址", "手机", "邮箱"],
            "haxi_huizong_bite_all":
                ["交易哈希", "UID", "姓名", "身份证", "身份证归属地",
                 "交易所", "交易所用户地址", "手机", "邮箱"],
            "dizhi_diaozheng": ["交易哈希", "区块高度", "钱包地址", "本方标签",
                                "交易时间", "交易金额", "交易余额", "交易方向",
                                "对方交易钱包", "对手标签", "币种"],
            "dizhi_diaozheng_information_yitai_all":
                ["交易哈希", "区块高度", "钱包地址", "本方标签",
                 "交易时间", "交易金额", "交易余额", "交易方向",
                 "对方交易钱包", "对手标签", "币种"],
            "dizhi_diaozheng_information_bochang_all":
                ["交易哈希", "区块高度", "钱包地址", "本方标签",
                 "交易时间", "交易金额", "交易余额", "交易方向",
                 "对方交易钱包", "对手标签", "币种"],
            "dizhi_diaozheng_information_bite_all":
                ["交易哈希", "区块高度", "钱包地址", "本方标签",
                 "交易时间", "交易金额", "交易余额", "交易方向",
                 "对方交易钱包", "对手标签", "币种"],
            "dizhi_huizong": ["钱包地址", "UID", "姓名", "身份证", "身份证归属地",
                              "交易所", "手机", "邮箱"],
            "dizhi_huizong_yitai_all":
                ["钱包地址", "UID", "姓名", "身份证", "身份证归属地",
                 "交易所", "手机", "邮箱"],
            "dizhi_huizong_bochang_all":
                ["钱包地址", "UID", "姓名", "身份证", "身份证归属地",
                 "交易所", "手机", "邮箱"],
            "dizhi_huizong_bite_all":
                ["钱包地址", "UID", "姓名", "身份证", "身份证归属地",
                 "交易所", "手机", "邮箱"],
            "register_information": ["交易所", "UID", "姓名", "身份证号/护照号", "国家",
                                     "身份证归属地", "省(直辖市)", "市", "县",
                                     "持仓总量", "手机号", "邮箱", "注册时间", "银行卡号",
                                     "支付宝", "微信", "用户地址", "地址所属链", "地址所属币种"],
            "shenfen_information": ["姓名", "身份证号/护照号", "身份证归属地",
                                    "前科标签", "毒品种类", "抓获时间", "出所时间",
                                    "管控情况", "案件详情"],
            "approved_devices": ["姓名", "UID", "身份证号/护照号", "身份证归属地",
                                 "设备名称", "客户端", "ip地址",
                                 "定位", "最近使用时间(标准时)",
                                 "状态", "key", "value"]}

        # 变量名对应的文件名及文件类型(excel或csv)
        self.varname_to_filename_and_filekind = {
            "bi_to_bi_trade": ["sm币币交易记录", ".xlsx"],
            "chong_bi_record": ["sm充币记录", ".xlsx"],
            "ti_bi_record": ["sm提币记录", ".xlsx"],
            "login_information": ["sm登录信息", ".xlsx"],
            "law_bi_trade_record": ["sm法币交易记录", ".xlsx"],
            "haxi_diaozheng_information_yitai_all":
                ["sm交易哈希调证人员信息整理-以太坊", ".csv"],
            "haxi_diaozheng_information_bochang_all":
                ["sm交易哈希调证人员信息整理-波场币", ".csv"],
            "haxi_diaozheng_information_bite_all":
                ["sm交易哈希调证人员信息整理-比特币", ".csv"],
            "haxi_huizong_yitai_all":
                ["sm已调证哈希汇总表-以太坊", ".xlsx"],
            "haxi_huizong_bochang_all":
                ["sm已调证哈希汇总表-波场币", ".xlsx"],
            "haxi_huizong_bite_all":
                ["sm已调证哈希汇总表-比特币", ".xlsx"],
            "dizhi_diaozheng_information_yitai_all":
                ["sm钱包地址调证人员信息整理-以太坊", ".csv"],
            "dizhi_diaozheng_information_bochang_all":
                ["sm钱包地址调证人员信息整理-波场币", ".csv"],
            "dizhi_diaozheng_information_bite_all":
                ["sm钱包地址调证人员信息整理-比特币", ".csv"],
            "dizhi_huizong_yitai_all":
                ["sm已调证钱包地址汇总表-以太坊", ".xlsx"],
            "dizhi_huizong_bochang_all":
                ["sm已调证钱包地址汇总表-波场币", ".xlsx"],
            "dizhi_huizong_bite_all":
                ["sm已调证钱包地址汇总表-比特币", ".xlsx"],
            "register_information": ["sm用户注册信息", ".xlsx"],
            "shenfen_information": ["sm身份信息表", ".xlsx"],
            "approved_devices": ["sm用户设备表(币安)", ".xlsx"]}

        # 不同数据的变量名对应的表头
        self.different_varname_to_header = {
            # 火币otc交易记录
            "huobi_otc_trade_record":
                ["订单号", "对手方UID", "币种", "数量", "价格",
                 "法币", "交易额", "时间", "UID", "买卖方向"],
            # 币安流动资产和钱包表
            "bi_an_current_assets_and_wallets":
                ["Name", "User ID", "Asset Ticker",
                 "Asset Name", "Total Position", "Estimated BTC Value",
                 "Deposit Wallet Address", "Label/Tag/Memo"],
            # 币安 登录信息表
            "bi_an_access_logs":
                ["User ID", "Operation", "Client", "Client Version",
                 "Real IP", "Geolocation", "Browser",
                 "Timestamp (UTC)"],
            # okex用户余额表
            "okex_user_yu_e":
                ["uuid", "姓名", "currency_symbol",
                 "total_balance", "pt"],
            # okex 统一账户表
            "okex_tongyi_zhanghu":
                ["uuid", "姓名", "时间", "业务线",
                 "产品名称", "类型", "数量", "单位",
                 "收益", "手续费",
                 "仓位余额变动", "仓位余额",
                 "交易账户余额变动", "交易账户余额",
                 "币种名称", "成交价", "trade_side"],
            # okex用户设备信息表
            "okex_user_device_information":
                ["uuid", "姓名", "设备制造商", "设备型号",
                 "操作系统", "操作系统版本",
                 "屏幕高度", "屏幕宽度",
                 "运营商名称", "网络类型",
                 "设备id", "mac地址",
                 "设备imei号", "wifi信息",
                 "是否越狱", "是否模拟器",
                 "是否为debug", "是否双开"],
            # okex 交割账单币本位表
            "okex_jiaoge_bill":
                ["uuid", "姓名", "合约周期id",
                 "币种", "类型", "仓位数量",
                 "收益", "账单时间", "转入转出账户类型",
                 "价格"],
            # okex 币币交易账单
            "okex_bi_to_bi_bill":
                ["uuid", "姓名", "币种",
                 "币对", "类型", "币的数量",
                 "实时价格", "交易前余额", "交易后余额",
                 "手续费", "账单时间"],
            # 中币 用户注册信息
            "zb_basic_info_ori":
                ["用户地址", "用户名", "注册邮箱",
                 "认证手机", "真实姓名", "身份证号",
                 "注册IP"],
            # 中币 法币交易记录
            "zb_otc_record_ori":
                ["订单ID", "下单时间", "确认支付时间", "确认收款时间",
                 "取消时间", "申诉时间", "市场类型", "广告ID",
                 "商家用户ID", "广告类型", "下单用户ID", "下单类型",
                 "交易单价", "交易数量", "交易金额", "订单状态",
                 "操作"]}

        # 不同数据的变量名对应的文件名及文件类型(excel或csv)
        self.different_varname_to_filename_and_filekind = {
            "huobi_otc_trade_record":
                ["different/huobi/otc交易记录", ".xlsx"],
            "bi_an_current_assets_and_wallets":
                ["different/binance/Current_Assets_and_Wallets", ".xlsx"],
            "bi_an_access_logs":
                ["different/binance/Access_Logs", ".xlsx"],
            "okex_user_yu_e":
                ["different/okex/用户余额", ".xlsx"],
            "okex_tongyi_zhanghu":
                ["different/okex/统一账户", ".xlsx"],
            "okex_user_device_information":
                ["different/okex/用户设备信息", ".xlsx"],
            "okex_jiaoge_bill":
                ["different/okex/交割账单币本位", ".xlsx"],
            "okex_bi_to_bi_bill":
                ["different/okex/币币账单", ".xlsx"],
            "zb_basic_info_ori":
                ["different/zb/basic_info_ori", ".xlsx"],
            "zb_otc_record_ori":
                ["different/zb/otc_record_ori", ".xlsx"]}


class Split_same_Output_Data():
    # 将文件相同数据进行分割的类
    # 在 DataBody 进行多进程输出文件的时候需要用到

    def __init__(self, bi_to_bi_trade, chong_bi_record, ti_bi_record,
                 login_information, law_bi_trade_record,
                 haxi_diaozheng_information_yitai_all,
                 haxi_diaozheng_information_bochang_all,
                 haxi_diaozheng_information_bite_all,
                 haxi_huizong_yitai_all,
                 haxi_huizong_bochang_all,
                 haxi_huizong_bite_all,
                 dizhi_diaozheng_information_yitai_all,
                 dizhi_diaozheng_information_bochang_all,
                 dizhi_diaozheng_information_bite_all,
                 dizhi_huizong_yitai_all,
                 dizhi_huizong_bochang_all,
                 dizhi_huizong_bite_all,
                 register_information,
                 shenfen_information,
                 approved_devices,
                 each_file_max_line=200000):
        # 存放要输出的数据，每个数据都是DataFrame对象
        self.__output_same_data_dict = {
            "bi_to_bi_trade": bi_to_bi_trade,
            "chong_bi_record": chong_bi_record,
            "ti_bi_record": ti_bi_record,
            "login_information": login_information,
            "law_bi_trade_record": law_bi_trade_record,
            "haxi_diaozheng_information_yitai_all": haxi_diaozheng_information_yitai_all,
            "haxi_diaozheng_information_bochang_all": haxi_diaozheng_information_bochang_all,
            "haxi_diaozheng_information_bite_all": haxi_diaozheng_information_bite_all,
            "haxi_huizong_yitai_all": haxi_huizong_yitai_all,
            "haxi_huizong_bochang_all": haxi_huizong_bochang_all,
            "haxi_huizong_bite_all": haxi_huizong_bite_all,
            "dizhi_diaozheng_information_yitai_all": dizhi_diaozheng_information_yitai_all,
            "dizhi_diaozheng_information_bochang_all": dizhi_diaozheng_information_bochang_all,
            "dizhi_diaozheng_information_bite_all": dizhi_diaozheng_information_bite_all,
            "dizhi_huizong_yitai_all": dizhi_huizong_yitai_all,
            "dizhi_huizong_bochang_all": dizhi_huizong_bochang_all,
            "dizhi_huizong_bite_all": dizhi_huizong_bite_all,
            "register_information": register_information,
            "shenfen_information": shenfen_information,
            "approved_devices": approved_devices}
        # 单个文件最大函数
        self.each_file_max_line = each_file_max_line

    def __handle_data(self) -> None:
        '''
        分割文件
        :return:
        '''
        # 每个 excel/csv 文件中最大数据量
        each_file_max_line = self.each_file_max_line

        splited_data = {}
        for key, value in self.__output_same_data_dict.items():
            each_kind_data = []  # 存放一种数据的切割后的列表
            if value.shape[0] == 0:
                # 考虑没有数据的情况
                each_kind_data.append([value, 1])
            elif value.shape[0] <= each_file_max_line:
                # 数据量较小，一个文件可以放得下
                each_kind_data.append([value, 1])
            else:
                # 数据量较大，一个文件放不下
                length = value.shape[0] // each_file_max_line
                if value.shape[0] % each_file_max_line != 0:
                    length += 1
                for i in range(length):
                    each_kind_data.append(
                        [value[each_file_max_line * i: each_file_max_line * (i + 1)], (i + 1)])
            splited_data[key] = each_kind_data

        self.__splited_data_dict = splited_data

    def run(self) -> dict:
        '''
        分割文件的启动函数
        :return:
        '''
        self.__handle_data()
        return self.__splited_data_dict


class DataBody(Header):
    # 数据体，用于存储、增加、处理以及输出相同数据

    def __init__(self):
        super(DataBody, self).__init__()
        # 币币交易记录
        self.__bi_to_bi_trade = pd.DataFrame(
            columns=self.varname_to_header["bi_to_bi_trade"])
        # 充币记录
        self.__chong_bi_record = pd.DataFrame(
            columns=self.varname_to_header["chong_bi_record"])
        # 提币记录
        self.__ti_bi_record = pd.DataFrame(
            columns=self.varname_to_header["ti_bi_record"])
        # 登录记录
        self.__login_information = pd.DataFrame(
            columns=self.varname_to_header["login_information"])
        # 法币交易记录
        self.__law_bi_trade_record = pd.DataFrame(
            columns=self.varname_to_header["law_bi_trade_record"])
        # 哈希调证人员信息整理-以太坊
        self.__haxi_diaozheng_information_yitai_all = pd.DataFrame(
            columns=self.varname_to_header["haxi_diaozheng_information_yitai_all"])
        # 哈希调证人员信息整理-波场币
        self.__haxi_diaozheng_information_bochang_all = pd.DataFrame(
            columns=self.varname_to_header["haxi_diaozheng_information_bochang_all"])
        # 哈希调证人员信息整理-比特币
        self.__haxi_diaozheng_information_bite_all = pd.DataFrame(
            columns=self.varname_to_header["haxi_diaozheng_information_bite_all"])
        # 哈希汇总表-以太坊
        self.__haxi_huizong_yitai_all = pd.DataFrame(
            columns=self.varname_to_header["haxi_huizong_yitai_all"])
        # 哈希汇总表-波场币
        self.__haxi_huizong_bochang_all = pd.DataFrame(
            columns=self.varname_to_header["haxi_huizong_bochang_all"])
        # 哈希汇总表-比特币
        self.__haxi_huizong_bite_all = pd.DataFrame(
            columns=self.varname_to_header["haxi_huizong_bite_all"])
        # 钱包地址调证人员信息整理-以太坊
        self.__dizhi_diaozheng_information_yitai_all = pd.DataFrame(
            columns=self.varname_to_header["dizhi_diaozheng_information_yitai_all"])
        # 钱包地址调证人员信息整理-波场币
        self.__dizhi_diaozheng_information_bochang_all = pd.DataFrame(
            columns=self.varname_to_header["dizhi_diaozheng_information_bochang_all"])
        # 钱包地址调证人员信息整理-比特币
        self.__dizhi_diaozheng_information_bite_all = pd.DataFrame(
            columns=self.varname_to_header["dizhi_diaozheng_information_bite_all"])
        # 钱包地址汇总表-以太坊
        self.__dizhi_huizong_yitai_all = pd.DataFrame(
            columns=self.varname_to_header["dizhi_huizong_yitai_all"])
        # 钱包地址汇总表-波场币
        self.__dizhi_huizong_bochang_all = pd.DataFrame(
            columns=self.varname_to_header["dizhi_huizong_bochang_all"])
        # 钱包地址汇总表-比特币
        self.__dizhi_huizong_bite_all = pd.DataFrame(
            columns=self.varname_to_header["dizhi_huizong_bite_all"])
        # 用户注册信息
        self.__register_information = pd.DataFrame(
            columns=self.varname_to_header["register_information"])
        # 身份信息表
        self.__shenfen_information = pd.DataFrame(
            columns=self.varname_to_header["shenfen_information"])
        # 用户设备表
        self.__approved_devices = pd.DataFrame(
            columns=self.varname_to_header["approved_devices"])

    def append_bi_to_bi_trade(self, df: pd.DataFrame) -> None:
        # 币币交易记录 增加数据
        self.__bi_to_bi_trade = pd.concat(
            [self.__bi_to_bi_trade, df], ignore_index=True)

    def append_chong_bi_record(self, df: pd.DataFrame) -> None:
        # 充币记录 增加数据
        self.__chong_bi_record = pd.concat(
            [self.__chong_bi_record, df], ignore_index=True)

    def append_ti_bi_record(self, df: pd.DataFrame) -> None:
        # 提币记录 增加数据
        self.__ti_bi_record = pd.concat(
            [self.__ti_bi_record, df], ignore_index=True)

    def append_login_information(self, df: pd.DataFrame) -> None:
        # 登录信息 增加数据
        self.__login_information = pd.concat(
            [self.__login_information, df], ignore_index=True)

    def append_law_bi_trade_record(self, df: pd.DataFrame) -> None:
        # 法币交易记录 增加数据
        self.__law_bi_trade_record = pd.concat(
            [self.__law_bi_trade_record, df], ignore_index=True)

    def append_haxi_diaozheng_information_yitai_all(self, df: pd.DataFrame) -> None:
        # 哈希调证人员信息整理-以太坊 增加数据
        self.__haxi_diaozheng_information_yitai_all = pd.concat(
            [self.__haxi_diaozheng_information_yitai_all, df], ignore_index=True)

    def append_haxi_diaozheng_information_bochang_all(self, df: pd.DataFrame) -> None:
        # 哈希调证人员信息整理-波场币 增加数据
        self.__haxi_diaozheng_information_bochang_all = pd.concat(
            [self.__haxi_diaozheng_information_bochang_all, df], ignore_index=True)

    def append_haxi_diaozheng_information_bite_all(self, df: pd.DataFrame) -> None:
        # 哈希调证人员信息整理-比特币 增加数据
        self.__haxi_diaozheng_information_bite_all = pd.concat(
            [self.__haxi_diaozheng_information_bite_all, df], ignore_index=True)

    def append_haxi_huizong_yitai_all(self, df: pd.DataFrame) -> None:
        # 哈希汇总表-以太坊 增加数据
        self.__haxi_huizong_yitai_all = pd.concat(
            [self.__haxi_huizong_yitai_all, df], ignore_index=True)

    def append_haxi_huizong_bochang_all(self, df: pd.DataFrame) -> None:
        # 哈希汇总表-波场币 增加数据
        self.__haxi_huizong_bochang_all = pd.concat(
            [self.__haxi_huizong_bochang_all, df], ignore_index=True)

    def append_haxi_huizong_bite_all(self, df: pd.DataFrame) -> None:
        # 哈希汇总表-比特币 增加数据
        self.__haxi_huizong_bite_all = pd.concat(
            [self.__haxi_huizong_bite_all, df], ignore_index=True)

    def append_dizhi_diaozheng_information_yitai_all(self, df: pd.DataFrame) -> None:
        # 钱包地址调证人员信息整理-以太坊 增加数据
        self.__dizhi_diaozheng_information_yitai_all = pd.concat(
            [self.__dizhi_diaozheng_information_yitai_all, df], ignore_index=True)

    def append_dizhi_diaozheng_information_bochang_all(self, df: pd.DataFrame) -> None:
        # 钱包地址调证人员信息整理-波场币 增加数据
        self.__dizhi_diaozheng_information_bochang_all = pd.concat(
            [self.__dizhi_diaozheng_information_bochang_all, df], ignore_index=True)

    def append_dizhi_diaozheng_information_bite_all(self, df: pd.DataFrame) -> None:
        # 钱包地址调证人员信息整理-比特币 增加数据
        self.__dizhi_diaozheng_information_bite_all = pd.concat(
            [self.__dizhi_diaozheng_information_bite_all, df], ignore_index=True)

    def append_dizhi_huizong_yitai_all(self, df: pd.DataFrame) -> None:
        # 钱包地址汇总表-以太坊 增加数据
        self.__dizhi_huizong_yitai_all = pd.concat(
            [self.__dizhi_huizong_yitai_all, df], ignore_index=True)

    def append_dizhi_huizong_bochang_all(self, df: pd.DataFrame) -> None:
        # 钱包地址汇总表-波场币 增加数据
        self.__dizhi_huizong_bochang_all = pd.concat(
            [self.__dizhi_huizong_bochang_all, df], ignore_index=True)

    def append_dizhi_huizong_bite_all(self, df: pd.DataFrame) -> None:
        # 钱包地址汇总表-比特币 增加数据
        self.__dizhi_huizong_bite_all = pd.concat(
            [self.__dizhi_huizong_bite_all, df], ignore_index=True)

    def append_register_information(self, df: pd.DataFrame) -> None:
        # 用户注册信息 增加数据
        self.__register_information = pd.concat(
            [self.__register_information, df], ignore_index=True)

    def append_shenfen_information(self, df: pd.DataFrame) -> None:
        # 身份信息表 增加数据
        self.__shenfen_information = pd.concat(
            [self.__shenfen_information, df], ignore_index=True)

    def append_approved_devices(self, df: pd.DataFrame) -> None:
        # 用户设备表 增加一条记录
        self.__approved_devices = pd.concat(
            [self.__approved_devices, df], ignore_index=True)

    def append_df_dict(self, df_dict: dict) -> None:
        # 传入一个处理完的 df 的字典, 找到对应的 df 加入数据
        for key, value in df_dict.items():
            if key in ["picture", "summary", "invalid"]:
                if key == "picture":
                    for key1, value1 in value.items():
                        if key1 == "dizhi":
                            for key2, value2 in value1.items():
                                if key2 == "eth":
                                    self.append_dizhi_diaozheng_information_yitai_all(value2)
                                elif key2 == "tron":
                                    self.append_dizhi_diaozheng_information_bochang_all(value2)
                                elif key2 == "bite":
                                    self.append_dizhi_diaozheng_information_bite_all(value2)
                        elif key1 == "haxi":
                            for key2, value2 in value1.items():
                                if key2 == "eth":
                                    self.append_haxi_diaozheng_information_yitai_all(value2)
                                elif key2 == "tron":
                                    self.append_haxi_diaozheng_information_bochang_all(value2)
                                elif key2 == "bite":
                                    self.append_haxi_diaozheng_information_bite_all(value2)
                elif key == "summary":
                    for key1, value1 in value.items():
                        if key1 == "dizhi":
                            for key2, value2 in value1.items():
                                if key2 == "eth":
                                    self.append_dizhi_huizong_yitai_all(value2)
                                elif key2 == "tron":
                                    self.append_dizhi_huizong_bochang_all(value2)
                                elif key2 == "bite":
                                    self.append_dizhi_huizong_bite_all(value2)
                        elif key1 == "haxi":
                            for key2, value2 in value1.items():
                                if key2 == "eth":
                                    self.append_haxi_huizong_yitai_all(value2)
                                elif key2 == "tron":
                                    self.append_haxi_huizong_bochang_all(value2)
                                elif key2 == "bite":
                                    self.append_haxi_huizong_bite_all(value2)
            elif value.shape[0] > 0:
                if key == "register_information":
                    self.append_register_information(value)
                elif key == "chongbi_record":
                    self.append_chong_bi_record(value)
                elif key == "tibi_record":
                    self.append_ti_bi_record(value)
                elif key == "login_information":
                    self.append_login_information(value)
                elif key == "law_bi_trade_record":
                    self.append_law_bi_trade_record(value)
                elif key == "bi_to_bi_trade":
                    self.append_bi_to_bi_trade(value)


    def handle_bi_to_bi_trade(self) -> None:
        '''
        表头：交易所  UID  姓名  身份证  身份证归属地  订单类型  价格
        顺序： 0      1    2      3           4         5       6
        表头：数量   交易额  订单号   时间  币对   买卖方向
        顺序： 7      8        9      10    11      12
        '''
        # 处理 币币交易记录
        df = self.__bi_to_bi_trade

        if df.shape[0] > 0:
            # 保证有数据
            # 交易所、身份证归属地 不处理，
            # 剩余其他字段 处理方式为 2
            df[[each_column for each_column in df.columns if each_column not in ["交易所", "身份证归属地"]]] = \
                df[[each_column for each_column in df.columns if each_column not in ["交易所", "身份证归属地"]]].applymap(
                lambda x: clear_no_meaning_string(x, handle_mode=2))

            # 统一 时间 字段格式
            df["时间"] = df["时间"].apply(handle_for_time)

            # 价格，数量，交易额字段 转数值型
            # 以此去掉内部的异常值
            df[["价格", "数量", "交易额"]] = df[["价格", "数量", "交易额"]].applymap(str_to_float)

            # 去重方式: 简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__bi_to_bi_trade = df


    def handle_chong_bi_record(self) -> None:
        '''
        表头：交易所  UID  姓名  身份证  身份证归属地  本方地址 来源地址
        顺序： 0      1     2     3         4          5         6
        表头：订单号   充值方向   币种   时间   数量
        顺序： 7         8        9      10     11
        '''
        # 处理 充币记录
        df = self.__chong_bi_record

        if df.shape[0] > 0:
            # 如果来源地址为以太坊，则 本方地址、来源地址、订单号 全小写
            def func(x):
                result = {}
                if judge_bizhong(x["来源地址"]) == "yitai":
                    result["本方地址"] = small_write(x["本方地址"])
                    result["来源地址"] = small_write(x["来源地址"])
                    result["订单号"] = small_write(x["订单号"])
                else:
                    result["本方地址"] = x["本方地址"]
                    result["来源地址"] = x["来源地址"]
                    result["订单号"] = x["订单号"]
                return pd.Series(result)

            df[["本方地址", "来源地址", "订单号"]] = df.apply(func, axis=1)

            # 去除无意义字符
            # 交易所、身份证归属地 不处理
            # 本方地址、来源地址、订单号  处理方式为 1
            # 剩余的其他字段 处理方式为 2
            df[["本方地址", "来源地址", "订单号"]] = \
                df[["本方地址", "来源地址", "订单号"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=1))
            df[[each_column for each_column in df.columns if each_column not in ["交易所", "身份证归属地", "本方地址", "来源地址", "订单号"]]] = \
                df[[each_column for each_column in df.columns if each_column not in ["交易所", "身份证归属地", "本方地址", "来源地址", "订单号"]]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=2))

            #币种字段大写
            df["币种"] = df["币种"].apply(big_write)

            # 统一时间格式
            df["时间"] = df["时间"].apply(handle_for_time)

            # 数量 字段转数值型
            # 以此去掉内部的异常值
            df["数量"] = df["数量"].apply(str_to_float)

            # 去重方式: 按 来源地址 和 订单号 降序排序
            # 以 交易所 UID 姓名 来源地址 订单号 时间 为关键列去重
            df = df.sort_values(by=["来源地址", "订单号"], ascending=[False, False])

            drop_key = ["交易所", "UID", "姓名", "来源地址", "订单号", "时间"]
            df = df.drop_duplicates(subset=drop_key, inplace=False)

            self.__chong_bi_record = df


    def handle_ti_bi_record(self) -> None:
        '''
        表头：交易所  UID  姓名  身份证  身份证归属地  去向地址   订单号
        顺序： 0      1     2     3          4          5         6
        表头：充值方向    币种    时间    数量
        顺序：  7          8       9      10
        '''
        # 处理 提币记录
        df = self.__ti_bi_record

        if df.shape[0] > 0:
            # 如果去向地址为以太坊， 则 去向地址、订单号全小写
            def func(x):
                result = {}
                if judge_bizhong(x["去向地址"]) == "yitai":
                    result["去向地址"] = small_write(x["去向地址"])
                    result["订单号"] = small_write(x["订单号"])
                else:
                    result["去向地址"] = x["去向地址"]
                    result["订单号"] = x["订单号"]
                return pd.Series(result)

            df[["去向地址", "订单号"]] = df.apply(func, axis=1)

            # 去除无意义字符
            # 交易所 身份证归属地 不处理
            # 去向地址 处理方式为 1
            # 剩余其他字段 处理方式为 2
            df["去向地址"] = df["去向地址"].apply(
               clear_no_meaning_string, args=(1, ))
            df[[each_column for each_column in df.columns if each_column not in ["交易所", "身份证归属地", "去向地址"]]] = \
                df[[each_column for each_column in df.columns if each_column not in ["交易所", "身份证归属地", "去向地址"]]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=2))

            # 币种 字段全大写
            df["币种"] = df["币种"].apply(big_write)

            # 统一 时间 字段格式
            df["时间"] = df["时间"].apply(handle_for_time)

            # 数量 字段 转数值型
            # 以此去掉内部的异常值
            df["数量"] = df["数量"].apply(str_to_float)

            # 去重方式: 按 去向地址、订单号 降序排序
            # 以 交易所、UID、姓名、去向地址、订单号、时间为关键列去重
            df = df.sort_values(by=["去向地址", "订单号"], ascending=[False, False])

            drop_key = ["交易所", "UID", "姓名", "去向地址", "订单号", "时间"]
            df = df.drop_duplicates(subset=drop_key, inplace=False)

            self.__ti_bi_record = df


    def handle_login_information(self) -> None:
        '''
        表头：交易所  UID   姓名   身份证  身份证归属地  手机号  登录时间
        顺序： 0       1     2      3          4         5        6
        表头：登录端   IP地址    国家    区域    省份   城市     ISP
        顺序： 7       8          9       10     11    12      13
        '''
        # 处理 登录记录
        df = self.__login_information

        if df.shape[0] > 0:
            # 去除无意义字符
            # 交易所、身份证归属地、国家、区域、省份、城市、ISP 不处理
            # 剩余字段 处理方式为 2
            df[[each_column for each_column in df.columns if each_column not in ["交易所", "身份证归属地址", "国家", "区域", "省份", "城市", "ISP"]]] = \
                df[[each_column for each_column in df.columns if each_column not in ["交易所", "身份证归属地址", "国家", "区域", "省份", "城市", "ISP"]]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=2))

            # 统一 登录时间 字段 格式
            df["登录时间"] = df["登录时间"].apply(handle_for_time)

            # 手机号 字段 去掉后面的 .0
            def func(x):
                try:
                    return str(x).split(".")[0]
                except:
                    return None

            df["手机号"] = df["手机号"].apply(func)

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__login_information = df


    def handle_law_bi_trade_record(self) -> None:
        '''
        表头：交易所  UID   姓名   身份证  身份证归属地  订单号  币种
        顺序： 0      1      2      3          4          5      6
        表头：数量    价格    法币    交易额   时间   买卖方向
        顺序： 7       8      9       10       11      12
        '''
        # 处理 法币交易记录
        df = self.__law_bi_trade_record

        if df.shape[0] > 0:
            # 去除无意义字符
            # 交易所、身份证归属地、法币 不处理
            # 订单号 处理方式为 1
            # 剩余其他字段 处理方式为 2
            df["订单号"] = df["订单号"].apply(
                clear_no_meaning_string, args=(1, ))
            df[[each_column for each_column in df.columns if each_column not in ["交易所", "身份证归属地", "订单号"]]] = \
                df[[each_column for each_column in df.columns if each_column not in ["交易所", "身份证归属地", "订单号"]]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=2))

            # 币种 字段 全大写
            df["币种"] = df["币种"].apply(big_write)

            # 统一 时间 字段 格式
            df["时间"] = df["时间"].apply(handle_for_time)

            # 数量、价格、交易额 字段转数值型
            # 以此去掉内部的异常值
            df[["数量", "价格", "交易额"]] = df[["数量", "价格", "交易额"]].applymap(str_to_float)

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__law_bi_trade_record = df


    def handle_haxi_diaozheng_information_yitai_all(self) -> None:
        '''
        表头：交易哈希  区块高度   钱包地址   本方标签
        顺序：  0         1         2          3
        表头：交易时间  交易金额   交易余额   交易方向
        顺序：  4         5          6         7
        表头：对方交易钱包    对方标签   币种
        顺序：   8             9         10
        '''
        # 处理 哈希调证人员信息-以太坊
        df = self.__haxi_diaozheng_information_yitai_all

        if df.shape[0] > 0:
            # 去除无意义字符
            # 交易哈希、钱包地址、本方标签、币种 处理方式为 1
            # 剩余其他字段 处理方式为 2
            df[["交易哈希", "钱包地址", "本方标签", "币种"]] = \
                df[["交易哈希", "钱包地址", "本方标签", "币种"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=1))
            df[[each_column for each_column in df.columns if each_column not in ["交易哈希", "钱包地址", "本方标签", "币种"]]] = \
                df[[each_column for each_column in df.columns if each_column not in ["交易哈希", "钱包地址", "本方标签", "币种"]]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=2))

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__haxi_diaozheng_information_yitai_all = df


    def handle_haxi_diaozheng_information_bochang_all(self) -> None:
        '''
        表头：交易哈希  区块高度   钱包地址   本方标签
        顺序：  0         1         2          3
        表头：交易时间  交易金额   交易余额   交易方向
        顺序：  4         5          6         7
        表头：对方交易钱包    对方标签   币种
        顺序：   8             9         10
        '''
        # 处理 哈希调证人员信息-波场币
        df = self.__haxi_diaozheng_information_bochang_all

        if df.shape[0] > 0:
            # 去除无意义字符
            # 交易哈希、钱包地址、本方标签、币种 处理方式为 1
            # 剩余其他字段 处理方式为 2
            df[["交易哈希", "钱包地址", "本方标签", "币种"]] = \
                df[["交易哈希", "钱包地址", "本方标签", "币种"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=1))
            df[[each_column for each_column in df.columns if each_column not in ["交易哈希", "钱包地址", "本方标签", "币种"]]] = \
                df[[each_column for each_column in df.columns if
                    each_column not in ["交易哈希", "钱包地址", "本方标签", "币种"]]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=2))

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__haxi_diaozheng_information_bochang_all = df


    def handle_haxi_diaozheng_information_bite_all(self) -> None:
        '''
        表头：交易哈希  区块高度   钱包地址   本方标签
        顺序：  0         1         2          3
        表头：交易时间  交易金额   交易余额   交易方向
        顺序：  4         5          6         7
        表头：对方交易钱包    对方标签   币种
        顺序：   8             9         10
        '''
        # 处理 哈希调证人员信息-比特币
        df = self.__haxi_diaozheng_information_bite_all

        if df.shape[0] > 0:
            # 去除无意义字符
            # 交易哈希、钱包地址、本方标签、币种 处理方式为 1
            # 剩余其他字段 处理方式为 2
            df[["交易哈希", "钱包地址", "本方标签", "币种"]] = \
                df[["交易哈希", "钱包地址", "本方标签", "币种"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=1))
            df[[each_column for each_column in df.columns if each_column not in ["交易哈希", "钱包地址", "本方标签", "币种"]]] = \
                df[[each_column for each_column in df.columns if
                    each_column not in ["交易哈希", "钱包地址", "本方标签", "币种"]]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=2))

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__haxi_diaozheng_information_bite_all = df


    def handle_haxi_huizong_yitai_all(self) -> None:
        '''
        表头：交易哈希   UID   姓名  身份证   身份证归属地
        顺序： 0         1      2      3          4
        表头：交易所  交易所用户地址   手机    邮箱
        顺序： 5         6             7       8
        '''
        # 处理 哈希汇总表-以太坊
        df = self.__haxi_huizong_yitai_all

        if df.shape[0] > 0:
            # 去除无意义字符
            # 身份证归属地、交易所 不处理
            # 交易哈希、交易所用户地址、手机、邮箱 处理方式为 1
            # 剩余其他字段(UID、姓名、身份证) 处理方式为 2
            df[["交易哈希", "交易所用户地址", "手机", "邮箱"]] = \
                df[["交易哈希", "交易所用户地址", "手机", "邮箱"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=1))
            df[["UID", "姓名", "身份证"]] = \
                df[["UID", "姓名", "身份证"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=2))

            # 手机号 字段 去掉后面的 .0
            def func(x):
                try:
                    return str(x).split(".")[0]
                except:
                    return None

            df["手机"] = df["手机"].apply(func)

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__haxi_huizong_yitai_all = df


    def handle_haxi_huizong_bochang_all(self) -> None:
        '''
        表头：交易哈希   UID   姓名  身份证   身份证归属地
        顺序： 0         1      2      3          4
        表头：交易所  交易所用户地址   手机    邮箱
        顺序： 5         6             7       8
        '''
        # 处理 哈希汇总表-波场币
        df = self.__haxi_huizong_bochang_all

        if df.shape[0] > 0:
            # 去除无意义字符
            # 身份证归属地、交易所 不处理
            # 交易哈希、交易所用户地址、手机、邮箱 处理方式为 1
            # 剩余其他字段(UID、姓名、身份证) 处理方式为 2
            df[["交易哈希", "交易所用户地址", "手机", "邮箱"]] = \
                df[["交易哈希", "交易所用户地址", "手机", "邮箱"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=1))
            df[["UID", "姓名", "身份证"]] = \
                df[["UID", "姓名", "身份证"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=2))

            # 手机号 字段 去掉后面的 .0
            def func(x):
                try:
                    return str(x).split(".")[0]
                except:
                    return None

            df["手机"] = df["手机"].apply(func)

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__haxi_huizong_bochang_all = df


    def handle_haxi_huizong_bite_all(self) -> None:
        '''
        表头：交易哈希   UID   姓名  身份证   身份证归属地
        顺序： 0         1      2      3          4
        表头：交易所  交易所用户地址   手机    邮箱
        顺序： 5         6             7       8
        '''
        # 处理 哈希汇总表-比特币
        df = self.__haxi_huizong_bite_all

        if df.shape[0] > 0:
            # 去除无意义字符
            # 身份证归属地、交易所 不处理
            # 交易哈希、交易所用户地址、手机、邮箱 处理方式为 1
            # 剩余其他字段(UID、姓名、身份证) 处理方式为 2
            df[["交易哈希", "交易所用户地址", "手机", "邮箱"]] = \
                df[["交易哈希", "交易所用户地址", "手机", "邮箱"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=1))
            df[["UID", "姓名", "身份证"]] = \
                df[["UID", "姓名", "身份证"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=2))

            # 手机 字段 去掉后面的 .0
            def func(x):
                try:
                    return str(x).split(".")[0]
                except:
                    return None

            df["手机"] = df["手机"].apply(func)

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__haxi_huizong_bite_all = df


    def handle_dizhi_diaozheng_information_yitai_all(self) -> None:
        '''
        表头：交易哈希  区块高度  钱包地址  本方标签  交易时间
        顺序：  0         1         2        3        4
        表头：交易金额   交易余额   交易方向  对方交易钱包
        顺序：  5          6         7           8
        表头：对手标签    币种
        顺序： 9          10
        '''
        # 处理 地址调证人员信息-以太坊
        df = self.__dizhi_diaozheng_information_yitai_all

        if df.shape[0] > 0:
            # 去除无意义字符
            # 钱包地址 处理方式为 1
            # 剩余其他字段 不处理
            df["钱包地址"] = df["钱包地址"].apply(
                clear_no_meaning_string, args=(1, ))

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__dizhi_diaozheng_information_yitai_all = df


    def handle_dizhi_diaozheng_information_bochang_all(self) -> None:
        '''
        表头：交易哈希  区块高度  钱包地址  本方标签  交易时间
        顺序：  0         1         2        3        4
        表头：交易金额   交易余额   交易方向  对方交易钱包
        顺序：  5          6         7           8
        表头：对手标签    币种
        顺序： 9          10
        '''
        # 处理 地址调证人员信息-波场币
        df = self.__dizhi_diaozheng_information_bochang_all

        if df.shape[0] > 0:
            # 去除无意义字符
            # 钱包地址 处理方式为 1
            # 剩余其他字段 不处理
            df["钱包地址"] = df["钱包地址"].apply(
                clear_no_meaning_string, args=(1,))

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__dizhi_diaozheng_information_bochang_all = df


    def handle_dizhi_diaozheng_information_bite_all(self) -> None:
        '''
        表头：交易哈希  区块高度  钱包地址  本方标签  交易时间
        顺序：  0         1         2        3        4
        表头：交易金额   交易余额   交易方向  对方交易钱包
        顺序：  5          6         7           8
        表头：对手标签    币种
        顺序： 9          10
        '''
        # 处理 地址调证人员信息-比特币
        df = self.__dizhi_diaozheng_information_bite_all

        if df.shape[0] > 0:
            # 去除无意义字符
            # 钱包地址 处理方式为 1
            # 剩余其他字段 不处理
            df["钱包地址"] = df["钱包地址"].apply(
                clear_no_meaning_string, args=(1,))

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__dizhi_diaozheng_information_bite_all = df


    def handle_dizhi_huizong_yitai_all(self) -> None:
        '''
        表头：钱包地址  UID  姓名   身份证  身份证归属地
        顺序：  0       1     2       3        4
        表头：交易所   手机   邮箱
        顺序：  5       6      7
        '''
        # 处理 地址汇总表-以太坊
        df = self.__dizhi_huizong_yitai_all

        if df.shape[0] > 0:
            # 去除无意义字符
            # 身份证归属地、交易所 不处理
            # 钱包地址、手机、邮箱 处理方式为 1
            # 剩余其他字段(UID、姓名、身份证) 处理方式为 2
            df[["钱包地址", "手机", "邮箱"]] = \
                df[["钱包地址", "手机", "邮箱"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=1))
            df[["UID", "姓名", "身份证"]] = \
                df[["UID", "姓名", "身份证"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=2))

            # 手机 字段 去掉后面的 .0
            def func(x):
                try:
                    return str(x).split(".")[0]
                except:
                    return None

            df["手机"] = df["手机"].apply(func)

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__dizhi_huizong_yitai_all = df


    def handle_dizhi_huizong_bochang_all(self) -> None:
        '''
        表头：钱包地址  UID  姓名   身份证  身份证归属地
        顺序：  0       1     2       3        4
        表头：交易所   手机   邮箱
        顺序：  5       6      7
        '''
        # 处理 地址汇总表-波场币
        df = self.__dizhi_huizong_bochang_all

        if df.shape[0] > 0:
            # 去除无意义字符
            # 身份证归属地、交易所 不处理
            # 钱包地址、手机、邮箱 处理方式为 1
            # 剩余其他字段(UID、姓名、身份证) 处理方式为 2
            df[["钱包地址", "手机", "邮箱"]] = \
                df[["钱包地址", "手机", "邮箱"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=1))
            df[["UID", "姓名", "身份证"]] = \
                df[["UID", "姓名", "身份证"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=2))

            # 手机 字段 去掉后面的 .0
            def func(x):
                try:
                    return str(x).split(".")[0]
                except:
                    return None

            df["手机"] = df["手机"].apply(func)

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__dizhi_huizong_bochang_all = df


    def handle_dizhi_huizong_bite_all(self) -> None:
        '''
        表头：钱包地址  UID  姓名   身份证  身份证归属地
        顺序：  0       1     2       3        4
        表头：交易所   手机   邮箱
        顺序：  5       6      7
        '''
        # 处理 地址汇总表-比特币
        df = self.__dizhi_huizong_bite_all

        if df.shape[0] > 0:
            # 去除无意义字符
            # 身份证归属地、交易所 不处理
            # 钱包地址、手机、邮箱 处理方式为 1
            # 剩余其他字段(UID、姓名、身份证) 处理方式为 2
            df[["钱包地址", "手机", "邮箱"]] = \
                df[["钱包地址", "手机", "邮箱"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=1))
            df[["UID", "姓名", "身份证"]] = \
                df[["UID", "姓名", "身份证"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=2))

            # 手机 字段 去掉后面的 .0
            def func(x):
                try:
                    return str(x).split(".")[0]
                except:
                    return None

            df["手机"] = df["手机"].apply(func)

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__dizhi_huizong_bite_all = df


    def handle_register_information(self) -> None:
        '''
        表头：交易所  UID  姓名  身份证号/护照号   国家 身份证归属地
        顺序：  0      1    2         3            4        5
        表头： 省(直辖市)   市    县   持仓总量
        顺序：   6          7     8     9
        表头： 手机号   邮箱   注册时间  银行卡号  支付宝  微信
        顺序：   10     11       12       13       14     15
        表头： 用户地址    地址所属链   地址所属币种
        顺序：   16           17          18
        '''
        # 处理 用户注册信息
        df = self.__register_information

        if df.shape[0] > 0:
            # 如果 用户地址 为以太坊, 则改为小写
            def func(x):
                if judge_bizhong(x) == "yitai":
                    return small_write(x)
                else:
                    return x
            df["用户地址"] = df["用户地址"].apply(func)

            # 去除无意义字符
            # 交易所、身份证归属地、省(直辖市)、市、县 不处理
            # 国家、用户地址 处理方式为 1
            # 剩余其他字段 处理方式为 2
            df[["国家", "用户地址"]] = \
                df[["国家", "用户地址"]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=1))
            df[[each_column for each_column in df.columns if each_column not in ["交易所", "国家", "身份证归属地", "省(直辖市)", "市", "县", "用户地址"]]] = \
                df[[each_column for each_column in df.columns if each_column not in ["交易所", "国家", "身份证归属地", "省(直辖市)", "市", "县", "用户地址"]]].applymap(
                    lambda x: clear_no_meaning_string(x, handle_mode=2))

            # 统一 注册时间 字段 格式
            df["注册时间"] = df["注册时间"].apply(handle_for_time)

            # 持仓总量 字段 转数值型
            # 以此去除内部的异常值
            df["持仓总量"] = df["持仓总量"].apply(str_to_float)

            # 手机号 字段 去掉后面的 .0
            def func(x):
                try:
                    return str(x).split(".")[0]
                except:
                    return None
            df["手机号"] = df["手机号"].apply(func)

            # 火币的初始用户注册信息会把一个人的信息仅仅根据
            # 银行卡号、支付宝、微信 分成三条
            # 需要收集火币所有用户的银行卡号、支付宝、微信 信息
            # 填充到对应用户信息的空白处
            # 之后的筛重会把同一个人的三条信息筛成一条
            df_huobi = df[df["交易所"] == "huobi"]  # 获取火币的数据
            df_other = df[~(df["交易所"] == "huobi")]  # 获取其他交易所的数据
            if df_huobi.shape[0] > 0:
                # 保证有火币的数据
                def func(x):
                    result = {}
                    # 获取银行卡号的非空 Series
                    series_flog = x["银行卡号"][x["银行卡号"] != ""]
                    if len(series_flog) > 0:
                        # 如果有非空值
                        result["银行卡号"] = series_flog.tolist()[0]
                    else:
                        result["银行卡号"] = ""
                    series_flog = x["支付宝"][x["支付宝"] != ""]
                    if len(series_flog) > 0:
                        # 如果有非空值
                        result["支付宝"] = series_flog.tolist()[0]
                    else:
                        result["支付宝"] = ""
                    series_flog = x["微信"][x["微信"] != ""]
                    if len(series_flog) > 0:
                        # 如果有非空值
                        result["微信"] = series_flog.tolist()[0]
                    else:
                        result["微信"] = ""
                    return pd.Series(result)
                # 找出 UID 与 银行卡号、支付宝、微信 的对应关系
                df_huobi_flog = df_huobi.groupby(["UID"]).apply(func).reset_index()
                # 原始 df_huobi 删掉 银行卡号、支付宝、微信字段, 与df_huobi_flog匹配
                df_huobi = df_huobi.drop(columns=["银行卡号", "支付宝", "微信"])
                df_huobi = pd.merge(left=df_huobi, right=df_huobi_flog, on="UID", how="left")

            # 将处理后的火币数据和其他交易所的数据合并
            df = pd.concat([df_huobi, df_other], ignore_index=True)
            # 去重方式: 按 交易所、UID、用户地址 降序排序
            # 以 交易所、UID、姓名、手机号、邮箱、用户地址为关键列去重
            df = df.sort_values(by=["交易所", "UID", "用户地址"], ascending=[False, False, False])
            df = df.drop_duplicates(subset=["交易所", "UID", "姓名", "手机号", "邮箱", "用户地址"], inplace=False)

            self.__register_information = df


    def handle_shenfen_information(self) -> None:
        '''
        表头：姓名  身份证号/护照号   身份证归属地
        顺序： 0       1                  2
        表头：前科标签   毒品种类   抓获时间   出所时间
        顺序：  3         4           5          6
        表头：管控情况    案件详情
        顺序： 7           8
        '''
        # 处理 身份信息表
        df = self.__shenfen_information

        if df.shape[0] > 0:
            # 去除无意义字符
            # 身份证号/护照号 处理方式为 1
            # 姓名 处理方式为 2
            # 其他剩余字段 不处理
            df["身份证号/护照号"] = df["身份证号/护照号"].apply(
                clear_no_meaning_string, args=(1, ))
            df["姓名"] = df["姓名"].apply(
                clear_no_meaning_string, args=(2, ))

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__shenfen_information = df


    def handle_approved_devices(self) -> None:
        '''
        表头: 姓名  UID  身份证号/护照号   身份证归属地
        顺序:  0    1          2              3
        表头: 设备名称    客户端     ip地址
        顺序:   4          5          6
        表头: 定位     最近使用时间(标准时)
        顺序:  7             8
        表头: 状态    key      value
        顺序:  9      10        11
        '''
        # 处理 用户设备表
        df = self.__approved_devices

        if df.shape[0] > 0:
            # 去除无意义字符
            # 姓名 处理方式为 2
            # 其他剩余字段不处理
            df["姓名"] = df["姓名"].apply(clear_no_meaning_string, args=(2, ))

            # 去重方式:简单去重(如果每个字段中的数据全都一样，则进行去重)
            df = df.drop_duplicates(inplace=False)

            self.__approved_devices = df


    def handle_all(self) -> None:
        # 对所有数据进行处理
        self.handle_bi_to_bi_trade()
        self.handle_chong_bi_record()
        self.handle_ti_bi_record()
        self.handle_login_information()
        self.handle_law_bi_trade_record()
        self.handle_haxi_diaozheng_information_yitai_all()
        self.handle_haxi_diaozheng_information_bochang_all()
        self.handle_haxi_diaozheng_information_bite_all()
        self.handle_haxi_huizong_yitai_all()
        self.handle_haxi_huizong_bochang_all()
        self.handle_haxi_huizong_bite_all()
        self.handle_dizhi_diaozheng_information_yitai_all()
        self.handle_dizhi_diaozheng_information_bochang_all()
        self.handle_dizhi_diaozheng_information_bite_all()
        self.handle_dizhi_huizong_yitai_all()
        self.handle_dizhi_huizong_bochang_all()
        self.handle_dizhi_huizong_bite_all()
        self.handle_register_information()
        self.handle_shenfen_information()
        self.handle_approved_devices()


    def pool_output_tongyong(self, output_address: str, key: str,
                             output_data: pd.DataFrame, flog: int) -> None:
        '''
        多进程输出的通用输出函数
        :param output_address: 要输出的文件路径
        :param key: 要输出的文件的种类
        :param output_data: 要输出的数据
        :param flog: 要输出的数据的第几个文件
        :return:
        '''
        if output_data.shape[0] > 0:
            # 如果为第一个文件，则文件名后面的数字不显示(即不显示 1)
            # 否则在文件名后面显示这是第几个文件
            filename = output_address + self.varname_to_filename_and_filekind[key][0] + \
                       str(flog) if str(flog) != "1" else None + \
                        self.varname_to_filename_and_filekind[key][1]

            if self.varname_to_filename_and_filekind[key][1] == ".xlsx":
                # 要输出excel文件
                output_data.astype(str).to_excel(
                    filename, index=None,
                    header=self.varname_to_header[key])
            elif self.varname_to_filename_and_filekind[key][1] == ".csv":
                # 要输出csv文件
                output_data.astype(str).to_csv(
                    filename, index=False,
                    header=self.varname_to_header[key], encoding="utf-8")


    def output_bi_to_bi_trade(self, output_address: str,
                              each_file_max_line: int=200000) -> None:
        '''
        表头：交易所  UID  姓名  身份证  身份证归属地  订单类型  价格
        顺序： 0      1    2      3           4         5       6
        表头：数量   交易额  订单号   时间  币对   买卖方向
        顺序： 7      8        9      10    11      12
        '''
        # 输出 币币交易记录
        df = self.__bi_to_bi_trade.astype(str)

        if df.shape[0] > 0:
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1

            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm币币交易记录.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[1000000 * i: 1000000 * (i + 1)].to_excel(
                        output_address + "sm币币交易记录" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_chong_bi_record(self, output_address: str,
                               each_file_max_line: int=200000) -> None:
        '''
        表头：交易所  UID  姓名  身份证  身份证归属地  本方地址  来源地址
        顺序： 0      1     2     3         4          5         6
        表头：订单号   充值方向   币种   时间   数量
        顺序： 7         8        9      10     11
        '''
        # 输出 充币记录
        df = self.__chong_bi_record.astype(str)

        if df.shape[0] > 0:
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1

            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm充币记录.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm充币记录" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_ti_bi_record(self, output_address: str,
                            each_file_max_line: int=200000) -> None:
        '''
        表头：交易所  UID  姓名  身份证  身份证归属地  去向地址   订单号
        顺序： 0      1     2     3          4          5         6
        表头：充值方向    币种    时间    数量
        顺序：  7          8       9      10
        '''
        # 输出 提币记录
        df = self.__ti_bi_record.astype(str)

        if df.shape[0] > 0:
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1

            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm提币记录.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm提币记录" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_login_information(self, output_address: str,
                                 each_file_max_line: int=200000) -> None:
        '''
        表头：交易所  UID   姓名   身份证  身份证归属地  手机号  登录时间
        顺序： 0       1     2      3          4         5        6
        表头：登录端   IP地址    国家    区域    省份   城市   ISP
        顺序： 7       8          9       10     11    12      13
        '''
        # 输出 登录记录
        df = self.__login_information.astype(str)

        if df.shape[0] > 0:
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1

            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm登录信息.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm登录信息" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_law_bi_trade_record(self, output_address: str,
                                   each_file_max_line: int=200000) -> None:
        '''
        表头：交易所  UID   姓名   身份证  身份证归属地  订单号  币种
        顺序： 0      1      2      3          4          5      6
        表头：数量    价格    法币    交易额   时间   买卖方向
        顺序： 7       8      9       10       11      12
        '''
        # 输出 法币交易记录
        df = self.__law_bi_trade_record.astype(str)

        if df.shape[0] > 0:
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1

            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm法币交易记录.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm法币交易记录" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_haxi_diaozheng_information_yitai_all(self, output_address: str) -> None:
        '''
        表头：交易哈希  区块高度   钱包地址   本方标签
        顺序：  0         1         2          3
        表头：交易时间  交易金额   交易余额   交易方向
        顺序：  4         5          6         7
        表头：对方交易钱包    对方标签   币种
        顺序：   8             9         10
        '''
        # 输出 哈希调证人员信息整理-以太坊
        df = self.__haxi_diaozheng_information_yitai_all.astype(str)

        if df.shape[0] > 0:
            df.to_csv(
                output_address + "sm交易哈希调证人员信息整理-以太坊.csv",
                index=False,
                header=df.columns,
                encoding="utf-8")

    def output_haxi_diaozheng_information_bochang_all(self, output_address: str) -> None:
        '''
        表头：交易哈希  区块高度   钱包地址   本方标签
        顺序：  0         1         2          3
        表头：交易时间  交易金额   交易余额   交易方向
        顺序：  4         5          6         7
        表头：对方交易钱包    对方标签   币种
        顺序：   8             9         10
        '''
        # 输出 哈希调证人员信息整理-波场币
        df = self.__haxi_diaozheng_information_bochang_all.astype(str)

        if df.shape[0] > 0:
            df.to_csv(
                output_address + "sm交易哈希调证人员信息整理-波场币.csv",
                index=False,
                header=df.columns)

    def output_haxi_diaozheng_information_bite_all(self, output_address: str) -> None:
        '''
        表头：交易哈希  区块高度   钱包地址   本方标签
        顺序：  0         1         2          3
        表头：交易时间  交易金额   交易余额   交易方向
        顺序：  4         5          6         7
        表头：对方交易钱包    对方标签   币种
        顺序：   8             9         10
        '''
        # 输出 哈希调证人员信息整理-比特币
        df = self.__haxi_diaozheng_information_bite_all.astype(str)

        if df.shape[0] > 0:
            df.to_csv(
                output_address + "sm交易哈希调证人员信息整理-比特币.csv",
                index=False,
                header=df.columns,
                encoding="utf-8")

    def output_haxi_huizong_yitai_all(self, output_address: str,
                                      each_file_max_line: int=200000) -> None:
        '''
        表头：交易哈希   UID   姓名  身份证   身份证归属地
        顺序： 0         1      2      3          4
        表头：交易所  交易所用户地址   手机    邮箱
        顺序： 5         6             7       8
        '''
        # 输出 哈希汇总表-以太坊
        df = self.__haxi_huizong_yitai_all.astype(str)

        if df.shape[0] > 0:
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1

            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm已调证哈希汇总表-以太坊.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm已调证哈希汇总表-以太坊" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_haxi_huizong_bochang_all(self, output_address: str,
                                        each_file_max_line: int=200000) -> None:
        '''
        表头：交易哈希   UID   姓名  身份证   身份证归属地
        顺序： 0         1      2      3          4
        表头：交易所  交易所用户地址   手机    邮箱
        顺序： 5         6             7       8
        '''
        # 输出 哈希汇总表-波场币
        df = self.__haxi_huizong_bochang_all.astype(str)

        if df.shape[0] > 0:
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1

            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm已调证哈希汇总表-波场币.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm已调证哈希汇总表-波场币" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_haxi_huizong_bite_all(self, output_address: str,
                                     each_file_max_line: int=200000) -> None:
        '''
        表头：交易哈希   UID   姓名  身份证   身份证归属地
        顺序： 0         1      2      3          4
        表头：交易所  交易所用户地址   手机    邮箱
        顺序： 5         6             7       8
        '''
        # 输出 哈希汇总表-比特币
        df = self.__haxi_huizong_bite_all.astype(str)

        if df.shape[0] > 0:
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1

            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm已调证哈希汇总表-比特币.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm已调证哈希汇总表-比特币" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_dizhi_diaozheng_information_yitai_all(self, output_address: str) -> None:
        '''
        表头：交易哈希  区块高度  钱包地址  本方标签  交易时间
        顺序：  0         1         2        3        4
        表头：交易金额   交易余额   交易方向  对方交易钱包
        顺序：  5          6         7           8
        表头：对手标签    币种
        顺序： 9          10
        '''
        # 输出 地址调证人员信息-以太坊
        df = self.__dizhi_diaozheng_information_yitai_all.astype(str)

        if df.shape[0] > 0:
            df.to_csv(
                output_address + "sm钱包地址调证人员信息整理-以太坊.csv",
                index=False,
                header=df.columns,
                encoding="utf-8")

    def output_dizhi_diaozheng_information_bochang_all(self, output_address: str) -> None:
        '''
        表头：交易哈希  区块高度  钱包地址  本方标签  交易时间
        顺序：  0         1         2        3        4
        表头：交易金额   交易余额   交易方向  对方交易钱包
        顺序：  5          6         7           8
        表头：对手标签    币种
        顺序： 9          10
        '''
        # 输出 地址调证人员信息-波场币
        df = self.__dizhi_diaozheng_information_bochang_all.astype(str)

        if df.shape[0] > 0:
            df.to_csv(
                output_address + "sm钱包地址调证人员信息整理-波场币.csv",
                index=False,
                header=df.columns,
                encoding="utf-8")

    def output_dizhi_diaozheng_information_bite_all(self, output_address: str) -> None:
        '''
        表头：交易哈希  区块高度  钱包地址  本方标签  交易时间
        顺序：  0         1         2        3        4
        表头：交易金额   交易余额   交易方向  对方交易钱包
        顺序：  5          6         7           8
        表头：对手标签    币种
        顺序： 9          10
        '''
        # 输出 地址调证人员信息-比特币
        df = self.__dizhi_diaozheng_information_bite_all.astype(str)

        if df.shape[0] > 0:
            df.to_csv(
                output_address + "sm钱包地址调证人员信息整理-比特币.csv",
                index=False,
                header=df.columns,
                encoding="utf-8")

    def output_dizhi_huizong_yitai_all(self, output_address: str,
                                       each_file_max_line: int=200000) -> None:
        '''
        表头：钱包地址  UID  姓名   身份证  身份证归属地
        顺序：  0       1     2       3        4
        表头：交易所   手机   邮箱
        顺序：  5       6      7
        '''
        # 输出 地址汇总表-以太坊
        df = self.__dizhi_huizong_yitai_all.astype(str)

        if df.shape[0] > 0:
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1

            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm已调证钱包地址汇总表-以太坊.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm已调证钱包地址汇总表-以太坊" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_dizhi_huizong_bochang_all(self, output_address: str,
                                         each_file_max_line: int=200000) -> None:
        '''
        表头：钱包地址  UID  姓名   身份证  身份证归属地
        顺序：  0       1     2       3        4
        表头：交易所   手机   邮箱
        顺序：  5       6      7
        '''
        # 输出 地址汇总表-波场币
        df = self.__dizhi_huizong_bochang_all.astype(str)

        if df.shape[0] > 0:
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1

            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm已调证钱包地址汇总表-波场币.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm已调证钱包地址汇总表-波场币" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_dizhi_huizong_bite_all(self, output_address: str,
                                      each_file_max_line: int=200000) -> None:
        '''
        表头：钱包地址  UID  姓名   身份证  身份证归属地
        顺序：  0       1     2       3        4
        表头：交易所   手机   邮箱
        顺序：  5       6      7
        '''
        # 输出 地址汇总表-比特币
        df = self.__dizhi_huizong_bite_all.astype(str)

        if df.shape[0] > 0:
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1

            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm已调证钱包地址汇总表-比特币.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm已调证钱包地址汇总表-比特币" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_register_information(self, output_address: str,
                                    each_file_max_line: int=200000) -> None:
        '''
        表头：交易所  UID  姓名  身份证号/护照号   国家 身份证归属地
        顺序：  0      1    2         3            4        5
        表头： 省(直辖市)   市    县   持仓总量
        顺序：   6          7     8     9
        表头： 手机号   邮箱   注册时间  银行卡号  支付宝  微信
        顺序：   10     11       12       13       14     15
        表头： 用户地址    地址所属链   地址所属币种
        顺序：   16           17          18
        '''
        # 输出 用户注册信息
        df = self.__register_information.astype(str)

        if df.shape[0] > 0:
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1

            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm用户注册信息.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm用户注册信息" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_shenfen_information(self, output_address: str,
                                   each_file_max_line: int=200000) -> None:
        '''
        表头：姓名  身份证号/护照号   身份证归属地
        顺序： 0       1                  2
        表头：前科标签   毒品种类   抓获时间   出所时间
        顺序：  3         4           5          6
        表头：管控情况    案件详情
        顺序： 7           8
        '''
        # 输出 身份信息表
        df = self.__shenfen_information.astype(str)

        if df.shape[0] > 0:
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1

            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm身份信息表.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm身份信息表" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_approved_devices(self, output_address: str,
                                each_file_max_line: int=200000) -> None:
        '''
        表头: 姓名  UID  身份证号/护照号   身份证归属地
        顺序:  0    1          2              3
        表头: 设备名称    客户端     ip地址
        顺序:   4          5          6
        表头: 定位     最近使用时间(标准时)
        顺序:  7             8
        表头: 状态    key      value
        顺序:  9      10        11
        '''
        # 输出 用户设备表
        df = self.__approved_devices.astype(str)

        if df.shape[0] > 0:
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1

            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm用户设备表(币安).xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "sm用户设备表(币安)" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)


    def output_data(self, output_address: str, output_mode: str,
                    each_file_max_line: int=200000) -> None:
        '''
        对数据进行输出
        在网页上时一般使用  pool
        打包成exe时一般使用  order
        :param shuchu_address: 要输出的文件地址
        :param output_mode: 输出模式  pool  使用多进程输出
                                     order  依次输出
        :param each_file_max_line: 单个文件最大行数
        :return:
        '''

        if output_mode == "pool":
            # 先对所有数据进行处理
            self.handle_all()

            output_data_splited = Split_same_Output_Data(
                self.__bi_to_bi_trade, self.__chong_bi_record,
                self.__ti_bi_record, self.__login_information,
                self.__law_bi_trade_record,
                self.__haxi_diaozheng_information_yitai_all,
                self.__haxi_diaozheng_information_bochang_all,
                self.__haxi_diaozheng_information_bite_all,
                self.__haxi_huizong_yitai_all,
                self.__haxi_huizong_bochang_all,
                self.__haxi_huizong_bite_all,
                self.__dizhi_diaozheng_information_yitai_all,
                self.__dizhi_diaozheng_information_bochang_all,
                self.__dizhi_diaozheng_information_bite_all,
                self.__dizhi_huizong_yitai_all,
                self.__dizhi_huizong_bochang_all,
                self.__dizhi_huizong_bite_all,
                self.__register_information,
                self.__shenfen_information,
                self.__approved_devices,
                each_file_max_line=each_file_max_line)

            # 获得被切割好的要输出的数据
            splited_data = output_data_splited.run()

            pool = Pool()
            for key, value in splited_data.items():
                # key 为要输出的数据的 变量名
                # value 为列表 [[第一批数据, 1], [第二批数据, 2], ...]
                for i in value:
                    pool.apply_async(self.pool_output_tongyong, args=(output_address, key, i[0], i[1]))

            pool.close()
            pool.join()
        elif output_mode == "order":
            # 先对所有数据进行处理
            self.handle_all()

            self.output_bi_to_bi_trade(output_address, each_file_max_line)
            self.output_chong_bi_record(output_address, each_file_max_line)
            self.output_ti_bi_record(output_address, each_file_max_line)
            self.output_login_information(output_address, each_file_max_line)
            self.output_law_bi_trade_record(output_address, each_file_max_line)
            self.output_haxi_diaozheng_information_yitai_all(output_address)
            self.output_haxi_diaozheng_information_bochang_all(output_address)
            self.output_haxi_diaozheng_information_bite_all(output_address)
            self.output_haxi_huizong_yitai_all(output_address, each_file_max_line)
            self.output_haxi_huizong_bochang_all(output_address, each_file_max_line)
            self.output_haxi_huizong_bite_all(output_address, each_file_max_line)
            self.output_dizhi_diaozheng_information_yitai_all(output_address)
            self.output_dizhi_diaozheng_information_bochang_all(output_address)
            self.output_dizhi_diaozheng_information_bite_all(output_address)
            self.output_dizhi_huizong_yitai_all(output_address, each_file_max_line)
            self.output_dizhi_huizong_bochang_all(output_address, each_file_max_line)
            self.output_dizhi_huizong_bite_all(output_address, each_file_max_line)
            self.output_register_information(output_address, each_file_max_line)
            self.output_shenfen_information(output_address, each_file_max_line)
            self.output_approved_devices(output_address, each_file_max_line)



class Split_different_Output_Data():
    # 将文件相同数据进行分割的类
    # 在 DataBody_Different 进行多进程输出文件的时候需要用到

    def __init__(self, huobi_otc_trade_record,
                 bi_an_current_assets_and_wallets,
                 bi_an_access_logs,
                 okex_user_yu_e, okex_tongyi_zhanghu,
                 okex_user_device_information,
                 okex_jiaoge_bill, okex_bi_to_bi_bill,
                 zb_basic_info_ori, zb_otc_record_ori,
                 each_file_max_line=200000):
        self.__output_different_data_dict = {
            "huobi_otc_trade_record": huobi_otc_trade_record,
            "bi_an_current_assets_and_wallets":
                bi_an_current_assets_and_wallets,
            "bi_an_access_logs": bi_an_access_logs,
            "okex_user_yu_e": okex_user_yu_e,
            "okex_tongyi_zhanghu": okex_tongyi_zhanghu,
            "okex_user_device_information": okex_user_device_information,
            "okex_jiaoge_bill": okex_jiaoge_bill,
            "okex_bi_to_bi_bill": okex_bi_to_bi_bill,
            "zb_basic_info_ori": zb_basic_info_ori,
            "zb_otc_record_ori": zb_otc_record_ori}
        # 单个文件最大行数
        self.__each_file_max_line = each_file_max_line

    def __handle_data(self):
        # 每个 excel/csv 文件中最大数据量
        each_file_data_number = self.__each_file_max_line

        splited_data = {}
        for key, value in self.__output_different_data_dict.items():
            each_kind_data = []  # 存放一种数据的切割后的列表
            if len(value) == 0:
                # 考虑没有数据的情况
                each_kind_data.append([[], 1])
            elif len(value) <= each_file_data_number:
                # 数据量较小，一个文件可以放得下
                each_kind_data.append([value, 1])
            else:
                # 数据量较大，一个文件放不下
                length = len(value) // each_file_data_number
                if len(value) % each_file_data_number != 0:
                    length += 1
                for i in range(length):
                    each_kind_data.append([value[each_file_data_number * i: each_file_data_number * (i + 1)], (i + 1)])
            splited_data[key] = each_kind_data

        self.__splited_data_dict = splited_data

    def run(self):
        self.__handle_data()
        return self.__splited_data_dict


class DataBody_differnet(Header):
    # 数据体，用于存储、增加、处理以及输出不同数据

    def __init__(self):
        super(DataBody_differnet, self).__init__()
        # 火币 otc交易记录表
        self.__huobi_otc_trade_record = pd.DataFrame(
            columns=self.different_varname_to_header["huobi_otc_trade_record"])

        # 币安 流动资产和钱包表
        self.__bi_an_current_assets_and_wallets = pd.DataFrame(
            columns=self.different_varname_to_header["bi_an_current_assets_and_wallets"])
        # 币安 登录记录表
        self.__bi_an_access_logs = pd.DataFrame(
            columns=self.different_varname_to_header["bi_an_access_logs"])

        # okex 用户余额表
        self.__okex_user_yu_e = pd.DataFrame(
            columns=self.different_varname_to_header["okex_user_yu_e"])
        # okex 统一账户表
        self.__okex_tongyi_zhanghu = pd.DataFrame(
            columns=self.different_varname_to_header["okex_tongyi_zhanghu"])
        # okex 用户设备信息表
        self.__okex_user_device_information = pd.DataFrame(
            columns=self.different_varname_to_header["okex_user_device_information"])
        # okex 交割账单币本位表
        self.__okex_jiaoge_bill = pd.DataFrame(
            columns=self.different_varname_to_header["okex_jiaoge_bill"])
        # okex 币币账单表
        self.__okex_bi_to_bi_bill = pd.DataFrame(
            columns=self.different_varname_to_header["okex_bi_to_bi_bill"])

        # 中币 用户注册信息表
        self.__zb_basic_info_ori = pd.DataFrame(
            columns=self.different_varname_to_header["zb_basic_info_ori"])
        # 中币 法币交易记录表
        self.__zb_otc_record_ori = pd.DataFrame(
            columns=self.different_varname_to_header["zb_otc_record_ori"])

    def append_huobi_otc_trade_record(self, df: pd.DataFrame) -> None:
        # 火币 otc交易记录 增加数据
        self.__huobi_otc_trade_record = pd.concat(
            [self.__huobi_otc_trade_record, df], ignore_index=True)

    def append_bi_an_current_assets_and_wallets(self, df: pd.DataFrame) -> None:
        # 币安 流动资产和钱包表 增加数据
        self.__bi_an_current_assets_and_wallets = pd.concat(
            [self.__bi_an_current_assets_and_wallets, df], ignore_index=True)

    def append_bi_an_access_logs(self, df: pd.DataFrame) -> None:
        # 币安 登录信息表 增加数据
        self.__bi_an_access_logs = pd.concat(
            [self.__bi_an_access_logs, df], ignore_index=True)

    def append_okex_user_yu_e(self, df: pd.DataFrame) -> None:
        # okex 用户余额表 增加数据
        self.__okex_user_yu_e = pd.concat(
            [self.__okex_user_yu_e, df], ignore_index=True)

    def append_okex_tongyi_zhanghu(self, df: pd.DataFrame) -> None:
        # okex 统一账户表 增加数据
        self.__okex_tongyi_zhanghu = pd.concat(
            [self.__okex_tongyi_zhanghu, df], ignore_index=True)

    def append_okex_user_device_information(self, df: pd.DataFrame) -> None:
        # okex 用户设备信息表 增加数据
        self.__okex_user_device_information = pd.concat(
            [self.__okex_user_device_information, df], ignore_index=True)

    def append_okex_jiaoge_bill(self, df: pd.DataFrame) -> None:
        # okex 交割账单币本位表 增加数据
        self.__okex_jiaoge_bill = pd.concat(
            [self.__okex_jiaoge_bill, df], ignore_index=True)

    def append_okex_bi_to_bi_bill(self, df: pd.DataFrame) -> None:
        # okex 币币交易账单 增加数据
        self.__okex_bi_to_bi_bill = pd.concat(
            [self.__okex_bi_to_bi_bill, df], ignore_index=True)

    def append_zb_basic_info_ori(self, df: pd.DataFrame) -> None:
        # 中币 用户注册信息 增加数据
        self.__zb_basic_info_ori = pd.concat(
            [self.__zb_basic_info_ori, df], ignore_index=True)

    def append_zb_otc_record_ori(self, df: pd.DataFrame) -> None:
        # 中币 法币交易记录 增加数据
        self.__zb_otc_record_ori = pd.concat(
            [self.__zb_otc_record_ori, df], ignore_index=True)

    def output_huobi_otc_trade_reocrd(self, output_address: str,
                                      each_file_max_line: int=200000) -> None:
        '''
        表头：订单号   对手方UID   币种   数量   价格
        顺序： 0          1        2      3      4
        表头：法币   交易额   时间   UID   买卖方向
        顺序： 5       6      7     8       9
        '''
        # 输出 火币 otc交易记录
        df = self.__huobi_otc_trade_record

        if df.shape[0] > 0:
            df = df.drop_duplicates(inplace=False)  # 简单去重
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1
            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/huobi/otc交易记录.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/huobi/otc交易记录" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_bi_an_current_assets_and_wallets(self, output_address: str,
                                                each_file_max_line: int=200000) -> None:
        '''
        表头：Name   User ID   Asset Ticker   Asset Name   Total Position
        顺序： 0          1        2              3              4
        表头：Estimated BTC Value   Deposit Wallet Address   Label/Tag/Memo
        顺序：          5                       6                  7
        '''
        # 输出 币安 流动资产和钱包表
        df = self.__bi_an_current_assets_and_wallets

        if df.shape[0] > 0:
            df = df.drop_duplicates(inplace=False)
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1
            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/binance/Current_Assets_and_Wallets.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/binance/Current_Assets_and_Wallets" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

        print("币安 流动资产和钱包表 输出结束")

    def output_bi_an_access_logs(self, output_address: str,
                                 each_file_max_line: int=200000) -> None:
        '''
        表头：User ID   Operation   Client   Client Version  Real IP
        顺序： 0            1          2              3          4
        表头：Geolocation   Browser   Timestamp (UTC)
        顺序：    5            6             7
        '''
        # 输出 币安 登录信息表
        df = self.__bi_an_access_logs

        if df.shape[0] > 0:
            df = df.drop_duplicates(inplace=False)
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1
            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/binance/Access_Logs.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/binance/Access_Logs" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_okex_user_yu_e(self, output_address: str,
                              each_file_max_line: int=200000) -> None:
        '''
        表头：uuid   姓名  currency_symbol   total_balance   pt
        顺序： 0       1          2               3          4
        '''
        # 输出 okex 用户余额表
        df = self.__okex_user_yu_e

        if df.shape[0] > 0:
            df = df.drop_duplicates(inplace=False)
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1
            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/okex/用户余额.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/okex/用户余额" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_okex_tongyi_zhanghu(self, output_address: str,
                                   each_file_max_line: int=200000) -> None:
        '''
        表头：uuid   姓名  时间   业务线     产品名称    类型
        顺序： 0      1     2       3         4         5
        表头: 数量  单位  收益  手续费  仓位余额变动   仓位余额
        顺序:  6     7     8    9         10           11
        表头: 交易账户余额变动    交易账户余额   币种名称
        顺序:       12              13           14
        表头:  成交价   trade_side
        顺序:    15       16
        '''
        # 输出 okex 统一账户表
        df = self.__okex_tongyi_zhanghu

        if df.shape[0] > 0:
            df = df.drop_duplicates(inplace=False)
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1
            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/okex/统一账户.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/okex/统一账户" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_okex_user_device_information(self, output_address: str,
                                            each_file_max_line: int=200000) -> None:
        '''
        表头：uuid   姓名  设备制造商   设备型号   操作系统
        顺序:  0      1       2           3         4
        表头: 操作系统版本  屏幕高度   屏幕宽度
        顺序:     5          6          7
        表头:  运营商名称   网络类型  设备id   mac地址
        顺序:     8           9       10       11
        表头:  设备imei号   wifi信息  是否越狱
        顺序:     12          13        14
        表头:  是否模拟器  是否为debug   是否双开
        顺序:     15          16          17
        '''
        # 输出 okex 用户设备信息表
        df = self.__okex_user_device_information

        if df.shape[0] > 0:
            df = df.drop_duplicates(inplace=False)
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1
            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/okex/用户设备信息.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/okex/用户设备信息" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_okex_jiaoge_bill(self, output_address: str,
                                each_file_max_line: int=200000) -> None:
        '''
        表头：uuid   姓名  合约周期id  币种  类型    仓位数量
        顺序:  0      1       2        3     4         5
        表头: 收益   账单时间    转入转出账户类型   价格
        顺序:  6        7             8           9
        '''
        # 输出 okex 交割账单币本位表
        df = self.__okex_jiaoge_bill

        if df.shape[0] > 0:
            df = df.drop_duplicates(inplace=False)
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1
            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/okex/交割账单币本位.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/okex/交割账单币本位" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_okex_bi_to_bi_bill(self, output_address: str,
                                  each_file_max_line: int=200000) -> None:
        '''
        表头: uuid  姓名  币种  币对   类型   币的数量
        顺序:  0     1     2     3     4       5
        表头:  实时价格    交易前余额   交易后余额
        顺序:    6            7           8
        表头:  手续费   账单时间
        顺序:    9        10
        '''
        # 输出 okex 币币交易账单
        df = self.__okex_bi_to_bi_bill

        if df.shape[0] > 0:
            df = df.drop_duplicates(inplace=False)
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1
            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/okex/币币账单.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/okex/币币账单" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_zb_basic_info_ori(self, output_address: str,
                                 each_file_max_line: int=200000) -> None:
        '''
        表头：用户地址  用户名  注册邮箱  认证手机
        顺序：  0        1        2        3
        表头：真实姓名  身份证号   注册IP
        顺序：  4        5         6
        '''
        # 输出 中币 用户注册信息
        df = self.__zb_basic_info_ori

        if df.shape[0] > 0:
            df = df.drop_duplicates(inplace=False)
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1
            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/zb/basic_info_ori.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/zb/basic_info_ori" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def output_zb_otc_record_ori(self, output_address: str,
                                 each_file_max_line: int=200000) -> None:
        '''
        表头：订单ID  下单时间  确认支付时间  确认收款时间
        顺序：  0        1          2            3
        表头：取消时间  申诉时间  市场类型  广告ID
        顺序：   4         5        6       7
        表头：商家用户ID  广告类型  下单用户ID  下单类型
        顺序：   8          9         10         11
        表头：交易单价  交易数量   交易金额  订单状态  操作
        顺序：   12       13         14      15      16
        '''
        # 输出 中币 法币交易记录
        df = self.__zb_otc_record_ori

        if df.shape[0] > 0:
            df = df.drop_duplicates(inplace=False)
            length = df.shape[0] // each_file_max_line
            if df.shape[0] % each_file_max_line != 0:
                length += 1
            for i in range(length):
                if i == 0:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/zb/otc_record_ori.xlsx",
                        index=None,
                        header=df.columns)
                else:
                    df[each_file_max_line * i: each_file_max_line * (i + 1)].to_excel(
                        output_address + "/different/zb/otc_record_ori" + str(i + 1) + ".xlsx",
                        index=None,
                        header=df.columns)

    def pool_output_tongyong(self, output_address: str, key: str,
                             output_data: pd.DataFrame, flog: int) -> None:
        '''
        多进程输出的通用输出函数
        :param output_address: 要输出的文件路径
        :param key: 要输出的文件的种类
        :param output_data: 要输出的数据
        :param flog: 要输出的数据的第几个文件
        :return:
        '''
        if output_data.shape[0] > 0:
            # 如果为第一个文件，则文件名后面的数字不显示(即不显示 1)
            # 否则在文件名后面显示这是第几个文件
            filename = output_address + self.varname_to_filename_and_filekind[key][0] + \
                       str(flog) if str(flog) != "1" else None + \
                                                          self.varname_to_filename_and_filekind[key][1]

            if self.varname_to_filename_and_filekind[key][1] == ".xlsx":
                # 要输出excel文件
                output_data.to_excel(
                    filename, index=None,
                    header=self.varname_to_header[key])
            elif self.varname_to_filename_and_filekind[key][1] == ".csv":
                # 要输出csv文件
                output_data.to_csv(
                    filename, index=False,
                    header=self.varname_to_header[key], encoding="utf-8")

    def output_data(self, output_address: str, output_mode: str,
                    each_file_max_line: int=200000) -> None:
        '''
        对数据进行输出
        在网页上时一般使用  pool
        打包成exe时一般使用  order
        :param shuchu_address: 要输出的文件地址
        :param output_mode: 输出模式  pool  使用多进程输出
                                     order  依次输出
        :param each_file_max_line: 单个文件最大行数
        :return:
        '''
        if output_mode == "pool":
            # 多进程输出文件
            output_data_splited = Split_different_Output_Data(
                self.__huobi_otc_trade_record,
                self.__bi_an_current_assets_and_wallets,
                self.__bi_an_access_logs,
                self.__okex_user_yu_e, self.__okex_tongyi_zhanghu,
                self.__okex_user_device_information,
                self.__okex_jiaoge_bill, self.__okex_bi_to_bi_bill,
                self.__zb_basic_info_ori, self.__zb_otc_record_ori,
                each_file_max_line=each_file_max_line)

            # 获得被切割好的要输出的数据
            splited_data = output_data_splited.run()

            pool = Pool()
            for key, value in splited_data.items():
                # key 为要输出的数据的 变量名
                # value 为列表 [[第一批数据, 1], [第二批数据, 2], ...]
                for i in value:
                    pool.apply_async(self.pool_output_tongyong, args=(output_address, key, i[0], i[1]))

            pool.close()
            pool.join()
        elif output_mode == "order":
            # 依次输出文件
            self.output_huobi_otc_trade_reocrd(output_address, each_file_max_line)
            self.output_bi_an_current_assets_and_wallets(output_address, each_file_max_line)
            self.output_bi_an_access_logs(output_address, each_file_max_line)
            self.output_okex_user_yu_e(output_address, each_file_max_line)
            self.output_okex_tongyi_zhanghu(output_address, each_file_max_line)
            self.output_okex_user_device_information(output_address, each_file_max_line)
            self.output_okex_jiaoge_bill(output_address, each_file_max_line)
            self.output_okex_bi_to_bi_bill(output_address, each_file_max_line)
            self.output_zb_basic_info_ori(output_address, each_file_max_line)
            self.output_zb_otc_record_ori(output_address, each_file_max_line)
