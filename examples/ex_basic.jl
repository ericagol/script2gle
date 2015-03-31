x = linspace(-5,5,500)
y = exp(-(x).^2/2)

# J2G 
# rem can also be non-compliant (with single '')
# since it's not read with Julia..

plot(x,y,'-b','linewidth',1.5)
#
title('The std normal distribution')
xlabel('$x$')
ylabel('$\mathcal N(x;0,1)$')