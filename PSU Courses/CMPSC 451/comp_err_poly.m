f1=@(x) cos(x);
f2=@(x) 1./(1+x.^2);

x = [-1:1e-2:1];
err_t = [];
for n = [5 10 20 40]
    disp(n)
    xi = [-1:2/n:1];
    yi_1 = f1(xi);
    yi_2 = f2(xi);

    n_pn_1 = Naive_poly_interpolation(xi, yi_1, x);
    n_pn_2 = Naive_poly_interpolation(xi, yi_2, x);
    l_pn_1 = Lagrange_poly_interpolation(xi, yi_1, x);
    l_pn_2 = Lagrange_poly_interpolation(xi, yi_2, x);
    
    n_err_1 = max(abs(f1(x)-n_pn_1));
    n_err_2 = max(abs(f2(x)-n_pn_2));
    l_err_1 = max(abs(f1(x)-l_pn_1));
    l_err_2 = max(abs(f2(x)-l_pn_2));
    
    err_t = [err_t; n_err_1 l_err_1 n_err_2 l_err_2]
end