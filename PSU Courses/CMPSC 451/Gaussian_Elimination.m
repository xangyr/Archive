function x=Gaussian_Elimination(A,b)
%Input:     A--a nXn matrix  b--a nX1 vector
%Output:    x--a nX1 vector s.t. Ax=b
n=size(A,1);
Aug=[A b];
for i=1:n-1%Step 1    
    for j=i+1:n
        Aug(j,:)=Aug(j,:)-Aug(j,i)/Aug(i,i)*Aug(i,:);
    end
end
x=zeros(n,1);%Step 2
A=Aug(:,1:n);
b=Aug(:,n+1);
x(n)=b(n)/A(n,n);
for i=n-1:-1:1
    x(i)=b(i);
    for j=i+1:n
        x(i)=x(i)-A(i,j)*x(j);
    end
    x(i)=x(i)/A(i,i);
end

