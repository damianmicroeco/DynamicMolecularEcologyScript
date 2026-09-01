#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from fields import (
    text,
    integer,
    floating,
    combo,
    path,
    spreadsheet,
    visible_when,
    checkbox,
)

from widget_base import WidgetItem

import csv

# ----------------------------------------------------------------------
# Scheduler
# ----------------------------------------------------------------------

class ScheduleSystem(WidgetItem):

    TYPE = "scheduler"
    TITLE = "Scheduler"

    HELP_TEXT = """
    The Scheduler Widget generates a base file header for use
    with HPC schedulers (`Slurm` or `LSF`). When choosing `local`
    (e.g., a personal laptop), no scheduler headers are added."
        
    This widget is effectively required for all jobs.
    """

    TEMPLATE = "ScheduleSystem/{{SCHEDULER}}.txt"

    FIELDS = [

        combo(
            "Scheduler Type",
            [
                "Slurm",
                "LSF",
                "Local",
            ],
            template="SCHEDULER",
            default="Slurm",
            help_text= (
                "(drop-down)\n"
                "`Slurm`, `LSF`, or `local` depending on the system in which the job will be run."
            ) 
        ),

        integer(
            "Run Time in Hours",
            template="HOURS",
            minimum=1,
            maximum=999,
            default=1,
            help_text=(
                    "(integer)\n"
                    "This is how long you would like the script to run. We do not "
                    "include a realistic default as in arguments for other widgets "
                    "because this will vary tremendously based on features like "
                    "which jobs are run, how many cores are used, the system on "
                    "which the job is run, etc. If possible, please estimate required "
                    "time based on similar jobs run in the past."
            ),
        ),

        integer(
            "Memory per CPU in GB",
            template="MEMORY",
            minimum=1,
            maximum=4096,
            default=4,
            help_text=(
                    "(integer; default: 4)\n"
                    "This is the amount of working memory to be allocated for each CPU in the job."
            ),
        ),

        integer(
            "Number of CPUs",
            template="CPUS",
            minimum=1,
            maximum=512,
            default=1,
            help_text=(
                    "(integer)\n"
                    "Many HPC documentations often use the terms 'CPU' and 'node' "
                    "interchangeably. Here, our terminology represents a hierarchical "
                    "structure in which CPU is nested within node (i.e., one node has "
                    "many CPUs). Please keep in mind that some HPC systems limit how many "
                    "nodes are available within a 'computer' and thus you may need to edit "
                    "this header to run in parallel in certain systems."
            ),
        ),

        text(
            "E-Mail",
            template="EMAIL",
            help_text=(
                    "(text)\n"
                    "The email address to which users want job statuses sent."
            ),
        ),

        text(
            "Job Output File",
            template="OUTPUT",
            help_text=(
                    "(text)\n"
                    "Name of the terminal output (i.e., `stdout`) file. This "
                    "will be saved in the same directory in which the job is "
                    "submitted to the scheduler."
            ),
        ),

        text(
            "Read 1 Suffix",
            template="READ1SUFFIX",
            help_text=(
                    "(text)\n"
                    "The suffix in file names that distinguish between Read 1 "
                    "and Read 2 in paired-end reads. For instance, in the "
                    "files `14-008_S11_L001_R1_001.fastq.ora` and "
                    "`14-008_S11_L001_R2_001.fastq.ora`, the read 1 and read 2 "
                    "suffixes are `R1_001` and `R2_001`, respectively."
            ),
        ),

        text(
            "Read 2 Suffix",
            template="READ2SUFFIX",
            help_text=(
                    "(text)\n"
                    "The suffix in file names that distinguish between Read 1 "
                    "and Read 2 in paired-end reads. For instance, in the "
                    "files `14-008_S11_L001_R1_001.fastq.ora` and "
                    "`14-008_S11_L001_R2_001.fastq.ora`, the read 1 and read 2 "
                    "suffixes are `R1_001` and `R2_001`, respectively."
            ),
        ),
    ]

    def get_template_context(self):

        context = super().get_template_context()

        context["SCHEDULER"] = (
            context["SCHEDULER"]
            .lower()
        )

        return context


# ----------------------------------------------------------------------
# Sequence Processing
# ----------------------------------------------------------------------

