options.MaxIter=100;options.Tol=1e-10;
A=[2 -1 0; -1 2 -1; 0 -1 2];b=[1;2;3];
x0=[0;0;0];
x=Jacobi(A,b,x0,options)
x=Gauss_seidel(A,b,x0,options)
omega=1/2;
x=SOR(A,b,omega,x0,options)
omega=1.2;
x=SOR(A,b,omega,x0,options)
omega=1.5;
x=SOR(A,b,omega,x0,options)