#!/usr/bin/python
# Cook_file.py is used to make conversion among different format files
import json
import os
import re


class FileCook(object):
    '''In the brd file, the useful contents start from 27th line'''
    __brd_start_line = 27
    pstxnet_net_list = {}
    brd_pin_net_list = {}

    # TODO add pwr pattern list

    def __init__(self, pstxnet_file, brd_file):
        self.brd_file = brd_file
        self.pstxnet_file = pstxnet_file

    '''
    Get the string in the quotes. 'CON3.J4' -> CON3.J4
    '''

    def __strip_quotes(self, name):
        if (len(name) > 1):
            ind1 = name.find("'")
            ind2 = name.find("'", ind1+1)
            if ind1 < 0 or ind2 < 0:
                return name
            return name[ind1+1:ind2]

    '''
    Parse the pstxnel.dat from CIS 
    '''

    def parse_pstxnet(self):
        with open(self.pstxnet_file) as file:
            f_ = file.readline().strip()
            while (True):
                if f_ != "NET_NAME" and f_ != "END.":
                    f_ = file.readline().strip()
                if f_ == "NET_NAME":
                    f_ = file.readline().strip()
                    netName = self.__strip_quotes(f_)
                    nodes = []
                    while (True):
                        f_ = file.readline().strip()
                        f_split = f_.split()
                        if f_split[0] == "NODE_NAME":
                            node = f_split[1] + "." + f_split[2]
                            nodes.append(node)
                        if f_ and (f_ == "NET_NAME" or f_ == "END."):
                            break
                    self.pstxnet_net_list[netName] = nodes
                    # print(nodes)
                elif f_ == "END.":
                    break
            file.close()

    def parse_brd(self, brd_file):
        for line in brd_file.readlines()[self.__brd_start_line:]:
            self.brd_pin_net_list.append(line.strip().split())

    def save_to_json(self, source_file, json_file):
        with open(json_file, 'w') as f:
            json.dump(source_file, f, sort_keys=True, indent=4)
            f.close()

    def parse_pstxnet_to_json(self, json_file):
        print(" ---- parse pstxnet to json ------ ")
        self.parse_pstxnet()
       # print(self.pstxnet_net_list)
        self.save_to_json(self.pstxnet_net_list, json_file)

    '''
    Get the part name from the part net name
    "U1.AA9" -> U1
    '''

    def __get_part_name(self, part_net):
        s = part_net.strip().split('.', 2)
        # print(s[0])
        return s[0]

    '''
    Rule1: every net should connect at least two different parts.

    Correct:
    "FPGA_DONE": ["U1.AA9", "R9.1", "R10.2"]
    Error:
    "FPGA_ERROR": ["U1.Y10", "U1.Y11"]
    "IO_L1P_T0_AD0P_35": ["U1.L15"]
    '''

    def rule_check(self, json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
            f.close

        for k, v in data.items():
            # print(v)
            '''
            Net only placed in one pin in a single part
            "IO_L1P_T0_AD0P_35": ["U1.L15"]
            '''
            if (len(v) < 2):
                print("\033[31m Not connected net found: \033[0m" + k)
            else:
                part_list = []
                for e in v:
                    part_list.append(self.__get_part_name(e))
                # print(part_list)

                '''
                Deduplicate the part
                ['U1', 'U1', 'U2'] -> ['U1', 'U2']
                '''
                dedupliate_part_list = list(set(part_list))
                if (len(dedupliate_part_list) < 2):
                    print("\033[31m Net only placed in one part found: \033[0m" +
                          k)

    '''
    Get the power signals. Manually, check the powers to avoid isolated pwr because of naming issues.
    For instance, the right name for 3.3V is PWR_3V3, but some power lines are renamed to PWR_3V due to TYPO.
    '''

    def filter_power(self, json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
            f.close

        pwr_pattern = r"(.*)+\d+V"
        pwr_pattern2 = r"(.*)+\d+v"
        pwr_pattern3 = r"(.*)+VCC"
        for k, v in data.items():
            if re.match(pwr_pattern, k) or re.match(pwr_pattern2, k) or re.match(pwr_pattern3, k):
                print("Power signal found " + k)
