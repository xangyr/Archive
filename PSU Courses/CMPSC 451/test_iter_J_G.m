options.MaxIter=100;options.Tol=1e-5;
d=1e-5;
A=[1+d -1 0; -1 2+d -1; 0 -1 1+d];b=[-1;-1;2];
x0=[0;0;0];
x=Jacobi(A,b,x0,options)
x=Gauss_seidel(A,b,x0,options)