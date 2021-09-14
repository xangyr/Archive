function df = num_der(f,a,h)
df = (f(a-2*h)-8.*f(a-h)+8.*f(a+h)-f(a+2*h))/h/12;
end

