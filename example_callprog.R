sndp = 30
sltp = 25
clyp = 48 
orc = 23
bld = 1200
cec = 12
phihox = 6.4
x <- AWCPTF(sndp, sltp, clyp, orc, bld, cec, phihox)
library(GSIF)
install.packages(c("RCurl", "XML", "rgdal", "raster", "sp", "aqp", "mda", "gstat", "plotKML", "dismo", "rJava"))
install.packages("GSIF", repos=c("http://R-Forge.R-project.org"), type = "source")
str(x)
attr(x, "coef")
data(afsp)
names(afsp$horizons)
