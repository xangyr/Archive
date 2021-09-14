function res = dec_2bin(dec)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
bin=[];
in=fix(dec);
frac=dec-in;
max=10;
while abs(in)>1e-10
    rem=mod(in,2);
    in=(in-rem)/2;
    bin=[num2str(rem) bin];
end
bin=[bin "."];
frac_str="";
while abs(max)>1e-10
    frac=frac*2;
    in=floor(frac);
    frac_str=strcat(frac_str,num2str(in));
    if in==1
        frac=frac-1;
    end
    if frac==0
        break;
    end
    max=max-1;
end
bin=[bin frac_str];
res=strcat(bin(1),bin(2),bin(3));
end

