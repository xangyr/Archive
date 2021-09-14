wi=1;
h=0.1;
w=[wi];
y=[wi];
for i=1:1/h
    ti=h*i;
    yi=2*atan(exp(ti + log(tan(1/2))));
    wi=wi+sin(wi)*h;
    w=[w;wi];
    y=[y;yi];
    
end
clf
plot([0:10]*h,y,'linewidth',3);
hold on
plot([0:10]*h,w,'linewidth',3);

wi=1;
w=[wi];
df=@(w) 1-cos(w)*h;
for i=1:1/h
    f=@(w) w-wi-sin(w)*h;
    wi=Newton(f,df,wi,1e-10);
    w=[w;wi];
end
plot([0:10]*h,w,'linewidth',3);
set(gca,'fontsize',30)
legend('Real solution','Forward Euler','Backward Euler')
xlabel('t')
ylabel('y')