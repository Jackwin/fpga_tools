#!/usr/bin/python
import os
import file_cook as cook
import constr_cook as constr_cook

pstxnet_file = "./ms7z100-netlist/pstxnet.dat"
brd_file = "./ms7z100/FPGA-11-22.txt"
json_file = "pin.json"
json_file_test = "pin_test.json"

file_cook = cook.FileCook(pstxnet_file, brd_file)
file_cook.parse_pstxnet_to_json(json_file)
file_cook.rule_check(json_file)
# file_cook.filter_power(json_file)

constr_cook = constr_cook.ConstraintCook(brd_file)
#constr_cook.get_raw_ddr_net_and_pin(brd_file, 'PL_DDR')
# constr_cook.show_raw_ddr_net_and_pin()
# constr_cook.refine_ddr_net_and_pin()
# constr_cook.show_refine_ddr_net_and_pin()
constr_cook.gen_ddr_pin_assignment(brd_file, 'PL_DDR')
constr_cook.export_etch_length()
