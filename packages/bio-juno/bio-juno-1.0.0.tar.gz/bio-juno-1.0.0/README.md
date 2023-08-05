# Juno: read data generator  

Juno have two methods to generate reads fastq.  
1. Download the real fastq submitted to NCBI SRA from the contributors
2. Simulate the "fake" fastq   

If you want to develope genomic tools but has no real data, juno can generate the read fastq for your testing.

Juno is also available as a public online resource: https://juno.hlin.tw

## Requirements  
- Linux 
- Python >= 3.6
 
## Installation  

### Pypi version 
https://pypi.org/project/juno/
```
pip install juno
```

### Intall from source  

```
git clone https://github.com/hunglin59638/juno.git
cd juno
python3 setup.py install
```

### Docker version
`/data` is the entry point 
```
docker pull hunglin59638/juno:1.0.0
docker run --rm -v /your/mount/point:/data juno sra -a $RUN_ACCESSION -o /data/outdir
```

## CLI  
```
juno -h 
usage: juno [-h] SUBCOMMAND ...

Juno: read data generator

optional arguments:
  -h, --help  show this help message and exit

subcommands:
  subcommands

  SUBCOMMAND
    sra       Download reads from SRA database
    simulate  Simulating reads by reference genome
```
### Download reads from SRA database  
```
juno sra -a SRR19400588 -o /path/to/directory
```

### Simulate reads fastq  
There are two way to simulate read fastq    
1. Input your genome fasta
```
juno simulate -r /your/genome/fasta -o /path/to/directory --compressed --depth 200
```
2. Input RefSeq assembly accession and its genome will be downloaded from NCBI
```
juno simulate -a GCF_002004995.1 -o /path/to/directory --compressed --depth 200
```
Tips:
depth is greater than 200x is the better parameter for bacteria

### Update local NCBI RefSeq assembly summary  
```
juno simulate --update
```

## Python API

### Use Case 1: Update NCBI RefSeq Assembly Summary and get it in local 

```
from juno.data import Assembly
assembly = Assembly()
assembly.update_assembly()
df = assembly.dataframe
df.head()
```
```
	assembly_accession	bioproject	biosample	wgs_master	refseq_category	taxid	species_taxid	organism_name	infraspecific_name	isolate	version_status	assembly_level	release_type	genome_rep	seq_rel_date	asm_name	submitter	gbrs_paired_asm
0	GCF_000001215.4	PRJNA164	SAMN02803731		reference genome	7227	7227	Drosophila melanogaster			latest	Chromosome	Major	Full	2014/08/01	Release 6 plus ISO1 MT	The FlyBase Consortium/Berkeley Drosophila Genome Project/Celera Genomics	GCA_000001215.4
1	GCF_000001405.40	PRJNA168			reference genome	9606	9606	Homo sapiens			latest	Chromosome	Patch	Full	2022/02/03	GRCh38.p14	Genome Reference Consortium	GCA_000001405.29
2	GCF_000001635.27	PRJNA169			reference genome	10090	10090	Mus musculus			latest	Chromosome	Major	Full	2020/06/24	GRCm39	Genome Reference Consortium	GCA_000001635.9
3	GCF_000001735.4	PRJNA116	SAMN03081427		reference genome	3702	3702	Arabidopsis thaliana	ecotype=Columbia		latest	Chromosome	Minor	Full	2018/03/15	TAIR10.1	The Arabidopsis Information Resource (TAIR)	GCA_000001735.2
4	GCF_000001905.1	PRJNA70973	SAMN02953622	AAGU00000000.3	representative genome	9785	9785	Loxodonta africana		ISIS603380	latest	Scaffold	Major	Full	2009/07/15	Loxafr3.0	Broad Institute	GCA_000001905.1

```

### Use Case 2: Download assembly genome  
```
from juno.data import Assembly
assembly = Assembly()
genome_path = assembly.download("GCF_002004995.1", "/your/output/directory")
```
### Use Case 3: Simulate reads from genome reference  
```
from juno.simulator import Simulator
sm = Simulator()
sm.generate(reference="/your/genome/fasta/path", out_dir="/your/output/directory", depth=200.0, platform="nanopore", compressed=True)
```
tips:
The genome fasta is supported by gz format. 

## Citation

- pysradb: A Python package to query next-generation sequencing metadata and data from NCBI Sequence Read Archive (https://f1000research.com/articles/8-532/v1)  
- PBSIM2: a simulator for long-read sequencers with a novel generative model of quality scores (https://doi.org/10.1093/bioinformatics/btaa835)
