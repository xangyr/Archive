xx=[0 0.2 0.4 0.6 0.8 1];
yy=[1.996 1.244 0.810 0.541 0.375 0.259];
y1=log(yy);
x1=log(1+xx);
for i=1:length(xx)
	A(i,1)=1;
	A(i,2)=xx(i);
	A(i,3)=x1(i);
	yy1(i,1)=y1(i);
end
fprintf('The normal form of the matrix is\n')
disp(vpa(A,3))
AA=A\yy1;
fprintf('The coefficients A0=%f, A1=%f and A2=%f\n',AA(1),AA(2),AA(3));
syms x
y(x)=exp(AA(1)+AA(2).*x+AA(3).*log(1+x));
plot(xx,yy,'r*','linewidth',2)
hold on
plot(xx,double(y(xx)))
xlabel('x')
ylabel('y(x)')
title('x vs. y(x) plot')
legend('Actual data','Fitted data')
