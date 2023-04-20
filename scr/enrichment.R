library(gprofiler2)

# read file 
df <- read.csv('enrichment.csv')

gostres <- gost(query = df$snp_gprofiler_10000,
                organism = "hsapiens")
head(gostres$result)
p <- gostplot(gostres, capped = FALSE, interactive = FALSE)
p
