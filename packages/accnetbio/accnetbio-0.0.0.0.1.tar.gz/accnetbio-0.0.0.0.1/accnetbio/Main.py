import os
import sys
import argparse
import subprocess
from pyfiglet import Figlet


def main():
    parser = argparse.ArgumentParser(description='Welcome to accNetBio!')
    vignette1 = Figlet(font='standard')
    print(vignette1.renderText('accNetBio'))
    # vignette2 = Figlet(font='doom')
    # print(vignette2.renderText('Welcome'))

    parser.add_argument(
        "--method", "-m",
        metavar='method',
        dest='m',
        # required=True,
        type=str,
        help='str - a method can be: unipartite | bipartite | cumulative',
    )
    parser.add_argument(
        "--fasta_fpn", "-mol_f",
        metavar='fasta_fpn',
        dest='mol_path',
        # required=True,
        type=str,
        help='str - molecule sequence full file path',
    )
    parser.add_argument(
        "--net_fpn", "-net_f",
        metavar='net_fpn',
        dest='net_f',
        # required=True,
        type=str,
        help='str - full file path of relationships between any two molecules',
    )
    parser.add_argument(
        "--window_size", "-ws",
        metavar='window_size',
        dest='ws',
        # default=2,
        type=int,
        help='int - window size',
    )
    parser.add_argument(
        "--seq_sep_inferior", "-ssinf",
        metavar='seq_sep_inferior',
        dest='ssinf',
        default=0,
        type=int,
        help='int - sequence separation inferior',
    )
    parser.add_argument(
        "--seq_sep_superior", "-sssup",
        metavar='seq_sep_superior',
        dest='sssup',
        default=None,
        type=str,
        help='str - sequence separation superior',
    )
    parser.add_argument(
        "--pair_mode", "-pmode",
        metavar='pair_mode',
        dest='pmode',
        default='patch',
        type=str,
        help='str - mode of global pairs: patch | memconp | cross | unchanged',
    )
    parser.add_argument(
        "--assign_mode", "-amode",
        metavar='assign_mode',
        dest='amode',
        default='hash',
        type=str,
        help='str - mode of assignment: hash | hash_ori | hash_rl | pandas | numpy',
    )
    parser.add_argument(
        "--input_kind", "-ikind",
        metavar='input_kind',
        dest='ikind',
        default='general',
        type=str,
        help='str - input kind for relationships of a network file: general | simulate | freecontact | gdca | cmmpred | plmc',
    )
    parser.add_argument(
        "--cumu_ratio", "-cr",
        metavar='cumu_ratio',
        dest='cr',
        default=1.,
        type=float,
        help='float - cumulative ratio',
    )
    parser.add_argument(
        "--is_sv", "-issv",
        metavar='is_sv',
        dest='issv',
        default=True,
        type=bool,
        help='bool - to make sure if save to a file',
    )
    parser.add_argument(
        "--output_net", "-o",
        metavar='output_net',
        dest='o',
        default=None,
        type=str,
        help='str - output net to a file.',
    )

    args = parser.parse_args()

    fpnf = os.path.dirname(__file__) + 'Controller.py'
    print(fpnf)
    print(args.ibam)
    if args.m == None:
        print('Attention! the m option must be added to your command.')
        raise ValueError
    if args.mol_f == None:
        print('Attention! the mol_f option must be added to your command.')
        raise ValueError
    if args.net_f == None:
        print('Attention! the net_f option must be added to your command.')
        raise ValueError
    if args.ws == None:
        print('Attention! the ws option must be added to your command.')
        raise ValueError
    # cmd = 'python ' + fpnf + ' -h'
    cmd = 'python ' + fpnf + ' -m ' + args.m + ' -mol_f ' + args.mol_f + ' -net_f ' + str(args.net_f) + ' -ws ' + args.ws + ' -ssinf ' + args.ssinf + ' -sssup ' + args.sssup + ' -pmode ' + str(args.pmode) + ' -amode ' + str(args.amode) + ' -ikind ' + str(args.ikind) + ' -cr ' + args.cr + ' -is_sv ' + str(args.is_sv) + ' -o ' + str(args.o)
    # print(cmd)
    s = subprocess.Popen(cmd, shell=True)
    s.communicate()