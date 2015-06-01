from math import log, sqrt
import pandas as pd


def get_unique_count_list(input_list):
    myset = set(input_list)
    list2 = list(myset)
    return len(list2)


def get_matching_matrix(groundtruthAssignment, algorithmAssignment):
    nData = len(algorithmAssignment)
    nClusters = get_unique_count_list(algorithmAssignment)
    nTruths = get_unique_count_list(groundtruthAssignment)
    # print nClusters, nTruths
    df_index = range(nClusters)
    # change df_columns if cluster number is starting from 1 in ground truth
    df_columns = range(nTruths)
    df_matrix = pd.DataFrame(0, index=df_index, columns=df_columns)
    for i in range(nData):
        df_matrix.loc[algorithmAssignment[i], groundtruthAssignment[i]] += 1
    return df_matrix


def purity(groundtruthAssignment, algorithmAssignment):

    purity = 0
    # TODO
    # Compute the purity
    df_matrix = get_matching_matrix(groundtruthAssignment, algorithmAssignment)
    purity_num = 0
    purity_den = 0
    for x in df_matrix.index:
        # to calculate purity,sum(max(row-wise))/sum(row-wise)
        purity_num += df_matrix.loc[x, :].max()
        purity_den += df_matrix.loc[x, :].sum()
    purity = purity_num*1.0/purity_den

    return purity


def NMI(groundtruthAssignment, algorithmAssignment):

    NMI = 0
    # TODO
    # Compute the NMI
    # compute matching matrix
    df_matrix = get_matching_matrix(groundtruthAssignment, algorithmAssignment)
    nData = len(algorithmAssignment)
    H_c = 0
    H_t = 0
    pci_list = []
    ptj_list = []
    print df_matrix
    for x in df_matrix.index:
        pci = (df_matrix.loc[x, :].sum()*1.0)/nData
        H_c -= pci * log(pci)
        pci_list.append(pci)
    for y in df_matrix.columns:
        ptj = df_matrix.loc[:, y].sum()*1.0/nData
        H_t -= ptj * log(ptj)
        ptj_list.append(ptj)
    I_ct = 0
    for x in df_matrix.index:
        for y in df_matrix.columns:
            pij = df_matrix.loc[x, y]*1.0/nData
            if pij == 0:
                print 'pij=0'
                continue
            I_ct += pij * log(pij*1.0/(pci_list[x]*ptj_list[y]))
    NMI = I_ct / (sqrt(H_c*H_t))
    return NMI
