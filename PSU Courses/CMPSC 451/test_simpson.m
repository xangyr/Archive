n=[4,8,16,32,64,128];
error=zeros(size(n));
a=0;
b=0.8;
exact=exp(-1)-exp(-b);
for i=1:1:length(n)
    error(i)=abs(simpson('funItg',a,b,n(i))-exact);
end
loglog(n,error)
grid, title('Error with Trapezoid rule')
print -depsc simpsError.eps