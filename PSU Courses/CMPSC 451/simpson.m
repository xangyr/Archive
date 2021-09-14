function v=simpson(fun,a,b,n)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
h=(b-a)/2/n;
v=feval(fun,a)+feval(fun,b);
x=a+h;
for i=1:1:n
    v=v+4*feval(fun,x);
    x=x+h+h;
end
x=a+h+h;
for i=1:1:n-1
    v=v+2*feval(fun,x);
    x=x+h+h;
end
v=v*h/3
end

