#
# by John Vxlan (c) 2022
#

import argparse
from variables import Variables
from template import Template

def main():
    parser = argparse.ArgumentParser(description="CLI Templater")
    parser.add_argument('-t', '--template', default='template')
    parser.add_argument('-v', '--variable', default='variables')

    args = parser.parse_args()

    v = Variables(args.variable)

    for host in range(v.number_of_hosts):
        Template(args.template).generate_host(v.get_variable_collection(host))
        print("*****")

if __name__ == "__main__":
    main()
