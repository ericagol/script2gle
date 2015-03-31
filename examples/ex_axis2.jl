x = linspace(0,5,100)
y = exp(x)

# J2G --------------
#
plot(x,y,'-b','linewidth',1.5)
#
set(gca,'yscale','log')
set(gca,'xtick',[0,2.5,5])
set(gca,'ylim',[1 150])