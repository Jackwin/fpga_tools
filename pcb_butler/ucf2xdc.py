#!/usr/bin/python

import os
import re
import argparse

parser = argparse.ArgumentParser(description="options to the script")
parser.add_argument('--ucf-file', type=str, default = None)
parser.add_argument('--ddr-type', type = str, default = 'DDR3')
parser.add_argument('--prefix', type = str, default = None)
parser.add_argument('--io-standard', type = str, default = None)
args = parser.parse_args()

ucf_file = args.ucf_file
ddr_type = args.ddr_type
prefix = args.prefix
io_standard = args.io_standard

'''
NET     "PL_DDR_A12"      LOC = "K10"  -> ['PL_DDR_A12', 'K10']
'''
def get_pin_loc(name):
    if (len(name) > 1):
        pin_loc = re.findall(r'"([^"]*)"', name)
        return pin_loc

def format_constr(pin_loc):
    constr = "set_property " + "PACKAGE_PIN " + pin_loc[1] + " [get_ports " + prefix + '_' + pin_loc[0].replace('PL_DDR', ddr_type) + "]"
    return constr

def add_iostandards():
    print("set_property IOSTANDARD  SSTL15_T_DCI [get_ports {ddr3_dq[*]}]")


    print("set_property IOSTANDARD  DIFF_SSTL15_T_DCI [get_ports {ddr3_dqs[*]}]")
    print("set_property IOSTANDARD  SSTL15 [get_ports {ddr3_addr[*]}]")
    print("set_property IOSTANDARD  SSTL15 [get_ports {ddr3_ba[*]}]")
    print("set_property IOSTANDARD  SSTL15 [get_ports {ddr3_dm[*]}]")
    print("set_property IOSTANDARD  SSTL15 [get_ports {ddr3_cas_n}]")
    print("set_property IOSTANDARD  SSTL15 [get_ports {ddr3_ras_n}]")
    print("set_property IOSTANDARD  SSTL15 [get_ports {ddr3_we_n}]")
    print("set_property IOSTANDARD  SSTL15 [get_ports {ddr3_odt}]")
    #print("set_property IOSTANDARD = LVCMOS15 get_ports {ddr3_reset_n}")

#UCF_FIlE = "PL_DDR.ucf"
ucf_dict = {}
with open(ucf_file, 'r') as f:
    line = f.readline()
    while(line):
        # ignore an empty line
        if(len(line.strip()) != 0):
            #print(line)
            pin_loc = get_pin_loc(line)
            #print(pin_loc)
            print(format_constr(pin_loc))
        line = f.readline()
add_iostandards()
