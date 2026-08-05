#!/usr/bin/env Rscript

library(optparse)
library(ggplot2)
library(dplyr)

option_list <- list(
    make_option(c("-i", "--inputdir"), type = "character", help = "Directory where mosdepth outputs are stored"),
    make_option(c("-g", "--gtf"), type = "character", help = "GTF file of genome"),
    make_option(c("-o", "--output"), type = "character", help = "Output file"),
    make_option(c("-v", "--verbose"), action = "store_true", default = FALSE, help = "Print progress messages")
)

parser <- OptionParser(option_list = option_list, add_help_option = FALSE)
args <- parse_args(parser)

## Initiating Variables
inputdir = args$inputdir #directory containing mosdepth coverage
gtf = args$gtf #gtf file of genome
output= args$output #directory to store mosdepth visualizations

file_list = list.files(path = inputdir, pattern = ".bam.regions.bed$", full.names = TRUE)

## Dataframe Management
# #read in first file to initialize dataframe for adding on the other individuals
df = read.table(file_list[1])
df$source = file_list[1]
for (i in 2:length(file_list)) {
    holder = read.table(file_list[i])
    holder$source = i
    df = rbind(df, holder)
}

#read in gtf to get gene coordinates
gtf_df = read.table(gtf, comment.char = "", sep = "\t")
gtf_df = gtf_df[gtf_df$V3 == "gene",]
gtf_df$pos_mean = rowMeans(gtf_df[, c("V4", "V5")]) #we're getting the mean position of the gene so that we can plot the gene name across the genome

#calculate mean coverage for summary visualization
df_mean = df %>%
  group_by(V2) %>%
  summarise(cov_mean = mean(log(V4+1))

#save visualization
pdf(paste(output, "/coverage.svg", sep = ""))
ggplot() +
  geom_line(data = df, aes(x = V2, y = log(V4 + 1), group = source), alpha = 0.1) +
  geom_line(data = df_mean, aes(x = V2, y = cov_mean, size = 1.5) +
  geom_linerange(data = gtf_df, aes(xmin = V4, xmax = V5, y = -.2), linewidth = 1.5, color = "grey30") +
  annotate("text", x = gtf_df$pos_mean, y = -.5, label = gtf_df$V9, angle = 30, size = 8/.pt) +
  theme_minimal() +
  xlab("Genome Position") +
  ylab("ln(Coverage + 1)") +
  facet_wrap(vars(V1), ncol = 1)
dev.off()

#save files needed for recreating visualization in a different Rscript
write.table(df, paste(output, "/combined_coverage_all_samples.tsv", sep = ""), row.names = FALSE, quote = FALSE, sep = "\t")
write.table(gtf_df, paste(output, "/filtered_gtf_for_plotting.tsv", sep = ""), row.names = FALSE, quote = FALSE, sep = "\t")