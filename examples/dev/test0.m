x = linspace(-pi,pi,400);
y = sin(x)+0.5*cos(x).^2;
x2 = linspace(-pi,pi,50);
y2 = (1-x.^2*pi).*exp(-x.^2);
y3 = (1-x2.^2*pi).*exp(-x2.^2);
plot(x,y,'--r')
hold on
plot(x,y2,'-b','lwidth',0.1)
stem(x2,y3,'ok','msize',1.0,'markerfacecolor',foo)