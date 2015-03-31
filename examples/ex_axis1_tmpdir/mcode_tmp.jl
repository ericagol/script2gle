x = linspace(-5,5,500)
y = exp(-(x).^2/2)

# J2G ----------
#
x__ = x
y__ = y
c__ = [x__[:] y__[:]]
writecsv("ex_axis1_tmpdir/datplot1_1.dat",c__)
#
#
#


exit()
