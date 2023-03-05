#!/usr/bin/python
import json
import os
import re
import csv


class ConstraintCook(object):
    ddr_file = ""
    raw_ddr_net_and_pin_list = []
    refined_ddr_net_and_pin_list = []

    def __init__(self, ddr_file):
        self.ddr_file = ddr_file

    def __is_in(self, sub_str, str):
        if str.find(sub_str) != -1:
            return True
        else:
            return False

    def __get_num_from_str(self, str):
        return re.sub("\D", "", str)

    def __locate_num_in_str(self, str, num):
        return str.find(num)

    def __replace_str(self, string, source_str, target_str):
        return (string.replace(source_str, target_str))

    def __str_to_list(self, string):
        return (list(string.split(" ")))

    def __remove_spaces(self, list):
        res = []
        for e in list:
            if e.strip():
                res.append(e)
        return res
        # res = map(lambda x: x.strip(), res)
        # res = map(lambda x: x.rstrip(), res)

    # add square brackets

    '''
	Add square brackets to the numer, for instance, PL_DDR_A10 -> PL_DDR_A[10]
	'''

    def add_square_bracket(self, string):
        num = self.__get_num_from_str(string)
        num_len = len(num)
        start_loc = string.find(num)
        new_str = list(string)
        new_str.insert(start_loc, "[")
        end_loc = start_loc + num_len + 1
        new_str.insert(end_loc, "]")
        new_str = ''.join(new_str)
        return new_str

    '''
	From FPGA.txt, extract the DDR pin and add constraints.
    From the FPGA.txt in the layout get the DDR nets and the assigned pins in FPGA
    , which is called raw_ddr_net_and_pin.
    ['H2', 'UNSPEC', 'PL_DDR_DQ14\n']
 	'''

    def get_raw_ddr_net_and_pin(self, file, prefix):
        with open(file, 'r') as f:
            line = f.readline()
            while (line):
                if self.__is_in(prefix, line):
                    # line = line.strip()
                    line = line.rstrip("\n")
                    s = self.__str_to_list(line)
                    self.raw_ddr_net_and_pin_list.append(
                        self.__remove_spaces(s))
                line = f.readline()
            f.close()

    def show_raw_ddr_net_and_pin(self):
        print(self.raw_ddr_net_and_pin_list)

    '''
    Refine the raw_ddr_net_and_pin
    ['H2', 'UNSPEC', 'PL_DDR_DQ14\n']- > ['H2','PL_DDR_DQ14\n']
    '''

    def refine_ddr_net_and_pin(self):
        for k in self.raw_ddr_net_and_pin_list:
            if (len(k) < 3):
                print("refine ddr net and pin should contain more than 2 elements.")
                break
            k.pop(1)
            self.refined_ddr_net_and_pin_list.append(k)

    def show_refine_ddr_net_and_pin(self):
        print(self.refined_ddr_net_and_pin_list)

    def ddr_pin_assignment_format(self, pin, net):
        pin_constr = "NET     " + '"' + net + '"' + \
            "      " + "LOC = " + '"' + pin + '"' + '\n'
        return pin_constr
    '''
    Generate the ucf to validate the pin assignment in Xilinx DDR IP.
    NET     "PL_DDR_DQ28"      LOC = "A2"
    '''

    def gen_ddr_pin_assignment(self, file, prefix):
        self.get_raw_ddr_net_and_pin(file, prefix)
        self.refine_ddr_net_and_pin()
        with open(prefix+".ucf", 'w') as f:
            for k in self.refined_ddr_net_and_pin_list:
                f.write(self.ddr_pin_assignment_format(k[0], k[1]))
            f.close()
            print("---- The DDR constraint file has been written to " + prefix+".ucf")

    # TODO 1. add ddr pin constraint on vivado 2. add bank_pin and io nets
    def export_etch_length(self):
        with open("./ms7z100/bank_10_net_len.csv") as f:
            # reader = csv.reader(f, delimiter=' ', quotechar='|')
            csv_reader = csv.DictReader(f)
            row = next(csv_reader)
            for line in csv_reader:
                print(line)
            # print(next(csv_reader))