class SequenceProcessor(WidgetItem):

    TYPE = "sequence_processing"
    TITLE = "Sequence Processing"

    HELP_TEXT = """
    This widget processes raw sequencing data in `.ora` or `.fastq.gz` format 
    through `FastQC` quality checks and basic soft-trimming through `TrimGalore`. 
    Multi-sample processing is summarized through `MultiQC`. Please note that we 
    recommend reviewing the `MultiQC` outputs after trimming if further trimming 
    or sample exclusion need to occur.
    """

    TEMPLATE = (
        "SequenceProcessing/"
        "{{MODE}}_processing.txt"
    )

    FIELDS = [

        combo(
            "Processing Mode",
            [
                "ORAD",
                "FASTQ",
            ],
            template="MODE",
            default="ORAD",
            help_text=(
                    "(drop-down)\n"
                    "`ORAD` or `FASTQ`. `FASTQ` is most common, but some "
                    "sequencing centers provide data in Illumina's `.ora` "
                    "compressed format. The main difference between these "
                    "two options is whether or not the user will need to "
                    "include paths to the `ORAD` executable and the ORA "
                    "reference (e.g., *Homo spaiens*, *Arabidopsis thaliana*, "
                    "etc.)"
            ),
        ),

        visible_when(
            path(
                "ORAD Executable",
                template="ORAD_EXECUTABLE",
                mode="file",
                help_text=(
                    "(path)\n"
                    "File selection window to choose the ORAD executable from Illumina on your system."
                ),
            ),
            "Processing Mode",
            "ORAD",
        ),

        visible_when(
            path(
                "ORAD Reference",
                template="ORAD_REFERENCE",
                mode="directory",
                help_text=(
                    "(path)\n"
                    "Directory selection window to choose the species' "
                    "oradata used to compress sequencing data. In our "
                    "experience, this doesn't necessarily match your species "
                    "of interest. For example, we have received sequencing "
                    "data for a plant species that was compressed with human "
                    "oradata."
                ),
            ),
            "Processing Mode",
            "ORAD",
        ),

        path(
            "Sequencing Data",
            template="SEQUENCING_DATA",
            mode="directory",
            help_text=(
                    "(path)\n"
                    "Directory selection window to where the raw sequencing data is located."
            ),
        ),

        path(
            "Project Directory",
            template="FASTQ_OUTPUT_DIR",
            mode="directory",
            help_text=(
                    "(path)\n"
                    "Directory selection window to choose where project outputs are stored"
            ),
        ),

        integer(
            "Number of Cores",
            template="CORES",
            minimum=1,
            maximum=512,
            default=1,
            help_text=(
                    "(integer)\n"
                    "Many HPC documentations often use the terms 'CPU' and 'node' "
                    "interchangeably. Here, our terminology represents a hierarchical "
                    "structure in which CPU is nested within node (i.e., one node has "
                    "many CPUs). Please keep in mind that some HPC systems limit how many "
                    "nodes are available within a 'computer' and thus you may need to edit "
                    "the script header to run in parallel in certain systems."
            ),
        ),

        integer(
            "Phred Score Cutoff",
            template="PHRED",
            minimum=0,
            maximum=50,
            default=20,
            help_text=(
                    "(integer; default: 20)\n"
                    "Quality cut-off for soft-trimming of reads by `TrimGalore`. "
                    "The default we have included is the program default and, "
                    "in our experience, sufficient for most analyses."
            ),
        ),
    ]

    def get_template_context(self):

        context = super().get_template_context()

        context["MODE"] = (
            context["MODE"]
            .lower()
        )

        context["APPTAINER_DIR"] = str(
            Path(__file__).parent /
            "apptainers"
        )

        return context


# ----------------------------------------------------------------------
# Aligner
# ----------------------------------------------------------------------

