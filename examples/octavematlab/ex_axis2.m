% OK APR 9
x = linspace(1,10,100);
y = exp(x)./(x.^3.*log(x+0.5));

plot(x,y,'-','color','olive')
ylim([0 11])
xlim([0 11])
set(gca,'xtick',[2 5 10])
set(gca,'xticklabel',['$\sin(\pi x_0)$','$\mathcal L$','$\alpha^2_1$'])