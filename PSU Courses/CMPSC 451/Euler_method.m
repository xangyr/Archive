wi=0.5;
for i=1:10
    ti=0.2*i;
    yi=(ti+1)^2-0.5*exp(ti);
    wi=(wi+0.2-0.008*(i)^2)/0.8;% Forward Euler method
    %wi=1.2*wi+0.2-0.008*(i-1)^2;% Backward Euler method
    disp([num2str(ti) '   ' num2str(wi) '   ' num2str(yi) '   ' num2str(abs(wi-yi))])
end