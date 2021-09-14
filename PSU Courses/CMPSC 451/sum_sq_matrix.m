function sum_m = sum_sq_matrix(matrix)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

% size = size(matrix);
% a = size(1);
% b = size(2);
% for i=1:a
%     for j=1:b
%         matrix(i,j)=square(matrix(i,j));
%     end
% end
matrix = matrix.^2;
sum_m = sum(sum(matrix));
end

