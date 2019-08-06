import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-dir', "--directory", nargs = '?', type = str, default = "hiasdf")
parser.add_argument('-file', "--file", nargs ='?', type = str)

args = parser.parse_args()

print(args.directory)
