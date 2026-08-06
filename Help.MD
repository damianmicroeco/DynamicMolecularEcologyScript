# Help Page

This Markdown file will explain how different widgets work and provide an explanation of how to create new core widgets for customized workflows.

## Core Widgets

Core widgets are at the center of the program and are parts of pipelines we expect to be used most frequently. Please feel free to build your own customized widgets for specific, but frequent pipelines in your research program.

Some arguments are repeated across widgets and need to be changed/selected multiple times. This is by design. For instance, users will likely want to run jobs across many cores. However, some programs dramatically increase RAM when this occurs. Thus, by requiring users to specify the number of cores in multiple widgets, we provide users with the flexibility to limit RAM usage by some programs if their system is RAM-limited.

### Scheduler Widget
The Scheduler Widget generates a base file header for use with HPC schedulers (`Slurm` or `LSF`). When choosing `local` (e.g., a personal laptop), no scheduler headers are added.

This widget is effectively required for all jobs.

Widget arguments include:

1. `Scheduler Type` (drop-down): `Slurm`, `LSF`, or `local` depending on the system in which the job will be run.

2. `Run Time in Hours` (integer): This is how long you would like the script to run. We do not include a realistic default as in arguments for other widgets because this will vary tremendously based on features like which jobs are run, how many cores are used, the system on which the job is run, etc. If possible, please estimate required time based on similar jobs run in the past.

3. `Memory per CPU in GB` (integer; default: 4): This is the amount of working memory to be allocated for each CPU in the job. 

4. `Number of CPUs` (integer): Many HPC documentations often use the terms "CPU" and "node" interchangeably. Here, our terminology represents a hierarchical structure in which CPU is nested within node (i.e., one node has many CPUs). Please keep in mind that some HPC systems limit how many nodes are available within a "computer" and thus you may need to edit this header to run in parallel in certain systems.

5. `E-Mail` (text): The email address to which users want job statuses sent.

6. `Job Output File` (text): Name of the terminal output (i.e., `stdout`) file. This will be saved in the same directory in which the job is submitted to the scheduler.

7. `Read 1 or 2 Suffix` (text): The suffix in file names that distinguish between Read 1 and Read 2 in paired-end reads. For instance, in the files `14-008_S11_L001_R1_001.fastq.ora` and `14-008_S11_L001_R2_001.fastq.ora`, the read 1 and read 2 suffixes are `R1_001` and `R2_001`, respectively. 

### Sequence Processing

This widget processes raw sequencing data in `.ora` or `.fastq.gz` format through `FastQC` quality checks and basic soft-trimming through `TrimGalore`. Multi-sample processing is summarized through `MultiQC`. Please note that we recommend reviewing the `MultiQC` outputs after trimming if further trimming or sample exclusion need to occur.

Widget arguments include:

1. `Processing Mode` (drop-down): `ORAD` or `FASTQ`. `FASTQ` is most common, but some sequencing centers provide data in Illumina's `.ora` compressed format. The main difference between these two options is whether or not the user will need to include paths to the `ORAD` executable and the ORA reference (e.g., *Homo spaiens*, *Arabidopsis thaliana*, etc.)

2. `ORAD Executable` (path): File selection window to choose the ORAD executable from Illumina on your system.

3. `ORAD Reference` (path): Directory selection window to choose the species' oradata used to compress sequencing data. In our experience, this doesn't necessarily match your species of interest. For example, we have received sequencing data for a plant species that was compressed with human oradata.

4. `Sequencing Data` (path): Directory selection window to where the raw sequencing data is located.

5. `Project Directory` (path): Directory selection window to choose where project outputs are stored.

6. `Number of Cores` (integer): Many HPC documentations often use the terms "CPU" and "node" interchangeably. Here, our terminology represents a hierarchical structure in which CPU is nested within node (i.e., one node has many CPUs). Please keep in mind that some HPC systems limit how many nodes are available within a "computer" and thus you may need to edit this header to run in parallel in certain systems.

7. `Phred Score Cutoff` (integer; default: 20): Quality cut-off for soft-trimming of reads by `TrimGalore`. The default we have included is the program default and, in our experience, sufficient for most analyses.

### Aligner
This widget aligns short-read transcriptome (`STAR` mode) or short-read whole-genome (`bwa-mem2` mode) sequencing data processed through the Sequence Processing Widget. The goal of this widget is to align reads to a transcriptome or genome. While this script will run with no technical limitations here based on the completeness and intactness of a genome, we strongly recommend users limit their analyses to genomes/transcriptomes that are well-annotated and almost fully assembled (i.e., at least mostly chromosome-level scaffolds) otherwise users should proceed with caution.

Widget arguments include:

