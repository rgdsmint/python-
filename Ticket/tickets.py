"""
Usage:
    ticket [-dgktz] <from> <to> <date>

options:
        -h --help       显示菜单
        -d              动车
        -g              高铁
        -k              快车
        -t              特快
        -z              直达

Examples：
    Please input the trainType you want to search :dgz
    Please input the city you want leave :南京
    Please input the city you will arrive :北京
    Please input the date(Example:2017-09-27) :2018-03-01
"""
from docopt import docopt
import requests
from stations import station_code, code_station
from prettytable import PrettyTable

'''
查票程序
使用方法如上
'''
class SearchTicket:

    # 接受所查票的参数 : 车票类型 起始车站 日期
    def __init__(self):
        self.trainOption = input('-d动车 -g高铁 -k快速 -t特快 -z直达\n请输入您要查询的车次类型(如:-dg) :')
        self.fromStation = input('请输入您出发的城市(如:滁州) :')
        self.toStation = input('请输入您要前往的城市(如:上海) :')
        self.Date = input('请输入日期(如:2018-05-09) :')
        self.train = self.trains()
    # 处理信息  得出官网信息  并写成列表
    def searchTrain(self):
        arguments = {
            'option': self.trainOption,
            'from_station': station_code.get(self.fromStation, None),
            'to_station': station_code.get(self.toStation, None),
            'date': self.Date
        }
        self.options = ''.join([key for key in arguments['option']])
        url = 'https://kyfw.12306.cn/otn/leftTicket/query?\
leftTicketDTO.train_date={}\
&leftTicketDTO.from_station={}&\
leftTicketDTO.to_station={}\
&purpose_codes=ADULT'.format(arguments['date'], arguments['from_station'], arguments['to_station'])
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url, verify=False)
        try:
            self.raw_trains = r.json()['data']['result']
        except:
            exit('输入有误')
    # 解析信息  得出各参数
    def trains(self):
        for item in self.raw_trains:
            data_list = item.split('|')
            trainNum = data_list[3]
            initial = trainNum[0].lower()
            if not self.options or initial in self.options:
                from_station_code = data_list[6]
                to_station_code = data_list[7]
                from_station_name = code_station.get(from_station_code)
                to_station_name = code_station.get(to_station_code)
                start_time = data_list[8]
                arrive_time = data_list[9]
                time_duration = data_list[10]
                business_seat = data_list[32] or '--'  # 商务座
                first_seat = data_list[31] or '--'  # 一等座
                second_seat = data_list[30] or '--'  # 二等座
                high_sort_sleep = data_list[21] or '--'  # 高级软卧
                sort_sleep = data_list[23] or '--'  # 软卧
                move_slepp = data_list[33] or '--'  # 动卧
                hard_sleep = data_list[28] or '--'  # 硬卧
                sort_seat = data_list[24] or '--'  # 软座
                hard_seat = data_list[29] or '--'  # 硬座
                no_seat = data_list[26] or '--'  # 无座
                other_seat = data_list[22] or '--'  # 其它

                train = [
                    trainNum,
                    '\n'.join([from_station_name, to_station_name]),
                    '\n'.join([start_time, arrive_time]),
                    time_duration,
                    business_seat,
                    first_seat,
                    second_seat,
                    high_sort_sleep,
                    sort_sleep,
                    move_slepp,
                    hard_sleep,
                    sort_seat,
                    hard_seat,
                    no_seat,
                    other_seat
                ]
                yield train
    # 将参数可视化
    def pretty_print(self):
        pt = PrettyTable()
        article = '车次 站点 时间 历时  商务座 一等座 二等座 高级软卧 软卧 动卧 硬卧 软座 硬座 无座 其他'.split()
        pt._set_field_names(article)
        for train in self.train:
            pt.add_row(train)
        print(pt)
# 运行程序
if __name__ == '__main__':
    while True:
        st = SearchTicket()
        st.searchTrain()
        st.pretty_print()
