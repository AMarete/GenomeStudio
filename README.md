author: andrew.marete@canada.ca, (C), 2020

<b>Report2Plink:</b> is a function to convert GenomeStudio FinalReport and SNP Map to Plink ped/map. Report2Plink 
is written in Python 3.5, distributed 'as is' and can probably work on Linux-like machines including MacOS. To use [Report2Plink](https://github.com/AMarete/GenomeStudio/raw/main/report2plink), click on the link to download the standalone then change to executable: ```chmod a+x snprecode```; for full argument list run ```./report2plink -h```

basic usage:  
    
    ./report2plink -f [FinalReport.txt or .gz] -s [SNPMap.txt or .gz] -o [prefix]


![ ](https://github.com/AMarete/GenomeStudio/blob/main/data/Screen%20Shot%202020-10-14%20at%2010.28.03%20AM.png?raw=true)
