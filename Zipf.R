z <- runif(26475, min=0, max=1)
y <- qzipf(z, N=5, s=2)
write(y, "/Users/Apple/Desktop/lvl.txt", ncolumns=1, sep = ",")
table(y)


