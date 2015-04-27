x = linspace(-2,3,500);
y = exp(-abs(x).*cos(5*x));
y2 = exp(-abs(x).*cos(4*x));
plot(x,y)
xlabel('This is $x$')
ylabel('This is $y=\exp\left[-|x|\sin\left({x\over 10}\right)\right]$')
xlim([-3,3])
hold on
plot(x,y2,'-r')
figure
plot(x,y.^2)