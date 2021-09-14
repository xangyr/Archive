function pn=Lagrange_poly_interpolation(xi,yi,x)
pn=0;
n=length(xi);
for i=1:n
    li=1;
    for j=1:n
        if j~=i
            li=li.*(x-xi(j))/(xi(i)-xi(j));
        end
    end
    pn=pn+yi(i)*li;
end