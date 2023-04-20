library(gprofiler2)

# read file 
df <- read.csv('enrichment.csv')
# perform enrichment analysis
gostres <- gost(query = df$snp_gprofiler,
                organism = "mmusculus")
df.res <- gostres$result
df.res <- apply(df.res,2,as.character)
# write res to file
write.csv(df.res, "Terms.csv", row.names=FALSE)
