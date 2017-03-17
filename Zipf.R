z <- runif(65536, min=0, max=1)
y <- qzipf(z, N=6, s=2)
write(y, "output.txt", ncolumns=1, sep = ",")
table(y)
