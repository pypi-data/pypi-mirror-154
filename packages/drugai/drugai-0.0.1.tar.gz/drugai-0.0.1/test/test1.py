#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/10 23:15
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : test1.py

from rdkit import Chem
from rdkit.Chem.QED import qed
from rdkit.Chem import Descriptors
from rdkit.Chem.rdchem import Mol


mol:Mol = Chem.MolFromSmiles("CC1C2CCC(C2)C1CN(CCO)C(=O)c1ccc(Cl)cc1")
print(isinstance(mol, Mol))
print(qed(mol))

def logP(mol):
    """
    Computes RDKit's logP
    """
    return Chem.Crippen.MolLogP(mol)
print(logP((mol)))

def get_mol(smiles_or_mol):
    '''
    Loads SMILES/molecule into RDKit's object
    '''
    if isinstance(smiles_or_mol, str):
        if len(smiles_or_mol) == 0:
            return None
        mol = Chem.MolFromSmiles(smiles_or_mol) #将Smiles转换为mol对象
        if mol is None:
            return None
        try:
            Chem.SanitizeMol(mol) # 对分子进行检查
        except ValueError:
            return None
        return mol
    return smiles_or_mol

def canonic_smiles(smiles_or_mol):
    mol = get_mol(smiles_or_mol)
    if mol is None:
        return None
    return Chem.MolToSmiles(mol)

def weight(mol):
    """
    Computes molecular weight.
    Returns float,
    """
    return Descriptors.MolWt(mol)
print(weight(mol))