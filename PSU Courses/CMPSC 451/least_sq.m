xdata=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1];
ydata=[0.7829,0.8052,0.5753,0.5201,0.3783,0.2923,0.1695,0.0842,0.0415,0.009,0];
p1=polyfit(xdata,ydata,1); % first order polynomial 
p2=polyfit(xdata,ydata,2); % second order polynomial 
p4=polyfit(xdata,ydata,4); % fourth order polynomial 
p8=polyfit(xdata,ydata,8); % eight order polynomial 
y1=polyval(p1,xdata);
y2=polyval(p2,xdata);
y4=polyval(p4,xdata);
y8=polyval(p8,xdata);
figure
plot(xdata,ydata,'o'); 
hold on
plot(xdata,y1,'c--')
plot(xdata,y2,'b--')
plot(xdata,y4,'g--')
plot(xdata,y8,'r--') 
title('Data and polynomials approximation')
legend('Data','P1','P2','P4','P8','Location','Northeast')