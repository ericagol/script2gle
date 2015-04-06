x  = linspace(-3,3,200);
y1 = sin(x).*exp(-x.*cos(x));
y2 = sin(x).*exp(x.*cos(x));

plot(x,y1,'-r','linewidth',0.5)
hold on
plot(x,y2,'-b','linewidth',0.5)

% LABELS
title('Legend example')
xlabel('$x$')
ylabel('$y=f(x)$')
% Legend
legend('$f_1(x)$','$f_2(x)$')
legend('boxoff','location','nw','offset',[0.25,0.25])