class Aligner(WidgetItem):

    TYPE = "aligner"
    TITLE = "Aligner"

    HELP_TEXT = """
    This widget aligns short-read transcriptome (`STAR` mode) or 
    short-read whole-genome (`bwa-mem2` mode) sequencing data processed 
    through the Sequence Processing Widget. The goal of this widget is 
    to align reads to a transcriptome or genome. While this script will 
    run with no technical limitations here based on the completeness and 
    intactness of a genome, we strongly recommend users limit their analyses 
    to genomes/transcriptomes that are well-annotated and almost fully 
    assembled (i.e., at least mostly chromosome-level scaffolds) otherwise 
    users should proceed with caution.
    """
    
    TEMPLATE = (
        "Aligner/"
        "{{MODE}}.txt"
    )

    FIELDS = [

        combo(
            "Aligner",
            [
                "STAR",
                "bwa-mem2",
            ],
            template="MODE",
            default="STAR",
            help_text=(
                    "(drop-down)\n"
                    "Choice of aligner. `STAR` aligns reads to a "
                    "transcriptome and is splicing aware if users "
                    "need this level of information. `bwa-mem2` "
                    "aligns reads to a genome. Output from the `STAR` "
                    "mode can be used for the Differential Expression "
                    "and WGCNA widgets. Output from the `bwa-mem2` mode "
                    "can be used for the Coverage, SNP Calling, "
                    "SNP Filtering, SNP Imputation, GWAS, GEA, "
                    "Bulked Segregant Analysis, and Population Genetics Widgets."
            ),
        ),

        visible_when(
            path(
                "Genome GTF file",
                template="GTF",
                mode="file",
                help_text=(
                        "(path)\n"
                        "File selection window to a GTF file containing a genome annotation."
                ),
            ),
            "Aligner",
            "STAR",
        ),

        visible_when(
            integer(
                "SANIndex",
                template="SANINDEX",
                minimum=1,
                maximum=20,
                default=14,
                help_text=(
                        "(integer; default: 14)\n"
                        "This is needed for generating the genome index. "
                        "The actual value should be min(14, log2(GenomeLength)/2 - 1). "
                        "We left the `STAR` default here, but you should calculate "
                        "this value."
                ),
            ),
            "Aligner",
            "STAR",
        ),

        visible_when(
            integer(
                "Read Length - 1",
                template="RLENGTH",
                minimum=1,
                maximum=300,
                default=149,
                help_text=(
                        "(integer; default: 149)\n"
                        "This is the length of your reads from the sequencer "
                        "minus 1. This corresponds to the `--sjdbOverhang` kwarg "
                        "to generate the genome index. We chose a default of 149 "
                        "because, at this time, 150bp sequencing is the most "
                        "commonly used in our lab. But, the default value of 100 "
                        "in `STAR` is often good enough too."
                ),
            ),
            "Aligner",
            "STAR",
        ),

        visible_when(
            text(
                "BWA Prefix",
                template="BWA_PREFIX",
                default="bwa_out",
                help_text=(
                        "(text; default: bwa_out)\n"
                        "Folder/file prefixes for output from `bwa-mem2`."
                ),
            ),
            "Aligner",
            "bwa-mem2",
        ),

        path(
            "Genome Fasta File",
            template="GEN_FASTA",
            mode="file",
            help_text=(
                    "(path)\n"
                    "File selection window to a FASTA file containing "
                    "the genome assembly with sequence headers matching "
                    "the chromosome/scaffold names in the GTF file."
            ),
        ),

        integer(
            "Number of Cores",
            template="CORES",
            minimum=1,
            maximum=512,
            default=1,
            help_text=(
                    "(integer)\n"
                    "Many HPC documentations often use the terms 'CPU' and 'node' "
                    "interchangeably. Here, our terminology represents a hierarchical "
                    "structure in which CPU is nested within node (i.e., one node has "
                    "many CPUs). Please keep in mind that some HPC systems limit how many "
                    "nodes are available within a 'computer' and thus you may need to edit "
                    "the script header to run in parallel in certain systems."
            ),
        ),

        path(
            "Project Directory",
            template="PROJECTDIR",
            mode="directory",
            help_text=(
                    "(path)\n"
                    "Directory selection window to choose where project outputs are stored."
            ),
        ),
    ]

    def get_template_context(self):

        context = super().get_template_context()

        context["MODE"] = (
            context["MODE"]
            .lower()
        )

        context["APPTAINER_DIR"] = str(
            Path(__file__).parent /
            "apptainers"
        )

        return context

# ----------------------------------------------------------------------
# Differential Expression
# ----------------------------------------------------------------------

