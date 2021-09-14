function [f,num_sol]=shooting_nonlinear(s,h)
F=@(y,z)[z;2*y^3];
wi=[1/2;s];
num_sol=[wi(1)];
for i=1:1/h
wi= wi+F(wi(1),wi(2))*h;
num_sol=[num_sol;wi(1)];
end
f=wi(1)-1/3;