z <- runif(1224, min=0, max=1)
y <- qzipf(z, N=6, s=2)
write(y, "polblogs_privacy.txt", ncolumns=1, sep = ",")
table(y)