class DifferentialExpression(WidgetItem):

    TYPE = "deseq"
    TITLE = "Differential Expression"

    HELP_TEXT = """
    This script will run a differential expression analysis using `DESeq2` 
    comparing differences between two groups. This script will output a 
    volcano plot summarizing the differential expression analysis, a table 
    of significantly differentially-expressed genes, and a table of the 
    `DESeq2` analysis for all genes.
    """

    TEMPLATE = "DifferentialExpression/DESeq2.txt"

    FIELDS = [

        path(
            "Project Directory",
            template="PROJECTDIR",
            mode="directory",
            help_text=(
                    "(path)\n"
                    "Directory selection window to choose where project outputs are stored."
            ),
        ),

        spreadsheet(
            "Metadata",
            template="METADATA",
            columns=[
                "sample_name",
                "group_id",
            ],
            rows=3,
            help_text=(
                "Paste spreadsheet data of your sample metadata here or "
                "import a CSV file. The first column should be your sample names "
                "without special characters and the second column the group name "
                "without special characters. By sample names, we explicitly mean "
                "your read file names without the read 1 suffix. For example: "
                "`14-008_S11_L001_R1_001.fastq.ora` read 1 suffix is `14-008_S11_L001`."
            ),
        ),

        text(
            "Read 1 Suffix",
            template="READ1SUFFIX",
            help_text=(
                    "(text)\n"
                    "The suffix in file names that distinguish between Read 1 "
                    "and Read 2 in paired-end reads. For instance, in the "
                    "files `14-008_S11_L001_R1_001.fastq.ora` and "
                    "`14-008_S11_L001_R2_001.fastq.ora`, the read 1 and read 2 "
                    "suffixes are `R1_001` and `R2_001`, respectively."
            ),
        ),

        combo(
            "Strand",
            [
                "Unstranded",
                "Forward-Stranded",
                "Reverse-Stranded",
            ],
            template="STRAND",
            default="Unstranded",
            help_text=(
                    "(drop-down)\n"
                    "This is based on the type of library preparation that "
                    "was used to generate the transcriptome libraries."
            ),
        ),

        text(
            "Group 1 Name",
            template="GROUP1",
            help_text=(
                    "(text)\n"
                    "The name used for Group 1 in the metadata file."
            ),
        ),

        text(
            "Group 2 Name",
            template="GROUP2",
            help_text=(
                    "(text)\n"
                    "The name used for Group 2 in the metadata file."
            ),
        ),

        combo(
            "Test Type",
            [
                "Wald",
                "LRT",
            ],
            template="TESTTYPE",
            default="Wald",
            help_text=(
                    "(drop-down)\n"
                    "The desired test-statistic for calculating significance of differential expression."
            ),
        ),

        floating(
            "Alpha Cutoff",
            template="CUTOFF",
            minimum=0,
            maximum=0.5,
            default=0.05,
            decimals=5,
            step=0.001,
            help_text=(
                    "(float, default: 0.05)\n"
                    "Alpha cut-off value to determine significance after "
                    "False Discover Rate correction for multiple hypothesis "
                    "testing."
            ),
        ),

        text(
            "Group 1 Color Hexcode",
            template="PALETTE1",
            default="415cc5",
            help_text=(
                    "(text, default: 415cc5)\n"
                    "Color for plotting genes more highly expressed in Group 1."
            ),
        ),

        text(
            "Group 2 Color Hexcode",
            template="PALETTE2",
            default="c5aa41",
            help_text=(
                    "(text, default: c5aa41)\n"
                    "Color for plotting genes more highly expressed in Group 2."
            ),
        ),

        path(
            "Output Directory",
            template="OUTPUT_DIR",
            mode="directory",
            help_text=(
                    "(path)\n"
                    "Directory selection window to select/create directory "
                    "where users would like to store output of this widget."
            ),
        ),
    ]

    def prepare_files(self, output_directory):

        output_directory = Path(
            output_directory
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        metadata_field = self.field(
            "Metadata"
        )

        metadata_file = (
            output_directory / "metadata.csv"
        )

        with metadata_file.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as handle:

            writer = csv.writer(handle)

            writer.writerow(
                metadata_field.columns
            )

            writer.writerows(
                metadata_field.value()
            )

        return {
            "METADATA_FILE": str(metadata_file)
        }


    def get_template_context(self):

        context = super().get_template_context()

        context["APPTAINER_DIR"] = str(
            Path(__file__).parent /
            "apptainers"
        )

        context["TEMPLATE_DIR"] = str(
            Path(__file__).parent /
            "module_templates"
        )

        return context

# ----------------------------------------------------------------------
# Coverage
# ----------------------------------------------------------------------

class Coverage(WidgetItem):

    TYPE = "coverage"
    TITLE = "Coverage"

    TEMPLATE = "Coverage/coverage.txt"

    FIELDS = [

        path(
            "Project Directory",
            template="PROJECTDIR",
            mode="directory",
            help_text=(
                    "(path)\n"
                    "Directory selection window to choose where project outputs are stored."
            ),
        ),

        path(
            "Genome GTF file",
            template="GTF",
            mode="file",
            help_text=(
                    "(path)\n"
                    "File selection window to a GTF file containing a genome annotation."
            ),
        ),

        integer(
            "Number of Cores",
            template="CORES",
            minimum=1,
            maximum=512,
            default=1,
            help_text=(
                    "(integer)\n"
                    "Many HPC documentations often use the terms 'CPU' and 'node' "
                    "interchangeably. Here, our terminology represents a hierarchical "
                    "structure in which CPU is nested within node (i.e., one node has "
                    "many CPUs). Please keep in mind that some HPC systems limit how many "
                    "nodes are available within a 'computer' and thus you may need to edit "
                    "the script header to run in parallel in certain systems."
            ),
        ),

        integer(
            "Window Size (bp)",
            template="WINDOWSIZE",
            minimum=1,
            maximum=100000,
            default=100,
            help_text=(
                    "(integer, default: 100)\n"
                    "Size of window in which to calculate coverage in base pairs."
            ),
        ),

        integer(
            "Quality",
            template="QUALITY",
            minimum=1,
            maximum=60,
            default=30,
            help_text=(
                    "(integer; default: 30)\n"
                    "Quality cut-off for including reads in coverage calculation."
            ),
        ),

        path(
            "Output Directory",
            template="OUTPUT_DIR",
            mode="directory",
            help_text=(
                    "(path)\n"
                    "Directory selection window to select/create directory "
                    "where users would like to store output of this widget."
            ),
        ),
    ]

    def get_template_context(self):

        context = super().get_template_context()

        context["APPTAINER_DIR"] = str(
            Path(__file__).parent /
            "apptainers"
        )

        context["TEMPLATE_DIR"] = str(
            Path(__file__).parent /
            "module_templates"
        )

        return context

# ----------------------------------------------------------------------
# SNP Calling
# ----------------------------------------------------------------------

class SNPCalling(WidgetItem):

    TYPE = "snp_calling"
    TITLE = "SNP Calling"

    TEMPLATE = (
        "SNPCalling/"
        "{{MODE}}.txt"
    )

    FIELDS = [

        combo(
            "Processing Mode",
            [
                "GATK (Few)",
                "GATK (Many)",
                "bcftools mpileup",
            ],
            template="MODE",
            default="bcftools mpileup",
        ),

        path(
            "Project Directory",
            template="PROJECTDIR",
            mode="directory",
            help_text=(
                    "(path)\n"
                    "Directory selection window to choose where project outputs are stored."
            ),
        ),
        
        path(
            "Reference Genome",
            template="REFGENOME",
            mode="file",
            help_text=(
                    "(path)\n"
                    "File selection window to a FASTA file containing "
                    "the genome assembly with sequence headers matching "
                    "the chromosome/scaffold names in the GTF file."
            ),
        ),

        integer(
            "Number of Cores",
            template="CORES",
            minimum=1,
            maximum=512,
            default=1,
            help_text=(
                    "(integer)\n"
                    "Many HPC documentations often use the terms 'CPU' and 'node' "
                    "interchangeably. Here, our terminology represents a hierarchical "
                    "structure in which CPU is nested within node (i.e., one node has "
                    "many CPUs). Please keep in mind that some HPC systems limit how many "
                    "nodes are available within a 'computer' and thus you may need to edit "
                    "the script header to run in parallel in certain systems."
            ),
        ),

        visible_when(
            integer(
                "Max RAM in GB",
                template="MAXRAM",
                minimum=0,
                maximum=100000,
                default=160,
                help_text=(
                    "(integer)\n"
                    "Maximum amount of RAM (GB) to be used for GATK. "
                    "You should drop the RAM usage to about 4-8 GB lower than allocated to your "
                    "whole job because the JAVA virtual machine running GATK needs "
                    "a little bit of overhead for certain processes other than the analysis."
                )
                ),
            "Processing Mode",
            "GATK (Few)",
        ),

        visible_when(
            integer(
                "Max RAM in GB",
                template="MAXRAM",
                minimum=0,
                maximum=100000,
                default=160,
                help_text=(
                    "(integer)\n"
                    "Maximum amount of RAM (GB) to be used for GATK. "
                    "You should drop the RAM usage to about 4-8 GB lower than allocated to your "
                    "whole job because the JAVA virtual machine running GATK needs "
                    "a little bit of overhead for certain processes other than the analysis."
                )
                ),
            "Processing Mode",
            "GATK (Many)",
        ),
    ]

    def get_template_context(self):

        context = super().get_template_context()

        context["MODE"] = (
            context["MODE"]
            .lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
        )

        context["APPTAINER_DIR"] = str(
            Path(__file__).parent /
            "apptainers"
        )

        return context

# ----------------------------------------------------------------------
# SNP Filtering (Pre-Imputation)
# ----------------------------------------------------------------------

class SNPFilteringPreImputation(WidgetItem):

    TYPE = "snp_filtering_preimputation"
    TITLE = "SNP Filtering (Pre-Imputation)"

    TEMPLATE = "SNPFilteringPreImputation/snp_filtering.txt"

    FIELDS = [

        path(
            "Project Directory",
            template="PROJECTDIR",
            mode="directory",
            help_text=(
                    "(path)\n"
                    "Directory selection window to choose where project outputs are stored."
            ),
        ),

        integer(
            "Number of Cores",
            template="CORES",
            minimum=1,
            maximum=512,
            default=1,
            help_text=(
                    "(integer)\n"
                    "Many HPC documentations often use the terms 'CPU' and 'node' "
                    "interchangeably. Here, our terminology represents a hierarchical "
                    "structure in which CPU is nested within node (i.e., one node has "
                    "many CPUs). Please keep in mind that some HPC systems limit how many "
                    "nodes are available within a 'computer' and thus you may need to edit "
                    "the script header to run in parallel in certain systems."
            ),
        ),

        integer(
            "DP<N (Depth Threshold)",
            template="DP",
            minimum=1,
            maximum=999,
            default=5,
            help_text=(
                    "(integer, default: 5)\n"
                    "Minimum depth at SNP site to be included in final VCF."
            ),
        ),

        integer(
            "GQ<N (Genotype Quality Threshold)",
            template="GQ",
            minimum=1,
            maximum=99,
            default=20,
            help_text=(
                    "(integer, default: 20)\n"
                    "Minimum genotype quality at SNP site to be included in final VCF."
            ),
        ),
        
        integer(
            "QUAL>=N (Variant Level Quality Threshold)",
            template="QUAL",
            minimum=1,
            maximum=99,
            default=30,
            help_text=(
                    "(integer, default: 5)\n"
                    "Minimum variant level quality at SNP site to be included in final VCF."
            ),
        ),

        integer(
            "MAC>N (Minor Allele Count Threshold)",
            template="MAC",
            minimum=1,
            maximum=999,
            default=1,
            help_text=(
                    "(integer)\n"
                    "Minimum minor allele count at SNP site to be included in final VCF."
            ),
        ),

        floating(
            "F_MISSING<=N (Site Level Missingness Threshold)",
            template="F_MISSING",
            minimum=0,
            maximum=1,
            default=0.10,
            decimals=5,
            step=0.001,
            help_text=(
                    "(float, default: 0.10)\n"
                    "Maximum frequency of missing genotypes at SNP site to be included in final VCF."
            ),
        ),
    ]

    def get_template_context(self):

        context = super().get_template_context()

        context["APPTAINER_DIR"] = str(
            Path(__file__).parent /
            "apptainers"
        )

        context["TEMPLATE_DIR"] = str(
            Path(__file__).parent /
            "module_templates"
        )

        return context

# ----------------------------------------------------------------------
# SNP Imputation
# ----------------------------------------------------------------------

class SNPImputation(WidgetItem):

    TYPE = "snp_imputation"
    TITLE = "SNP Imputation"

    TEMPLATE = "SNPImputation/snp_imputation.txt"

    FIELDS = [

        path(
            "Project Directory",
            template="PROJECTDIR",
            mode="directory",
            help_text=(
                    "(path)\n"
                    "Directory selection window to choose where project outputs are stored."
            ),
        ),

        integer(
            "Number of Cores",
            template="CORES",
            minimum=1,
            maximum=512,
            default=1,
            help_text=(
                    "(integer)\n"
                    "Many HPC documentations often use the terms 'CPU' and 'node' "
                    "interchangeably. Here, our terminology represents a hierarchical "
                    "structure in which CPU is nested within node (i.e., one node has "
                    "many CPUs). Please keep in mind that some HPC systems limit how many "
                    "nodes are available within a 'computer' and thus you may need to edit "
                    "the script header to run in parallel in certain systems."
            ),
        ),
    ]

    def get_template_context(self):

        context = super().get_template_context()

        context["APPTAINER_DIR"] = str(
            Path(__file__).parent /
            "apptainers"
        )

        context["TEMPLATE_DIR"] = str(
            Path(__file__).parent /
            "module_templates"
        )

        return context

class BulkedSegregantAnalysis(WidgetItem):

    TYPE = "bsa"
    TITLE = "Bulked Segregant Analysis"

    HELP_TEXT = """
    This script will run a bulked segregant analysis using `QTLSeqR`
    comparing SNP differences between a high and low group. Please 
    note that SNP calling is called separately for a BSA than for 
    the other population genetic analysis widgets (i.e., the inputs 
    are the analysis ready bam files from the Aligner widget) because 
    statistics like G' are highly sensitive to uneven library sizes. 
    Thus we need to do subsampling to equalize libraries before 
    calling variants. 
    """

    TEMPLATE = "BulkedSegregantAnalysis/BulkedSegregantAnalysis.txt"

    FIELDS = [

        path(
            "Project Directory",
            template="PROJECTDIR",
            mode="directory",
            help_text=(
                    "(path)\n"
                    "Directory selection window to choose where project outputs are stored."
            ),
        ),

        text(
            "High Group",
            template="HIGHGROUP",
            help_text=(
                    "(text)\n"
                    "Filename prefix of the high group's sequencing data."
            ),
        ),

        text(
            "Low Group",
            template="LOWGROUP",
            help_text=(
                    "(text)\n"
                    "Filename prefix of the low group's sequencing data."
            ),
        ),

        path(
            "Reference Genome",
            template="REFGENOME",
            mode="file",
            help_text=(
                "(path)\n"
                "File selection window for choosing reference genome .fasta file."
            )
        ),

        integer(
            "Number of Cores",
            template="CORES",
            minimum=1,
            maximum=512,
            default=1,
            help_text=(
                    "(integer)\n"
                    "Many HPC documentations often use the terms 'CPU' and 'node' "
                    "interchangeably. Here, our terminology represents a hierarchical "
                    "structure in which CPU is nested within node (i.e., one node has "
                    "many CPUs). Please keep in mind that some HPC systems limit how many "
                    "nodes are available within a 'computer' and thus you may need to edit "
                    "the script header to run in parallel in certain systems."
            ),
        ),

        integer(
            "Max RAM in GB",
            template="MAXRAM",
            minimum=0,
            maximum=400,
            help_text=(
                "(integer)\n"
                "Maximum amount of RAM (GB) to be used for GATK HaplotypeCaller option. "
                "You should drop the RAM usage to about 4-8 GB lower than allocated to your "
                "whole job because the JAVA virtual machine running HaplotypeCaller needs "
                "a little bit of overhead for certain processes other than the analysis."
            )
        ),
        integer(
            "Number of Chromosomes",
            template="CHROM_COUNT",
            minimum=0,
            maximum=100000,
            default=160,
            help_text=(
                "(integer)\n"
                "The number of chromosomes in your genome."
            )
        ),

        text(
            "Chromosome Prefix",
            template="CHROM_PREFIX",
            help_text=(
                    "(text)\n"
                    "Prefix of chromosomes in your genome's fasta file header's "
                    "(e.g., `Chr`, `chr_`, `scaff_`, etc.)"
            ),
        ),

        path(
            "GTF",
            template="GTF",
            mode="file",
            help_text=(
                "(path)\n"
                "File selection window for choosing reference genome annotation (*.gtf)."
            )
        ),

        floating(
            "G-Prime Alpha Cutoff",
            template="GPRIME_ALPHA",
            minimum=0,
            maximum=0.5,
            default=0.05,
            decimals=5,
            step=0.001,
            help_text=(
                    "(float, default: 0.05)\n"
                    "Alpha cut-off value to determine significance for G-Prime "
                    "Analyses."
            ),
        ),

        floating(
            "Reference Allele-Frequency",
            template="ALLELE_FREQ",
            minimum=0,
            maximum=0.5,
            default=0.2,
            decimals=5,
            step=0.001,
            help_text=(
                    "(float, default: 0.2)\n"
                    "Reference-allele frequency cut-off for SNP filtering before running "
                    "Bulked Segregant Analysis. It may be best to choose a better value "
                    "in the variable initialization of the `BulkedSegregantAnalysis.R` script"
                    "after assessing the diagnostic plots."
            ),
        ),

        integer(
            "Minimum Total Depth",
            template="MIN_TOTDEPTH",
            minimum=0,
            maximum=100000,
            help_text=(
                    "(integer)\n"
                    "The minimum total depth for SNP-filtering input into Bulked-Segregant "
                    "Analysis. It may be best to choose a better value "
                    "in the variable initialization of the `BulkedSegregantAnalysis.R` script"
                    "after assessing the diagnostic plots."
            )
        ),

        integer(
            "Maximum Total Depth",
            template="MAX_TOTDEPTH",
            minimum=0,
            maximum=100000,
            help_text=(
                    "(integer)\n"
                    "The maximum total depth for SNP-filtering input into Bulked-Segregant "
                    "Analysis. It may be best to choose a better value "
                    "in the variable initialization of the `BulkedSegregantAnalysis.R` script"
                    "after assessing the diagnostic plots."
            )
        ),

        integer(
            "Minimum Sample Depth",
            template="MIN_SAMDEPTH",
            minimum=0,
            maximum=100000,
            help_text=(
                    "(integer)\n"
                    "The minimum sample depth for SNP-filtering input into Bulked-Segregant "
                    "Analysis. It may be best to choose a better value "
                    "in the variable initialization of the `BulkedSegregantAnalysis.R` script"
                    "after assessing the diagnostic plots."
            )
        ),

        integer(
            "Minimum GQ",
            template="GQ",
            minimum=0,
            maximum=64,
            help_text=(
                    "(integer)\n"
                    "The minimum GQ threshold for SNP-filtering input into Bulked-Segregant "
                    "Analysis. It may be best to choose a better value "
                    "in the variable initialization of the `BulkedSegregantAnalysis.R` script"
                    "after assessing the diagnostic plots."
            )
        ),
    ]

    def get_template_context(self):

        context = super().get_template_context()

        context["APPTAINER_DIR"] = str(
            Path(__file__).parent /
            "apptainers"
        )

        context["TEMPLATE_DIR"] = str(
            Path(__file__).parent /
            "module_templates"
        )

        return context

"""
To create a new widget add the below as a new class above and then add it to the registry below  (in __all__):
class NewAnalysis(WidgetItem):

    TYPE = "new_analysis"
    TITLE = "New Analysis"

    TEMPLATE = "NewAnalysis/script.txt"

    FIELDS = [

        text(
            "Sample Name",
            template="SAMPLE",
        ),

        path(
            "Input Directory",
            template="INPUT_DIR",
            mode="directory",
        ),

        integer(
            "Threads",
            template="THREADS",
            minimum=1,
            maximum=128,
            default=8,
        ),
    ]
"""

# ----------------------------------------------------------------------
# Widget Registry
# ----------------------------------------------------------------------

__all__ = [

    "ScheduleSystem",
    "SequenceProcessor",
    "Aligner",
    "DifferentialExpression",
    "Coverage",
    "SNPCalling",
    "SNPFilteringPreImputation",
    "SNPImputation",
    "BulkedSegregantAnalysis",
]

