import numpy as np
from numpy import linalg as LA
from Bio.PDB import *
import scipy.sparse as sp

import gzip
import biotite.structure.io.pdb as pdb
import biotite.structure as struc
import biotite.application.dssp as dssp

"""

"""
#
#def get_seq_and_coord(pdb_file=None, pdb_id="", pdb_model=0, pdb_chain="A"):
#    """
#    pdb_file:file of pdb 
#    output seq and coordinate  of a pdb file.
#    """
#    amino2abv = {
#            'ALA':'A',    'ARG':'R',  'ASN':'N',  'ASP':'D',  'CYS':'C',
#            'GLN':'Q',    'GLU':'E',  'GLY':'G',  'HIS':'H',  'ILE':'I',
#            'LEU':'L',    'LYS':'K',  'MET':'M',  'PHE':'F',  'PRO':'P',
#            'SER':'S',    'THR':'T',  'TRP':'W',  'TYR':'Y',  'VAL':'V'}
#    if pdb_file[-3:] == ".gz":
#        with gzip.open(pdb_file,"rt") as f:
#            structure = PDBParser().get_structure(pdb_id,f)
#    else:
#        structure = PDBParser().get_structure(pdb_id,pdb_file)
#
#    chain = [j for i in list(structure[pdb_model]) if i.id == pdb_chain for j in list(i)]
#    seq = ''.join([amino2abv[i.resname] if i.resname in amino2abv.keys() else 'X' for i in chain])
#    coord = np.array([j.coord  for i in chain for j in i if j.name == "CA"],dtype=np.float32)
#    return seq, coord
#

def get_coord_sasa_and_sec(pdb_file_path):
    """
    pdb_file_path: example  a.pdb or a.pdb.gz
    """
    amino2abv = {
        'ALA':'A',    'ARG':'R',  'ASN':'N',  'ASP':'D',  'CYS':'C',
        'GLN':'Q',    'GLU':'E',  'GLY':'G',  'HIS':'H',  'ILE':'I',
        'LEU':'L',    'LYS':'K',  'MET':'M',  'PHE':'F',  'PRO':'P',
        'SER':'S',    'THR':'T',  'TRP':'W',  'TYR':'Y',  'VAL':'V'}

    if pdb_file_path[-3:] == ".gz":
        with gzip.open(pdb_file_path,'rt') as f:
            model = pdb.PDBFile.read(f).get_structure(model=1)
    else:
        with open(pdb_file_path,'r') as f:
            model = pdb.PDBFile.read(f).get_structure(model=1)

    res = [amino2abv[i.res_name] for i in model if i.atom_name=="CA"]
    coord = [i.coord for i in model if i.atom_name=="CA"]
    
    atom_sasa = struc.sasa(model,vdw_radii="Single")
    sasa = struc.apply_residue_wise(model, atom_sasa, np.sum)

    app = dssp.DsspApp(model)
    app.start()
    app.join()
    sec = app.get_sse()
    return res,coord, sasa, sec


def get_feature(seq, sasa, sec):
    aminos = {i:idx for idx,i in enumerate('ARNDCQEGHILKMFPSTWYV')}
    sec2num = {i:idx for idx,i in enumerate("BCEGHIST")}

    seq_arr = np.array([aminos[i] for i in seq])
    sec_arr = np.array([sec2num[i] for i in sec])
    
    v_seq =  np.eye(20,dtype=np.float32)[seq_arr]
    v_sasa =  sasa.reshape(-1,1)/256
    v_sec = np.eye(8,dtype=np.float32)[sec_arr]
    #print(v_seq.shape,v_sasa.shape,v_sec.shape)
    v = np.hstack([v_seq,v_sasa,v_sec])
    return  sp.csr_matrix(v)


def get_adj(coord, threshold=9.5, max_length=None):
    """  normal adjacency of protein """
    distance_matrix =  LA.norm(np.array([i-coord  for i in coord]),axis=2)
    adj = np.array(distance_matrix < threshold,dtype=np.float32)
    adj = sp.csr_matrix(adj) 
    adj = normalize(adj)
    return adj

def get_rdist(coord, threshold=9.5, max_length=None):
    """  normal adjacency of protein """
    distance_matrix =  LA.norm(np.array([i-coord  for i in coord]),axis=2)
    d = distance_matrix + sp.eye(distance_matrix.shape[0],dtype=np.float32)
    rd = np.power(d,-1)
    rd[np.isinf(d)] = 0
    rd = np.multiply(rd,rd>1/threshold)
    rd = sp.csr_matrix(rd) 
    return rd

def pdb2graph(pdb_file=None, mode='rd', threshold=18, return_seq=False):
    """
    """
    seq, coord, sasa, sec  = get_coord_sasa_and_sec(pdb_file)
    feature = get_feature()

    if mode=='rd':
        adj = get_rdist(coord,threshold)
    else:
        adj = get_adj(coord,threshold)

    if return_seq == True:
        out = (feature,adj,seq)
    else:
        out = (feature,adj)
    return out


def normalize(mx):
    """Row-normalize sparse matrix"""
    rowsum = np.array(mx.sum(1))
    r_inv = np.power(rowsum, -1).flatten()
    r_inv[np.isinf(r_inv)] = 0.
    r_mat_inv = sp.diags(r_inv)
    mx = r_mat_inv.dot(mx)
    return mx


if __name__ == "__main__":
    pdb_file = "../../lib/pdb/AF-A0A0A7EPL0-F1-model_v2.pdb.gz"
    #seq, coord = get_seq_and_coord(pdb_file)
    
    feature,adj= pdb2graph(pdb_file)
    print("adj:\n",adj)
    print("feature:\n",feature)
    print(f"shape","adj:",adj.shape," feature:", feature.shape)
    import pickle
    with open("test.pkl","wb") as f:
        pickle.dump(adj,f)















#more info
    #'ASX':'B' represent Asp or Asn
    #'GLX':'Z' represent Glu or Gln
    #'XLE':'J' represent 
    #'XAA':'X' represent random
    #'PYL':'O' represent Pyrrolysine encoded by the 'amber' stop codon UAG)is an α-amino acid that is used in the biosynthesis of
    #proteins in some methanogenic archaea and bacteria;it is not present in humans
    #'SEC':'U' Selenocysteine (symbol Sec or U,[2] in older publications also as Se-Cys)[3] is the 21st proteinogenic amino acid


