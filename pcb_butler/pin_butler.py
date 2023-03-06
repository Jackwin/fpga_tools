#!/usr/bin/python

import json
import os


class primitive:
    def init(self, net_name, pin_loc):
        self.net_ = net_name
        self.pin_ = pin_loc


def getNet(self): return self.net_
def getPin(self): return self.pin_


def stripQuotes(name):
    if (len(name) > 1):
        ind1 = name.find("'")
        ind2 = name.find("'", ind1+1)
        if ind1 < 0 or ind2 < 0:
            return name
        return name[ind1+1:ind2]


'''
Get the pin number from a singnal name. For instance, CON4.20 -> 20
'''


def get_pin_num(signal_name):
    str1 = stripQuotes(signal_name)
    print(str1)
    str2 = str1.split(".")
    return str2[1]


'''
According to a net list, extract the pure corresponding pin number from a json file
net_list = ["IO_L19P_T3_35", "IO_L19P_T3_13"]pin_num = [10, 20]
file_name: pin_json from the pstxnet.dat containing the whole netlists after layout
target_connector_name: the connector name, such as "J1"
'''


def extract_pin_num(pin_json_file, source_connector_file, target_connector_name):
    pin_list = []
    print(pin_json_file)
    print(source_connector_file)
    print(target_connector_name)
    with open(pin_json_file) as f:
        net_dict = json.load(f)
        for e in source_connector_file:
           # print(e)
            if e in net_dict:
                node_list = net_dict[e]
                # print(node_list)
                # find the target part
                index = 0
                for item in node_list:
                    if target_connector_name in item:
                        pin_num = get_pin_num(node_list[index])
                        # print(pin_num)
                        pin_list.append(pin_num)
                        break
                    else:
                        index = index + 1
        f.close()
    return pin_list
    # print(pin_list)


'''
Read the pin assignment with its own net from brd netlist.
The key information starts from line 27
source:
Pin     Type      SigNoise Model          Net
---     ----      --------------          ---
1       UNSPEC                            GND
2       UNSPEC                            GND
3       UNSPEC                            IO_L15P_T2_DQS_13
4       UNSPEC                            IO_L14P_T2_SRCC_13

return:

'''


def parse_brd_net(filename):
    pin_net_list = []
    with open(filename, 'r') as f:
        for i in f.readlines()[27:]:
            pin_net_list.append(i.strip().split())
        f.close()
    # print(pin_net_list[0][2])
    return pin_net_list


'''Parse the nets from orCAD CIS'''


def parseXnet(filename):
    netsList = {}
    f_ = filename.readline().strip()
    while (True):
        if f_ != "NET_NAME" and f_ != "END.":
            f_ = filename.readline().strip()
        if f_ == "NET_NAME":
            f_ = filename.readline().strip()
            netName = stripQuotes(f_)
            nodes = []
            while (True):
                f_ = filename.readline().strip()
                f_split = f_.split()
                if f_split[0] == "NODE_NAME":
                    node = f_split[1] + "." + f_split[2]
                    nodes.append(node)
                if f_ and (f_ == "NET_NAME" or f_ == "END."):
                    break
            netsList[netName] = nodes
        elif f_ == "END.":
            break
    return netsList


'''Save the netlist to a json file'''


def save_to_json(filename, netlist_obj):
    with open(filename, 'w') as f:
        json.dump(netlist_obj, f, sort_keys=True, indent=4)


'''Locate a net in which componentssignal name: listpin name: list'''


def from_json(dct):
    if isinstance(dct, dict) and "IO_L19P_T3_35" in dct:
        return dct["IO_L19P_T3_35"]


# The whole pin json file

netlist_file = "./mszu9/mszu9-pin.json"

# with open("./pstxnet.dat")as file:
#    nets = parseXnet(file)
#    file.close()

#save_to_json(netlist_file, nets)

part = "J1"
# the netlist from pab layout
target_brd_filename = "J1"
index = "1"
pin_file_path = './mszu9/netlist-2023-2-25'
#part = "PL_DDR"
#target_brd_filename = "FPGA"
#index = "1"

# TODO: Add DDR signal filtering
source_pin_file = part + "_source_pin_part_" + index + ".txt"
brd_net_file = target_brd_filename + ".txt"
target_pin_file = part + "_" + "target" + "_pin_part_" + index + ".txt"

source_pin_file = os.path.join(pin_file_path, source_pin_file)
target_pin_file = os.path.join(pin_file_path, target_pin_file)
brd_net_file = os.path.join(pin_file_path, brd_net_file)
print(source_pin_file)

source_net_list = []
with open(source_pin_file, 'r') as f:
    while (True):
        net = f.readline().strip()
        source_net_list.append(net)
        if not net:
            break
    f.close()

print(source_net_list)

#connector_file = os.path.join(pin_file_path, part + ".txt")
connector_name = "J1"
source_pin_list = extract_pin_num(
    netlist_file, source_net_list, connector_name)
print(source_pin_list)
print(" ---------------- ")
pin_net_list = parse_brd_net(brd_net_file)
print(pin_net_list)

print(len(pin_net_list[70]))


with open(target_pin_file, 'w') as f:
    for pin in source_pin_list:
        print(pin)
        if (len(pin_net_list[int(pin)-1]) > 2):
            target_net = pin_net_list[int(pin)-1][2]
        else:
            target_net = "NO_CONNECT"
        f.write(target_net+'\r\n')
        print(target_net)
    f.close()
#extract_pin_num(netlist_file, net_list)

# print(get_pin_num('CON4.20'))
# print(net_dict)# if "IO_L19P_T3_35" in net_dict:# json.dumps(data)
# data1 = {'IO_L16N_T2_10': ['U1.AE15', 'CON4.45'],# 'IO_L23N_T3_35': ['U1.A14', 'CON5.65']}#data = json.dumps(nets, sort_keys=True, indent=4)# print(data)
