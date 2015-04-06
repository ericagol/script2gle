x = linspace(-5,5,500)
y = exp(-(x).^2/2)

# J2G ----------
#
plot(x,y,'-b','linewidth',0.5)
#
title('The std normal distribution')
xlabel('$x$')
ylabel('$\mathcal N(x;0,1)$')
#
set(gca,'xtick',[-5 -2.5 0 2.5 5],'ytick',0:.5:1)
#
set(gca,'xticklabel',['-5','-5/2','0','5/2','5'])
set(gca,'yticklabel',['0','50%','100%'])

