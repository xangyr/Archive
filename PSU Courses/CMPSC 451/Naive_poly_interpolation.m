function pn=Naive_poly_interpolation(xi,yi,x)
A=vander(xi);
a=A\yi';
n=length(xi)-1;
pn=0;
for i=1:n+1
    pn=pn+a(i)*x.^(n+1-i);
end