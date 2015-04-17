x = linspace(-2,3.3,100);
y = exp(-(x.*sin(x/2)).^2);
plot(x,y,'color','IndianRed')