1. `Aligner` (drop-down): Choice of aligner. `STAR` aligns reads to a transcriptome and is splicing aware if users need this level of information. `bwa-mem2` aligns reads to a genome. Output from the `STAR` mode can be used for the Differential Expression and WGCNA widgets. Output from the `bwa-mem2` mode can be used for the Coverage, SNP Calling, SNP Filtering, SNP Imputation, GWAS, GEA, Bulked Segregant Analysis, and Population Genetics Widgets.

`STAR` mode

1. `Genome GTF file` (path): File selection window to a GTF file containing a genome annotation.

2. `SANIndex` (integer, default: 14): This is needed for generating the genome index. The actual value should be min(14, log2(GenomeLength)/2 - 1). We left the `STAR` default here, but you should calculate this value.

3. `Read Length - 1` (integer, default: 149): This is the length of your reads from the sequencer minus 1. This corresponds to the `--sjdbOverhang` kwarg to generate the genome index. We chose a default of 149 because, at this time, 150bp sequencing is the most commonly used in our lab. But, the default value of 100 in `STAR` is often good enough too.

4. `Genome FASTA file` (path): File selection window to a FASTA file containing the genome assembly with sequence headers matching the chromosome/scaffold names in the GTF file. 

5. `Number of Cores` (integer): Many HPC documentations often use the terms "CPU" and "node" interchangeably. Here, our terminology represents a hierarchical structure in which CPU is nested within node (i.e., one node has many CPUs). Please keep in mind that some HPC systems limit how many nodes are available within a "computer" and thus you may need to edit this header to run in parallel in certain systems.

6. `Project Directory` (path): Directory selection window to choose where project outputs are stored.

`bwa-mem2` mode

1. `BWA Prefix` (text, default: bwa_out): Folder/file prefixes for output from `bwa-mem2`.

2. `Genome FASTA File` (path): File selection window to a FASTA file containing the genome assembly with sequence headers matching the chromosome/scaffold names in the GTF file.

3. `Number of Cores` (integer): Many HPC documentations often use the terms "CPU" and "node" interchangeably. Here, our terminology represents a hierarchical structure in which CPU is nested within node (i.e., one node has many CPUs). Please keep in mind that some HPC systems limit how many nodes are available within a "computer" and thus you may need to edit this header to run in parallel in certain systems.

4. `Project Directory` (path): Directory selection window to choose where project outputs are stored.

### Differential Expression Widget

This script will run a differential expression analysis using `DESeq2` comparing differences between two groups. This script will output a volcano plot summarizing the differential expression analysis, a table of significantly differentially-expressed genes, and a table of the `DESeq2` analysis for all genes.

Widget arguments include:

1. `Project Directory` (path): Directory selection window to choose where project outputs are stored.

2. `Metadata` (((((((TBD)))))))

3. `Strand` (drop-down): This is based on the type of library preparation that was used to generate the transcriptome libraries.

4. `Delimiter` (drop-down): The delimiter used in the metadata file.

5. `Group 1 Name` (text): The name used for Group 1 in the metadata file.

6. `Group 2 Name` (text): The name used for Group 2 in the metadata file.

7. `Test Type` (drop-down): The desired test-statistic for calculating significance of differential expression.

8. `Alpha Cutoff` (float, default: 0.05): Alpha cut-off value to determine significance after False Discover Rate correction for multiple hypothesis testing.

9. `Group 1 Color Hexcde` (text, default: 415cc5): Color for plotting genes more highly expressed in Group 1.

10. `Group 2 Color Hexcde` (text, default: c5aa41): Color for plotting genes more highly expressed in Group 2.

11. `Output Directory` (path): Directory selection window to select/create directory where users would like to store output of this widget.

### Coverage Widget
The Coverage Widget calculates read depth across the genome at a set window size. This script will produce a coverage plot across the genome split by chromosome/scaffold. The R script to generate the images is available in the `modules` folder if the user would like to replicate the image while removing non-chromosome scaffolds.

Widget arguments include:

1. `Project Directory` (path): Directory selection window to choose where project outputs are stored.

2. `Genome GTF file` (path): File selection window to a GTF file containing a genome annotation.

3. `Number of Cores` (integer): Many HPC documentations often use the terms "CPU" and "node" interchangeably. Here, our terminology represents a hierarchical structure in which CPU is nested within node (i.e., one node has many CPUs). Please keep in mind that some HPC systems limit how many nodes are available within a "computer" and thus you may need to edit this header to run in parallel in certain systems.

4. `Window Size (bp)` (integer, default: 100): Desired window size for calculating read depth across at locations across the genome.

5. `Quality` (integer, default: 30): Quality score for reads that reads must meet/surpass to be included.

6. `Output Directory` (path): Directory selection window to select/create directory where users would like to store output of this widget.

## Glossary
