x = linspace(-2,3.3,100);
y = exp(-(x.*sin(x/2)).^2);
y2 = sin(x);
figure
plot(x',y','color','IndianRed')
hold on
plot(x,y2)
set(gca,'xtick',[-1 0 1 2])
figure
plot(x,y.^2,'color','cornflowerblue')
figure
plot(x,sqrt(y),'color','brickred')
figure
fill([x,fliplr(x)],[y,fliplr(y2)])