__author__ = "Jianfeng Sun"
__version__ = "v1.0"
__copyright__ = "Copyright 2020"
__license__ = "GPL v3.0"
__email__ = "jianfeng.sunmt@gmail.com"
__maintainer__ = "Jianfeng Sun"

import sys
sys.path.append('../../../')
from accnetbio.Path import to


class kind(object):

    def __init__(self, ):
        pass

    def todict(self, seq):
        seq_dict = {}
        len_seq = len(seq)
        for i in range(len_seq):
            seq_dict[i+1] = seq[i]
        return seq_dict


if __name__ == "__main__":
    p = kind()
    from protein.sequence.Fasta import fasta as psfasta
    seq = psfasta().getMerged(fasta_fpn=to('data/protein/fasta/memconp_test_n51/1xqfA.fasta'))

    print(p.todict(seq))