z <- runif(105, min=0, max=1)
y <- qzipf(z, N=6, s=2)
write(y, "polbooks_privacy.txt", ncolumns=1, sep = ",")
table(y)
