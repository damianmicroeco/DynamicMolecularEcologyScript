#!/usr/bin/env Rscript

library(optparse)
library(DESeq2)
library(ggplot2)
library(tidyr)
library(stringr)
library(dplyr)

option_list <- list(
    make_option(c("-i", "--genecountdir"), type = "character", help = "Directory where gene counts are stored"),
    make_option(c("-m", "--metatable"), type = "character", help = "Metadata file (col 1: sample_prefix, col 2: group, header must be included)"),
    make_option(c("-r", "--read1suffix"), type = "character", help = "Read 1 Suffix for matching to internal naming conventions"),
    make_option(c("-s", "--strand"), type = "character", help = "Use unstranded (2), forward stranded (3), or reverse stranded (4) counts"),
    make_option(c("-g", "--group1"), type = "character", help = "Name of group 1"),
    make_option(c("-h", "--group2"), type = "character", help = "Name of group 2"),
    make_option(c("-t", "--test_type"), type = "character", help = "Test for DESeq2 ('Wald' or 'LRT')"),
    make_option(c("-c", "--cutoff"), type = "double", help = "Alpha cutoff for significance"),
    make_option(c("-o", "--output"), type = "character", help = "Output file"),
    make_option(c("-p", "--palette1"), type = "character", default = "#415cc5", help = "Hexcode for group 1 color"),
    make_option(c("-q", "--palette2"), type = "character", default = "#c5aa41", help = "Hexcode for group 2 color"),
    make_option(c("-v", "--verbose"), action = "store_true", default = FALSE, help = "Print progress messages")
)

parser <- OptionParser(option_list = option_list, add_help_option = FALSE)
args <- parse_args(parser)

## Initiating Variables
genecountdir = args$genecountdir #directory containing the read counts from STAR
read1suffix = args$read1suffix #suffix for read 1 reads 
strandcolumn = args$strand #whether to use unstranded (2), forward stranded (3), or reverse stranded (4) counts
grouplist1 = c(args$group1, args$group2) #levels of factor of interest in alphabetical order of files (i.e., the same order as list.files output)
meta_table = args$metatable #metadata with column 1 being the read prefix and column 2 as your grouping variable
test_type = args$test_type #type of test for DESeq analysis. Wald is preferred if you're just doing your model against a full null. LRT is useful if you're comparing between a full model and a simplified model
alpha_cutoff = args$cutoff #alpha cut-off for multiple hypothesis correction of DESeq2 results
color_palette1 = c(paste("#", args$palette1, sep = ""), paste("#", args$palette2, sep = "")) #color palette for plotting
output= args$output #directory to store deseq2 output files

if (strandcolumn == "Unstranded") {
    strandcolumn = 2
} else if (strandcolumn == "Forward-Stranded") {
    strandcolumn = 3
} else if (strandcolumn == "Reverse-Stranded") {
    strandcolumn = 4
} else {
    stop("Execution halted: Stranded value was mistyped.")
}
cat("Script is loaded and arguments saved.\n")

#create output directory
dir.create(output, recursive = TRUE, showWarnings = FALSE)


## Dataframe Management
### Build gene counts dataframe ###
filelist = list.files(genecountdir, pattern = "*ReadsPerGene.out.tab")

#read in sample mapping dataframe
<<<<<<< HEAD
samplemap = read.table(paste(sub("(.*\\/).*", "\\1", genecountdir), "/sample_name_map.tsv", sep = ""),
                        sep = "\t",
                        header = FALSE)
samplemap$V1 = lapply(samplemap$V1, function(x) basename(x))
samplemap$V2 = NULL
samplemap$V3 = lapply(samplemap$V3, function(x) basename(x))

samplemap$V1 = lapply(samplemap$V1, function(x) sub(paste(read1suffix, ".fastq.gz", sep = ""), "", x, fixed = TRUE))
samplemap$V3 = lapply(samplemap$V3, function(x) sub(".fastq.gz", "", x, fixed = TRUE))
=======
samplemap = read.table(file.path(dirname(genecountdir), "/sample_name_map.tsv"),
                        sep = "\t",
                        header = FALSE)
samplemap$V1 = unlist(lapply(samplemap$V1, function(x) basename(x)))
samplemap$V2 = NULL
samplemap$V3 = unlist(lapply(samplemap$V3, function(x) basename(x)))
samplemap$V4 = NULL

samplemap$V1 = unlist(lapply(samplemap$V1, function(x) sub(paste(read1suffix, ".fastq.gz", sep = ""), "", x, fixed = TRUE)))
samplemap$V3 = unlist(lapply(samplemap$V3, function(x) sub("_1.fastq.gz", "", x, fixed = TRUE)))
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)

colnames(samplemap) = c("sample_name", "new_sample_name")

#initialize counts dataframe by reading in first file
counts = read.table(paste(genecountdir, "/", filelist[1], sep = ""))
row.names(counts) = counts$V1
counts = counts[,c(1, strandcolumn)]
colnames(counts)[2] = filelist[1]
counts[,3:(length(filelist)+1)] = NA
counts$V1 = NULL

