#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from fields import (
    text,
    integer,
    floating,
    combo,
    path,
    visible_when,
    checkbox,
)

from widget_base import WidgetItem


# ----------------------------------------------------------------------
# Scheduler
# ----------------------------------------------------------------------

class ScheduleSystem(WidgetItem):

    TYPE = "scheduler"
    TITLE = "Scheduler"

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
        ),

        integer(
            "Run Time in Hours",
            template="HOURS",
            minimum=1,
            maximum=999,
            default=1,
        ),

        integer(
            "Memory per CPU in GB",
            template="MEMORY",
            minimum=1,
            maximum=4096,
            default=4,
        ),

        integer(
            "Number of CPUs",
            template="CPUS",
            minimum=1,
            maximum=512,
            default=1,
        ),

        text(
            "E-Mail",
            template="EMAIL",
        ),

        text(
            "Job Output File",
            template="OUTPUT",
        ),

        text(
            "Read 1 Suffix",
            template="READ1SUFFIX",
        ),

        text(
            "Read 2 Suffix",
            template="READ2SUFFIX",
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
        ),

        visible_when(
            path(
                "ORAD Executable",
                template="ORAD_EXECUTABLE",
                mode="file",
            ),
            "Processing Mode",
            "ORAD",
        ),

        visible_when(
            path(
                "ORAD Reference",
                template="ORAD_REFERENCE",
                mode="directory",
            ),
            "Processing Mode",
            "ORAD",
        ),

        path(
            "Sequencing Data",
            template="SEQUENCING_DATA",
            mode="directory",
        ),

        path(
            "Project Directory",
            template="FASTQ_OUTPUT_DIR",
            mode="directory",
        ),

        integer(
            "Number of Cores",
            template="CORES",
            minimum=1,
            maximum=512,
            default=1,
        ),

        integer(
            "Phred Score Cutoff",
            template="PHRED",
            minimum=0,
            maximum=50,
            default=20,
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
        ),

        visible_when(
            path(
                "Genome GTF file",
                template="GTF",
                mode="file",
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
            ),
            "Aligner",
            "STAR",
        ),

        visible_when(
            text(
                "BWA Prefix",
                template="BWA_PREFIX",
                default="bwa_out",
            ),
            "Aligner",
            "bwa-mem2",
        ),

        path(
            "Genome Fasta File",
            template="GEN_FASTA",
            mode="file",
        ),

        integer(
            "Number of Cores",
            template="CORES",
            minimum=1,
            maximum=512,
            default=1,
        ),

        path(
            "Project Directory",
            template="PROJECTDIR",
            mode="directory",
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

    TEMPLATE = "DifferentialExpression/DESeq2.txt"

    FIELDS = [

        path(
            "Project Directory",
            template="PROJECTDIR",
            mode="directory",
        ),

        path(
            "Metadata",
            template="METATABLE",
            mode="file",
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
        ),

        combo(
            "Delimiter",
            [
                "Comma-delimited",
                "Tab-delimited",
            ],
            template="DELIMITER",
            default="Comma-delimited",
        ),

        text(
            "Group 1 Name",
            template="GROUP1",
        ),

        text(
            "Group 2 Name",
            template="GROUP2",
        ),

        combo(
            "Test Type",
            [
                "Wald",
                "LRT",
            ],
            template="TESTTYPE",
            default="Wald",
        ),

        floating(
            "Alpha Cutoff",
            template="CUTOFF",
            minimum=0,
            maximum=0.5,
            default=0.05,
            decimals=5,
            step=0.001,
        ),

        text(
            "Group 1 Color Hexcode",
            template="PALETTE1",
            default="415cc5",
        ),

        text(
            "Group 2 Color Hexcode",
            template="PALETTE2",
            default="c5aa41",
        ),

        path(
            "Output Directory",
            template="OUTPUT_DIR",
            mode="directory",
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
        ),

        path(
            "Genome GTF file",
            template="GTF",
            mode="file",
        ),

        integer(
            "Number of Cores",
            template="CORES",
            minimum=1,
            maximum=512,
            default=1,
        ),

        integer(
            "Window Size (bp)",
            template="WINDOWSIZE",
            minimum=1,
            maximum=100000,
            default=100,
        ),

        integer(
            "Quality",
            template="QUALITY",
            minimum=1,
            maximum=60,
            default=30,
        ),

        path(
            "Output Directory",
            template="OUTPUT_DIR",
            mode="directory",
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
        ),
        
        path(
            "Reference Genome",
            template="REFGENOME",
            mode="file",
        ),

        integer(
            "Number of Cores",
            template="CORES",
            minimum=1,
            maximum=512,
            default=1,
        ),

        visible_when(
            integer(
                "Max RAM in GB",
                template="MAXRAM",
                minimum=0,
                maximum=100000,
                default=160,
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
        ),

        integer(
            "Number of Cores",
            template="CORES",
            minimum=1,
            maximum=512,
            default=1,
        ),

        integer(
            "DP<N (Depth Threshold)",
            template="DP",
            minimum=1,
            maximum=999,
            default=5,
        ),

        integer(
            "GQ<N (Genotype Quality Threshold)",
            template="GQ",
            minimum=1,
            maximum=99,
            default=20,
        ),
        
        integer(
            "QUAL>=N (Variant Level Quality Threshold)",
            template="QUAL",
            minimum=1,
            maximum=99,
            default=30,
        ),

        integer(
            "MAC>N (Minor Allele Count Threshold)",
            template="MAC",
            minimum=1,
            maximum=999,
            default=1,
        ),

        floating(
            "F_MISSING<=N (Site Level Missingness Threshold)",
            template="F_MISSING",
            minimum=0,
            maximum=1,
            default=0.10,
            decimals=5,
            step=0.001,
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
        ),

        integer(
            "Number of Cores",
            template="CORES",
            minimum=1,
            maximum=512,
            default=1,
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
]

