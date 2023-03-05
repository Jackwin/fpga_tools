## Parse pstsnet

`parse_pstxnet_to_json` is used to parse the cadence pstxnet file and generate the pin along with the signals attached to.

In the json file, every FPGA IO has its connections with other components or connectors.

```json
 "BANK44_GC_IO_L5N": [
        "J2.126",
        "U1.AK14"
    ],
    "BANK44_GC_IO_L5P": [
        "J2.128",
        "U1.AK15"
    ],

```

## Swap connectors' pin assignment

After the PCB layput, some pins need to be swapped. In such a case, the script can boost the name reassignment process. But, some manual work is still required.

1. In the schematic, the connector is divided into two parts by default. 