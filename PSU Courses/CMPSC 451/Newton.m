function [iter,x1]=Newton(f,df,x0)
max_iter=100;
iter=0;
x1=x0-f(x0)/df(x0);
while 1
    x1=x0-f(x0)/df(x0);
    iter=iter+1;
    if abs(x1-x0)<1e-10 || iter>max_iter
        break
    else
        x0=x1;
    end
end