for (i in 2:length(filelist)) {
    tempdf = read.table(paste(genecountdir, "/", filelist[i], sep = ""))
    counts[,i] = tempdf[,strandcolumn]
    colnames(counts)[i] = filelist[i]
}

<<<<<<< HEAD
colnames(counts) = lapply(colnames(counts) function(x) basename(x))
colnames(counts) = lapply(colnames(counts) function(x) sub("ReadsPerGene.out.tab", "", x))
=======
colnames(counts) = lapply(colnames(counts), function(x) basename(x))
colnames(counts) = lapply(colnames(counts), function(x) sub("ReadsPerGene.out.tab", "", x))
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)
cat("Read counts have been read.\n")

### Build metadata dataframe ###
meta_df = read.csv(meta_table, header = TRUE, stringsAsFactors = FALSE, check.names = FALSE)

colnames(meta_df) = c("sample_name", "group_id")

meta_df = merge(meta_df, samplemap, by = "sample_name")
meta_df$sample_name = NULL
meta_df = meta_df[,c("new_sample_name", "group_id")]
colnames(meta_df)[1] = "sample_name"

row.names(meta_df) = meta_df$sample_name

### Prepare dataframes for input into DESeq2 ###
#put metadata in order of column names from gene counts matrix
all(rownames(meta_df) %in% colnames(counts)) #check all samples are in counts
all(rownames(meta_df) == colnames(counts)) #check samples are in order
counts = counts[, rownames(meta_df)] #put data in same order if the first is true but the second is false

#remove STAR info about unmapped, multimapped etc. reads
counts = counts[5:dim(counts)[1],]

#order factor levels for DESeq to know which is the reference group
group1_order = c(args$group1, args$group2)
meta_df$group_id = factor(meta_df$group_id, levels = group1_order)

cat("Metadata has been read.\n")

#load data in to DESeq object
dds = DESeqDataSetFromMatrix(countData = counts,
                                    colData = meta_df,
                                    design = ~group_id
                                    )

#remove low count reads (optional, but I'm doing it)
keep = rowSums(counts(dds)) >= 10
dds = dds[keep,]

#perform differential expression analysis
if (test_type == "Wald") {
    dds_analysis = DESeq(dds, test = test_type) 
    } else {
    dds_analysis = DESeq(dds, test = test_type, reduced = ~1)
    }

cat("Differential expression statistics calculated.\n")

res = results(dds_analysis, alpha = alpha_cutoff)

print("Column descriptions of resulting DESeq2 results dataframe:")
mcols(res, use.names = TRUE) #prints descriptions of columns in results df

print("Number of significant hits:")
print(sum(res$padj < alpha_cutoff, na.rm = TRUE)) #prints number of significant hits

#get significant results
res = res[!is.na(res$padj),] #DESeq2 will introduce NAs when adjusting for p-values because, I think, these are genes that are too weakly expressed and/or are constant (e.g., all 0s) across all samples.
sig_genes = res[res$padj < alpha_cutoff,]

#print out list of significant genes
print("Significant genes:")
print(rownames(sig_genes))

#which group is gene enriched in?
res$enrichment = res$enrichment <- ifelse(
    res$log2FoldChange < 0,
    group1_order[1],
    ifelse(
        res$log2FoldChange > 0,
        group1_order[2],
        "No difference"
    )
)

sig_genes$enrichment = ifelse(sig_genes$log2FoldChange < 0, group1_order[1], group1_order[2])

#export results
write.table(res, paste(output, "/", "DESeq2_allgenes.tsv", sep = ""), row.names = TRUE, quote = FALSE, sep = "\t")
write.table(sig_genes, paste(output, "/", "DESeq2_significantgenes.tsv", sep = ""), row.names = TRUE, quote = FALSE, sep = "\t")

cat("Differential expression results saved to disk.\n")

colorman1 = c(color_palette1)
names(colorman1) = group1_order

#Volcano Plot
pdf(paste(output, "/", "DESeq2_volcano_plot.pdf", sep = ""))
ggplot(as.data.frame(res), aes(x = log2FoldChange, y = -log(padj))) +
    geom_hline(yintercept = -log(alpha_cutoff), linetype = "dashed", color = "grey40") +
    geom_hline(yintercept = 0, color = "grey40") +
    geom_vline(xintercept = 0, color = "grey40") +
    geom_point(aes(color = enrichment, alpha = padj < alpha_cutoff)) +
    scale_color_manual(values = colorman1) +
    geom_text(as.data.frame(sig_genes), mapping = aes(x = log2FoldChange, y = -log(padj), label = rownames(sig_genes))) +
    theme_minimal() +
    theme(legend.position = "none")
dev.off()

cat("Analysis complete. Volcano plot summary written to disk.\n")
#plotMA(res)

#plotCounts(dds, gene = which.min(res$padj), intgroup = "group1")
