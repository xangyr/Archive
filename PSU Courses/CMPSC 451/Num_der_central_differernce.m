function df=Num_der_central_differernce(fun,a,h)
df=(fun(a+h)-fun(a-h))/2/h;