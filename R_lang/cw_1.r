library(readr)
napoje = read.csv("C:/Users/�ukasz �akowski/Desktop/Studia/Statystics/R/napoje_po_reklamie.csv", row.names = 1, header = TRUE,sep=";")
View(napoje)
typeof(napoje)
sapply(napoje, sd)
sapply(napoje, mean)
sapply(napoje, var)
sapply(napoje, min)
sapply(napoje, median)
sapply(napoje, range)
sapply(napoje, quantile)
pepsi <- c(napoje$pepsi)
fanta <- c(napoje$fanta)
summary(fanta)
summary(pepsi)
mean(pepsi)
var(pepsi)
sd(pepsi)
min(pepsi)
max(pepsi)
median(pepsi)
range(pepsi)
mean(fanta)
var(fanta)
sd(fanta)
min(fanta)
max(fanta)
median(fanta)
range(fanta)
wzrost <- read_csv("C:/Users/�ukasz �akowski/Desktop/Studia/Statystics/R/Wzrost.csv")
rowMeans(wzrost)
rowSums(wzrost)
max(wzrost)
min(wzrost)
median(wzrost)
range(wzrost)