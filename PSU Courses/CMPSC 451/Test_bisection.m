a=0;
b=2;
f=@(x) x-cos(x);
Tol=1e-6;
[c,count]=bisection(f,a,b,Tol)

a=0;
b=2;
f=@(x) x^3-4;
Tol=1e-3;
[c,count]=bisection(f,a,b,Tol)

