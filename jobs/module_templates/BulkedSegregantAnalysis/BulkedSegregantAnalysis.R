#!/usr/bin/env Rscript

library(optparse)
library(QTLseqr)
library(ggplot2)
library(dplyr)
library(GenomicRanges)
library(snpsettest)

option_list <- list(
    make_option(c("-v", "--variant_table"), type = "character", help = "Path to output of GATK VariantsToTable Function"),
    make_option(c("-n", "--N"), type = "integer", help = "Number of chromosomes"),
    make_option(c("-c", "--chrom_prefix"), type = "character", help = "Prefix of chromosome names"),
    make_option(c("-g", "--GTF"), type = "character", help = "Path to reference genome's GTF"),
    make_option(c("-o", "--outdir"), type = "character", help = "Path to output directory"),
    make_option(c("-a", "--gprime_alpha"), type = "double", help = "Alpha cut-off for Gprime statistic")
)

parser <- OptionParser(option_list = option_list, add_help_option = FALSE)
args <- parse_args(parser)

#Initiating variables
variant_table = args$variant_table
N = args$N
chrom_prefix = args$chrom_prefix
GTF = args$GTF
outdir = args$outdir
gprime_alpha = args$gprime_alpha

#Choose which chromosomes will be included in the analysis (i.e. exclude smaller contigs)
chroms = paste0(rep(chrom_prefix, N), 1:N)

#Import SNP data from file
df =
    importFromGATK(
        file = variant_table,
        highBulk = "HIGH",
        lowBulk = "LOW",
        chromList=chroms
    )

#Read depth histogram to help decide what could be a good cut-off for removing SNPs
png(paste(outdir, "/depth_histogram.png", sep = ""), units = "in", width = 8, height = 3, res = 300)
ggplot(data = df) + 
    geom_histogram(aes(x = DP.HIGH + DP.LOW))
dev.off()

#Filter by reference allele frequency
png(paste(outdir, "/ref_allele_frequency.png", sep = ""), units = "in", width = 8, height = 3, res = 300)
ggplot(data = df) +
    geom_histogram(aes(x = REF_FRQ))
dev.off()

#Check the per-bulk distributions. You should, in theory, get two small peaks at the two extremes and a Gaussian distribution around 0.5
png(paste(outdir, "/high_bulk_distribution.png", sep = ""), units = "in", width = 8, height = 3, res = 300)
ggplot(data = df) +
    geom_histogram(aes(x = SNPindex.HIGH)) +
    ggtitle("High Bulk")
dev.off()

png(paste(outdir, "/low_bulk_distribution.png", sep = ""), units = "in", width = 8, height = 3, res = 300)
ggplot(data = df) +
    geom_histogram(aes(x = SNPindex.LOW)) +
    ggtitle("Low Bulk")
dev.off()

#Filter SNPs based on some criteria. See section below about using the filterSNPs function for more information.
#We suggest reviewing the outputs from above to optimize the values below and rerun the SNP filtering
df_filt =
    filterSNPs(
        SNPset = df,
        refAlleleFreq = 0.20,
        minTotalDepth = 100,
        maxTotalDepth = 400,
        minSampleDepth = 40,
        minGQ = 99
    )

#SNP filtering is one of the most time-consuming steps. we recommend saving an image at this stage, commenting out the above, and loading the image before continuing if running this script multiple times.

#Run G' analysis
df_filt_Gprime = runGprimeAnalysis(SNPset = df_filt,
                             windowSize = 1e6,
                             outlierFilter = "deltaSNP",
                             filterThreshold = 0.1)

#G' distributions with different filters
png(paste(outdir, "/g_prime_outliers_Hampel.png", sep = ""), units = "in", width = 8, height = 3, res = 300)
plotGprimeDist(SNPset = df_filt_Gprime, outlierFilter = "Hampel", binwidth = 0.1) +
    xlim(0, 10)
dev.off()

png(paste(outdir, "/g_prime_outliers_deltaSNP.png", sep = ""), units = "in", width = 8, height = 3, res = 300)
plotGprimeDist(SNPset =df_filt_Gprime, outlierFilter = "deltaSNP", filterThreshold = 0.1, binwidth = 0.1) +
    xlim(0, 10)
dev.off()

#Get QTL regions from G'
qtl_regions_Gprime = getQTLTable(
    SNPset = df_filt_Gprime,
    method = "Gprime",
    alpha = 0.01,
    export = FALSE)

##Run QTLseq analysis
df_filt_QTLseq= runQTLseqAnalysis(
    SNPset = df_filt,
    windowSize = 1e6,
    popStruc = "F2",
    bulkSize = c(71, 71),
    replications = 10000,
    intervals = c(95, 99))

#Get QTL regions from QTLseq
qtl_regions_QTLseq = getQTLTable(
    SNPset = df_filt_QTLseq,
    method = "QTLseq",
    interval = 95,
    export = FALSE)

