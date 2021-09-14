f=@(x) x^2-2*x-5;
df=@(x) 2*x-2;

r=Newton(f,df,-1);