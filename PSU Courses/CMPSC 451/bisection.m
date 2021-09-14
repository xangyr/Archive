function [c,count]=bisection(f,a,b,Tol)
c=(a+b)/2;
count=0;
while 1
    c=(a+b)/2;
    if f(a)*f(c)<0
        b=c;
    else
        a=c;
    end
    if (abs(f(c))<Tol)
        break
    end
    count=count+1;
end
