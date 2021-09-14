fun=@(x) sin(pi*x);
analytical_derivative=@(x) pi*cos(pi*x);
a=[0:1e-2:1];
h=0.01;
df=Num_der_central_differernce(fun,a,h);
plot(a,df,'r');
hold on
plot(a,analytical_derivative(a),'b')