#Export summary CSV for Gprime QTLs
getQTLTable(
    SNPset = df_filt_Gprime,
    method = "Gprime",
    alpha = gprime_alpha,
    export = TRUE,
    fileName = paste(outdir, "/bsa_qtl_Gprime.csv", sep = ""))

#Export summary CSV for deltaSNP QTLs
getQTLTable(
    SNPset = df_filt_QTLseq,
    method = "QTLseq",
    interval = 95,
    export = TRUE,
    fileName = paste(outdir, "/bsa_qtl_delta_snp.csv", sep = ""))

#Plot Gprime
png(paste(outdir, "/g_prime_plot.png", sep = ""), units = "in", width = 8, height = 3, res = 300)
(gplot = plotQTLStats(
    SNPset = df_filt_Gprime,
    var = "Gprime",
    plotThreshold = TRUE,
    q = gprime_alpha) +
    facet_wrap(vars(CHROM), nrow=3, ncol=5) +
    theme_minimal() +
    theme(panel.grid = element_line(color = "#FFFFFF", size = 0)) +
    theme(axis.text.x = element_text(angle = 30, size=10), axis.text.y= element_text(size=10),
          axis.title.y=element_text(size = 14), axis.title.x=element_text(size = 14))+
    theme(panel.background = element_rect(fill='transparent'),
        plot.background = element_rect(fill='transparent', color=NA),
        strip.text=element_text(margin=margin(), size = 10),
        panel.spacing=unit(1, "lines"))
)
dev.off()

#Plot deltaSNP
png(paste(outdir, "/delta_snp_plot.png", sep = ""), units="in", width=5, height=4, res=300)
plotQTLStats(
    SNPset = df_filt_QTLseq,
    var = "deltaSNP",
    plotIntervals = TRUE)+
  facet_wrap(vars(CHROM), nrow=3, ncol=5) +
  theme_minimal() +
  theme(panel.grid = element_line(color = "#FFFFFF", size = 0)) +
  ylim(c(-0.4,0.4))+
  theme(axis.text.x = element_text(angle = 30, size=10), axis.text.y= element_text(size=10),
        axis.title.y=element_text(size = 14), axis.title.x=element_text(size = 14),
        legend.position = "none")+
  theme(panel.background = element_rect(fill='transparent'),
        plot.background = element_rect(fill='transparent', color=NA),
        strip.text=element_text(margin=margin(), size = 10),
        panel.spacing=unit(1, "lines"))
dev.off()

#Map significant SNPs to gene IDs

#Reading in GTF file (annotated genome)
gtf = read.table(GTF, sep="\t", header=FALSE)
#Renaming columns
colnames(gtf) <- c("chr", "annot_program", "mol_type", "start", "end", "score", "strand", "blah", "gene.id")

#Only selecting genes from molecular type
gtf = gtf[gtf$mol_type=="gene",]

#Taking G' values greater than 95% confidence interval
sig_df = df_filt_QTLseq[df_filt_QTLseq$tricubeDeltaSNP >= -1*df_filt_QTLseq$CI_95,]

#Making an id column with chromosome and position
sig_df$id = paste(sig_df$CHROM, '_', sig_df$POS, sep="")
colnames(sig_df)[1:2] = c('chr', 'pos')

#Mapping SNPS to genes with 20kb on either side
mapsnp = map_snp_to_gene(sig_df, gtf, extend_start = 20, extend_end = 20)

#Merging significant SNPS dataframe to SNP map dataframe by id
comb_df = merge(sig_df, mapsnp$map, by="id")

#Rename chr.x and pos.x, because by merging the two dataframes there are two of each column
colnames(comb_df)[2:3] = c('chr', 'pos')

#Now you have a list of all of the significant genes in your QTLs!
write.csv(comb_df, paste(outdir, "/sig_gene_hits_delta_snp.csv", sep = ""))

#Taking tricubeDeltaSNP values greater than 95% confidence interval
sig_df = df_filt_QTLseq[df_filt_Gprime$pvalue <= gprime_alpha,]

#Making an id column with chromosome and position
sig_df$id = paste(sig_df$CHROM, '_', sig_df$POS, sep="")
colnames(sig_df)[1:2] = c('chr', 'pos')

#Mapping SNPS to genes with 20kb on either side
mapsnp = map_snp_to_gene(sig_df, gtf, extend_start = 20, extend_end = 20)

#Merging significant SNPS dataframe to SNP map dataframe by id
comb_df = merge(sig_df, mapsnp$map, by="id")

#Rename chr.x and pos.x, because by merging the two dataframes there are two of each column
colnames(comb_df)[2:3] = c('chr', 'pos')

#Now you have a list of all of the significant genes in your QTLs!
write.csv(comb_df, paste(outdir, "/sig_gene_hits_gprime.csv", sep = ""))