__author__ = "Jianfeng Sun"
__version__ = "v1.0"
__copyright__ = "Copyright 2020"
__license__ = "GPL v3.0"
__email__ = "jianfeng.sunmt@gmail.com"
__maintainer__ = "Jianfeng Sun"

import sys
sys.path.append('../../')
from accnetbio.sequence.convert.Kind import kind


class position():

    def __init__(self, sequence):
        self.sequence = sequence
        self.len_seq = len(self.sequence)

    def single(self, pos_list):
        """

        Parameters
        ----------
        pos_list

        Returns
        -------

        """
        seq_dict = kind().todict(self.sequence)
        len_pairs = len(pos_list)
        dist_matrix = []
        for id in range(len_pairs):
            fas_id1 = pos_list[id][0]
            dist_matrix.append([
                fas_id1,
                seq_dict[fas_id1],
                fas_id1,
                0
            ])
        return dist_matrix

    def pair(self, pos_list):
        """

        Parameters
        ----------
        pos_list

        Returns
        -------

        """
        seq_dict = kind().todict(self.sequence)
        len_pairs = len(pos_list)
        dist_matrix = []
        for id in range(len_pairs):
            fas_id1 = pos_list[id][0]
            fas_id2 = pos_list[id][1]
            dist_matrix.append([
                fas_id1,
                seq_dict[fas_id1],
                fas_id1,
                fas_id2,
                seq_dict[fas_id2],
                fas_id2,
                0
            ])
        return dist_matrix


if __name__ == "__main__":
    from accnetbio.Path import to
    from accnetbio.combo.Length import length as plength
    from accnetbio.sequence.Fasta import fasta as sfasta

    # /* sequence */
    fasta_path = to('data/example/1aigL.fasta')
    sequence = sfasta().get(fasta_path)
    print(len(sequence))

    # #/* scenario of positions */
    pos_list_pair = plength(seq_sep_inferior=4).topair(len(sequence))
    pos_list_single = plength(seq_sep_inferior=4).tosgl(len(sequence))
    print(pos_list_pair)

    # #/* get positions qualified */
    p = position(sequence=sequence)
    # print(p.single(pos_list_single))
    # print(p.pair(pos_list_pair))
