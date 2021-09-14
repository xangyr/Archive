options.MaxIter=100;
options.Tol=1e-10;
A=[10 1 1; 1 -10 1; 0 1 10];b=[1;2;3];
x0=[0;0;0];
omega=1.1;
x=SOR(A,b,omega,x0,options)
omega=1.4;
x=SOR(A,b,omega,x0,options)
omega=1.6;
x=SOR(A,b,omega,x0,options)