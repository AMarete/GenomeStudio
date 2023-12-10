#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from collections import defaultdict, Counter

# Author amarete@lactanet.ca; Nov/08/2023
# convert A/B to 012 similar to Store_seq_50K

genotype_mapping = {
    'AA': '2',
    'BB': '0',
    'BA': '1',
    'AB': '1',
    '00': '5',
    '0A': '5',
    '0B': '5',
    'A0': '5',
    'B0': '5'
}
reverse_geno_mapping = {value: key for key, value in genotype_mapping.items()}

store_seq_file = "/g1/programs/ge/src/is/Store_seq_50K.csv"
plink_map_file = sys.argv[1]    # "{main_path}Holstein.map"
plink_ped_file = sys.argv[2]    # f"{main_path}Holstein.ped"
output_file = sys.argv[3]       # f"{main_path}Holstein_012.csv"

store_seq_data = {}
with open(store_seq_file, 'r') as store_seq:
    for i, line in enumerate(store_seq):
        snp = line.strip().split(',')[1].strip()
        store_seq_data[snp] = i

plink_map_data = {}
with open(plink_map_file, 'r') as plink_map:
    for index, line in enumerate(plink_map, start=0):
        snp = line.strip().split()[1].strip()
        plink_map_data[snp] = index if index == 0 else index * 2

genotypes = {}
with open(plink_ped_file, 'r') as plink_ped:
    for animal_geno in [line.strip().split() for line in plink_ped]:
        genotypes[animal_geno[0]] = animal_geno[6:]

final = defaultdict(list)

check = {}
for iid, geno in genotypes.items():
    for snp, index in store_seq_data.items():
        try:
            mapped_value = genotype_mapping[geno[plink_map_data[snp]] + geno[plink_map_data[snp]+1]]
            try:
                check[index].append([mapped_value, geno[plink_map_data[snp]] + geno[plink_map_data[snp]+1]])
            except KeyError:
                check[index] = [[mapped_value, geno[plink_map_data[snp]] + geno[plink_map_data[snp] + 1]]]
        except KeyError:
            mapped_value = '5'
        final[iid].append([index, mapped_value])

for iid, geno_list in final.items():
    geno_list.sort(key=lambda x: int(x[0]))
    final[iid] = ''.join(sub_list[1] for sub_list in geno_list)

fin_len = []
with open(output_file, 'w') as output:
    for iid, genotype in final.items():
        fin_len.append(len(str(genotype)))
        output.write(','.join(str(i) for i in [iid, genotype]) + '\n')

snp_50k = len(set(store_seq_data.keys()))
snp_test = len(set(plink_map_data.keys()))
common_snp = len(set(plink_map_data.keys()) & set(store_seq_data.keys()))
final_snp = set(fin_len)


reverse_ss = {value: key for key, value in store_seq_data.items()}

def check_snps(check, reverse_geno_mapping, reverse_ss, logfile):
    with open(logfile, 'w') as file:
        file.write(''.join("SNP\tgeno012\tgenoAB\tcount012\tcountAB\tdiff\n"))

        for snp, values in check.items():
            geno_012 = Counter(item[0] for item in values)
            geno_AB = Counter(''.join(sorted(item[1])) for item in values)

            geno_012 = dict(sorted(geno_012.items(), key=lambda item: item[1], reverse=True))
            geno_AB = dict(sorted(geno_AB.items(), key=lambda item: item[1], reverse=True))

            for geno1, val_012 in geno_012.items():
                if reverse_geno_mapping[geno1] in geno_AB:
                    val_AB = geno_AB[reverse_geno_mapping[geno1]]
                    diff = val_012 - val_AB
                    file.write('\t'.join(str(i) for i in [reverse_ss[snp], geno1, reverse_geno_mapping[geno1],val_012,val_AB,diff])+ "\n")
                    if diff != 0:
                        print(f"Conversion may be irregular, check {reverse_ss[snp]}")

logfile = os.path.basename(sys.argv[0]).replace('.py', '') + '.log'
check_snps(check, reverse_geno_mapping, reverse_ss, logfile)


print(f"File Name            : SNP Count\n"
      f"{os.path.basename(store_seq_file):<20} : {snp_50k:,}\n"
      f"{os.path.basename(plink_map_file):<20} : {snp_test:,}\n"
      f"Common SNP           : {common_snp:,}\n"
      f"{os.path.basename(output_file):<20} : {int(list(final_snp)[0]):,}\n"
      f"Log file             : {os.path.basename(logfile)}\n")
