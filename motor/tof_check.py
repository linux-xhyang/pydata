import math
import re

import pandas as pd


class tofnode:
    def __init__(self, distance, step):
        self.distance = distance
        self.step = step

    def to_string(self):
        return "{distance},{step}".format(
            distance=self.distance, step=self.step)


class tofdata:
    def __init__(self, sn, data):
        self.sn = sn
        self.table = []
        self.theory_table = []
        self.diff_table = []
        nodes = re.findall('\((.*?)\)', data)
        if len(nodes) > 0:
            for v in nodes:
                values = v.split(',')
                if len(values) == 2:
                    self.table.append(
                        tofnode(
                            int(values[0].strip()), int(values[1].strip())))
        else:
            nodes = data.split(',')
            for v in nodes:
                values = v.split(':')
                if len(values) == 2:
                    self.table.append(
                        tofnode(
                            int(values[0].strip()), int(values[1].strip())))

        self.theory_compute()
        self.diff_compute()

    def theory_compute(self):
        best_step_2000 = 315.46
        compute_2000_step = -1
        for n in self.table:
            x = n.distance
            if abs(x - 2000) <= 100:
                compute_2000_step = n.step
                break

        if compute_2000_step > 0:
            offset = compute_2000_step - best_step_2000
            for n in self.table:
                x = n.distance
                y = int(331.0 +
                        (131.3 * math.pow(x, -0.9855) + 0.2498 - 0.341128) /
                        0.0013 + offset + 43100 / x - 23.22)
                self.theory_table.append(tofnode(x, y))

    def diff_compute(self):
        for x1, x2 in zip(self.table, self.theory_table):
            x = x1.distance
            y = x1.step - x2.step
            self.diff_table.append(tofnode(x, y))

    def get_diff_by_distance(self, distance):
        for i in self.diff_table:
            if abs(distance - i.distance) <= 100:
                return i.step

        return 0

    def get_raw_and_thoery_by_distance(self, distance):
        for x1, x2 in zip(self.table, self.theory_table):
            if abs(distance - x1.distance) <= 100:
                return 'raw:{step1},{step2}'.format(
                    step1=x1.step, step2=x2.step)

        return 'raw:0,0'

    def greater_than_bound(self, val):
        for var in self.diff_table:
            if abs(var.step) > val:
                return True
        return False

    def to_string(self):
        return "sn = {sn}, \ntable = {table}\n        {theory}\ndiff =    {diff}".format(
            sn=self.sn,
            table=';'.join(e.to_string() for e in self.table),
            theory=';'.join(e.to_string() for e in self.theory_table),
            diff=';'.join(str(e.step) + "       " for e in self.diff_table))


class tof_check:
    def __init__(self):
        self.tof_datas = []
        self.df = pd.read_excel(
            '~/Documents/TOF/135/TOF工厂测试数据/M135JCN_DVT1.xlsx')
        self.read_excel()
        self.write_excel()

        count = 0
        for var in self.tof_datas:
            if var.greater_than_bound(12):
                count += 1

        print("total : %d,failed : %f" % (len(self.tof_datas),
                                          count / len(self.tof_datas)))

    def read_excel(self):
        heads = self.df.columns.values
        for i in self.df.index.values:
            row_data = self.df.ix[i, ['sn', 'item', 'content']]
            if type(row_data['content']) == str and row_data['content'].strip(
            ).startswith('TofTables'):
                self.tof_datas.append(
                    tofdata(row_data['sn'], row_data['content']))
            elif row_data['item'] != None and row_data['item'] == '无感对焦数据读取':
                self.tof_datas.append(
                    tofdata(row_data['sn'], row_data['content']))

    def print_data(self):
        print("count = ", len(self.tof_datas))
        for i in self.tof_datas:
            print(i.to_string())

    def write_excel(self):
        headers = [
            '1000', '1200', '1400', '1600', '1800', '2000', '2500', '3000',
            '3600'
        ]
        dicts = {}
        dicts['sn'] = []
        dicts_raw = {}
        dicts_raw['sn'] = []
        for h in headers:
            dicts[h] = []
            dicts_raw[h] = []

        for i in self.tof_datas:
            dicts['sn'].append(i.sn)
            dicts_raw['sn'].append(i.sn)
            for h in headers:
                dicts[h].append(i.get_diff_by_distance(int(h)))
                dicts_raw[h].append(i.get_raw_and_thoery_by_distance(int(h)))

        pds = pd.DataFrame.from_dict(dicts)
        pds.style.bar(
            subset=headers, axis=None, color='#d65f5f').to_excel(
                'tof.xlsx', sheet_name='tof', engine="openpyxl", index=False)

        pds_raw = pd.DataFrame.from_dict(dicts_raw)
        pds_raw.to_excel(
            'tof_raw.xlsx',
            sheet_name='tof_raw',
            engine="openpyxl",
            index=False)


check = tof_check()
check.print_data()
