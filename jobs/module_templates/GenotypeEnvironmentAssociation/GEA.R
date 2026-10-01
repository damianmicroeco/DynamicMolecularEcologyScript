#!/usr/bin/env Rscript

library(optparse)
library(LEA)

option_list <- list(
    make_option(c("-i", "--input_vcf"), type = "character", help = "Filtered and imputed vcf file."),
    make_option(c("-d", "--lea_dir"), type = "character", help = "Directory in which to run and store LEA project."),
    make_option(c("-k", "--min_l"), type = "integer", help = "Minimum number of K populations to test."),
    make_option(c("-j", "--max_k"), type = "integer", help = "Maximum number of K populations to test."),
    make_option(c("-e", "--environment"), type = "character", help = "CSV-delimited environmental metadata")
)

parser <- OptionParser(option_list = option_list, add_help_option = FALSE)
args <- parse_args(parser)

#Initialize variables
input_vcf = args$input_vcf
lea_dir = args$lea_dir
min_k = args$min_k
max_k = args$max_k
env_df = read.csv(args$environment)

#move to LEA directory
setwd(lea_dir)

#convert vcf to lfmm
vcf2lfmm(input_vcf, output.file = "lea")

#Run PCA
pc = pca("lea.lfmm", scale = TRUE)

#PCA Elbow Plot
pdf("lea_pca_elbow.pdf", sep = "")
plot(pc)
dev.off()

#Tracy-Widom
tw = tracy.widom(pc)

pdf("lea_pca_tracy-widom.pdf", sep = "")
plot(tw$percentage)
dev.off()

#sNMF STRUCTURE analysis
project = NULL
project = snmf("lea.geno",
        K = min_k:max_k,
        entropy = TRUE,
        repetitions = 20,
        project = "new"
        )

pdf("lea_snmf_cross-entropy.pdf")
plot(project)
dev.off()

dir.create("ancestry_matrices")

for (i in min_k:max_k) {
    best = which.min(cross.entropy(project, K = i))
    pdf(paste("ancestry_matrices/k_", i, ".pdf", sep = ""))
    barchart(project, 
            K = i,
            run = best,
            xlab = "Individuals", ylab = "Ancestry Proportions",
            main = paste("Ancestry matrix, K = ", i, sep = ""), 
            border = NA,
            space = 0
            )
    dev.off()
}

#run GEA for desired sets of K
write.env(env_df, "lea.env")
#######directory to store RData outputs

lfmm_input = read.lfmm("lea.lfmm")
lfmm_env = as.matrix(env_df) #need to include a sorting mechanism to match samples

for (i in min_k:max_k) {
    lfmm_project = lfmm2(
        lfmm_input,
        lfmm_env,
        K = i
    )

    #you can also change the linear model by specifying `linear = FALSE` and setting `family` to the type of generalized linear model you'd prefer
    lfmm_res = lfmm2.test(lfmm_project,
        lfmm_input,
        lfmm_env,
        genomic.control = TRUE
        )
    
    #save the lfmm results in an RData file for future use
    save.image(paste(lea_dir, "/lfmm_result_K-", i, ".RData", sep = ""))
}