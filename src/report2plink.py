import timeit
from fxns import error, open_by_suffix
from parser_handler import ArgumentParser

start = timeit.default_timer()
print("""
Andrew Marete (C) 2016
This function converts an Illumina GenomeStudio Report to Plink Ped/Map format
This version supports conversion of Forward/Reverse strand i.e. `Allele1 - Forward` and  `Allele2 - Forward`
""")

parser = ArgumentParser()
parser.add_argument("-r", "--report", help="GenomeStudio FinalReport.txt", action="store", metavar="\b")
parser.add_argument("-m", "--marker", help="GenomeStudio SNP file", action="store", metavar="\b")
parser.add_argument("-p", "--prefix", help="Output prefix", action="store", metavar="\b")
args = parser.parse_args()

final_report = open_by_suffix(args.report)
marker_file = open_by_suffix(args.marker)
file_out = args.prefix

outped = open(file_out + '.ped', 'w')
outmap = open(file_out + '.map', 'w')
allele = "Forward"
start_line = False
c = 0
snp_count = 0
snp_name = []
ss = -1

for en, a in enumerate(final_report):
    if 'SNP Name' in a:
        start_line = True
        line = a.lower().strip().split('\t')
        if 'allele1 - ' + allele.lower() not in line:
            error(f'''The header does not contain the required field: `Allele1 - {allele}`''')
        continue
    if not start_line:
        continue
    snp, sample, a1, a2, other = a.strip().split('\t', 4)
    if a1 == '-':
        a1 = '0'
    if a2 == '-':
        a2 = '0'
    c += 1
    if c == 1:
        snp_count = -1
        geno = []
        name = [sample]
    if sample in name:
        geno.append(a1 + ' ' + a2)
        snp_count += 1
        if len(name) == 1:
            snp_name.append(snp)
        elif snp != snp_name[snp_count]:
            error(f'''SNP order inconsistent. Check {snp} and {snp_name[snp_count]}
       try sort by sample ID then SNP Name''')
    else:
        snp_count = 0
        ss += 1
        outped.write('%s %s 0 0 0 -9 %s\n' % (name[ss], name[ss], ' '.join(geno)))
        print(f'Finished processing sample: {name[ss]} - Total SNPs: {len(geno)}')
        geno = [a1 + ' ' + a2]
        name.append(sample)

outped.write('%s %s 0 0 0 -9 %s\n' % (sample, sample, ' '.join(geno)))
ss += 2
print(f'''Finished processing sample: {sample} - Total SNPs: {len(geno)}
...Total number of samples processed: {ss}
...Processing marker file''')

final_report.close()

markers = {}
with marker_file as f:
    next(f)
    for line in f:
        index, snp, chrom, pos, other = line.strip().split('\t', 4)
        markers[snp] = (chrom, pos)
print(f'''...Total number of SNPs processed: {len(markers)}
...Checking SNP id in ped file''')
for x in snp_name:
    if x not in markers:
        error(f'''SNP: {x} in FinalReport is not present in SNP map''')
    outmap.write('%s %s 0 %s\n' % (markers[x][0], x, markers[x][1]))

stop = timeit.default_timer()
mins, secs = divmod(stop - start, 60)
hours, mins = divmod(mins, 60)

print(f'''...Success! All SNP in map file also present in ped file
...ped file: {file_out}.ped
...map file: {file_out}.map
Conversion Time: {hours}hrs {mins}mins {secs}secs
''')