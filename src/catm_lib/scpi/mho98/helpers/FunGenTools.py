import argparse

def GetParser():
    parser = argparse.ArgumentParser(
        description="These scripts are used to control function generator from a PC, such as the Tektronix ASG3252"
    )

    parser.add_argument(
        "-ip",
        "--IPAddr",
        type=str,
        required=True,
        help="The IP address of the function generator"
    )

    parser.add_argument(
        "-ch",
        "--Channel",
        type=str,
        choices=['1',"2"],
        required=True,
        help="The output channel of the function generator"
    )

    parser.add_argument(
        "-f",
        "--Frequency",
        type=str,
        default=None,
        required=False,
        help="The output frequency of the function generator"
    )

    parser.add_argument(
        "-v",
        "--Voltage",
        type=str,
        default=None,
        required=False,
        help="The output voltage of the function generator"
    )

    parser.add_argument(
        "-o",
        "--Output",
        type=str,
        default='OFF',
        choices=['ON',"OFF"],
        required=False,
        help="Enabled or disable the output using ON or OFF"
    )

    args = parser.parse_args()
    return args