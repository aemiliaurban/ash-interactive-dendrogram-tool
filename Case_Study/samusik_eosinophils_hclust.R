BASE_PATH = "<INSERT YOUR PATH HERE>"

for (i in 1:11) {
  eo <- read.csv(
    paste(BASE_PATH, "Case_Study/eosinophils_", i, "/data.csv",sep="")
  )
  hc <- hclust(dist(eo))
  
  write.csv(
    hc["merge"],
    paste(BASE_PATH, "Case_Study/eosinophils_", i, "/merge.csv",sep=""),
    row.names = FALSE)
  write.csv(
    hc["height"],
    paste(BASE_PATH, "Case_Study/eosinophils_", i, "/heights.csv",sep=""),
    row.names = FALSE)
  write.csv(
    hc["order"],
    paste(BASE_PATH, "Case_Study/eosinophils_", i, "/order.csv",sep=""),
    row.names = FALSE)
}



