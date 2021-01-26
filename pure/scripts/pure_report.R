# title:
# author: domi
# date: Tue Jan 26 14:43:51 2021 

# libraries ---------------------------------------------------------------
library(dplyr)
library(data.table)
library(stringr)
library(seqinr)
library(ggplot2)


# working directory
cwd <- "~/Documents/promotion/mvome_pipeline/pure/pure/scripts/"
setwd(cwd)


# get ouput directory ---------------------------------------------------------

args = commandArgs(trailingOnly = TRUE)
# while developing
args <- c("~/Documents/promotion/mvome_pipeline/test_pure/o6")

outdir <- args[1] 


# input files -------------------------------------------------------------

dvf_file <- file.path(outdir, "virome/deepvirfinder/contigs_final.fasta_gt1bp_dvfpred.txt")
vs_file <- file.path(outdir, "virome/virsorter/final-viral-score.tsv")
marvel_file <- file.path(outdir, "log/marvel.log")

plasflow_file_1 <- file.path(outdir, "plasmidome/plasflow/plasflow_out.tsv")



# read data ---------------------------------------------------------------

dvf_dt <- fread(dvf_file)
vs_dt <- fread(vs_file)
marvel_dt <- fread()