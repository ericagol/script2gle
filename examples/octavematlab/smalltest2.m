x = linspace(-5,5,500);
plot(x,exp(-x.^2/2),'-r')
hold on
plot(x,exp(-abs(x)),'-','color','cornflowerblue')
set(gca,'ytick',[0 0.5 1],'yticklabel',['0', '1/2', '1'])
set(gca,'xtick',[-5 -2.5 0 2.5 5])
xlabel('$x$')
ylabel('$p(x)$')
legend('$\propto\mathcal N(0,1)$','$\propto$ Laplace','location','southeast')
set(gca,'fontsize',12)
% any of the following line will work

% fill([x,fliplr(x)],[exp(-x.^2/2),fliplr(exp(-abs(x)))],'color','cornflowerblue','alpha',0.2)
% fillbetween(x,exp(-x.^2/2),exp(-abs(x)),'color','indianred','alpha',0.8)
fillbetween(x,exp(-x.^2/2),exp(-abs(x)),'color',[1 0 1 0.3])