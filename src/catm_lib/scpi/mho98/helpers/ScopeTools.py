import argparse

def GetParser():
    parser = argparse.ArgumentParser(
        description="These scripts are used to query data from Keysight DSO-X 2024A oscilloscope to a PC"
    )

    parser.add_argument(
        "-ip",
        "--IPAddr",
        type=str,
        required=True,
        help="IP address of the oscilloscope"
    )

    parser.add_argument(
        "-ch",
        "--Channel",
        type=str,
        required=True,
        help="Channel number (e.g., CHAN1)"
    )

    parser.add_argument(
        "-of",
        "--OutFile",
        type=str,
        required=True,
        help="Path of the output root file"
    )

    parser.add_argument(
        "-n",
        "--NumWFs",
        type=int,
        required=True,
        help="The number of waveforms to save"
    )

    args = parser.parse_args()
    return args


def print_preamble(pre_list):
    print("=============================")
    print("===== Printing Preamble =====")
    print("=============================")
    format_str = ["Data format: ", "Waveform type: ", "Number of data points: ", "Number of averages: ", "Time difference (between two points): ", "Start time: ", "X reference point: ", "Voltage scale: ", "Vertical offset: ", "Vertical ref. value: "]
    
    if pre_list[0] == '+0': format_str[0] += "BYTE"
    elif pre_list[0] == '+1': format_str[0] += "WORD"
    elif pre_list[0] == '+2': format_str[0] += "ASCii"

    if pre_list[1] == '+0': format_str[1] += "NORMAL"
    elif pre_list[1] == '+1': format_str[1] += "PEAK DETECT"
    elif pre_list[1] == '+2': format_str[1] += "AVERAGE"

    format_str[2] += pre_list[2].replace("+","")
    format_str[3] += pre_list[3].replace("+","")
    format_str[4] += str(round(float(pre_list[4]) * 1e9,3)) + " ns"
    format_str[5] += str(round(float(pre_list[5]) * 1e6,3)) + " us"
    format_str[6] += str(round(float(pre_list[6]) * 1e6,3)) + " us"
    format_str[7] += str(round(float(pre_list[7]) * 1e3,3)) + " mV/count"

    format_str[8] += str(round(float(pre_list[8]) * 1e3,3)) + " mV"

    for nstr in format_str:
        print(nstr)
    print()