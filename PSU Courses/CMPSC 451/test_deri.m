f=@(x) x.*exp(x);
ana_der=@(x) exp(x)+x.*exp(x);

a = 0.5;
h = 0.01;
bf = num_der(f, a, h);
b = ana_der(a)

a = [0:1e-2:1];
df = num_der(f,a,h);
plot(a,df,'r');
hold on
plot(a, ana_der(a),'b');

err_h = abs(df-ana_der(a));
% change value of h here
h = h/2;
df = num_der(f,a,h);
err_h2 = abs(df-ana_der(a));
order = log2(err_h/err_h2);