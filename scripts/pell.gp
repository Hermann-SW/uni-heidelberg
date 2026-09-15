assert(b)={if(!(b),error())}

digmat(a)=[a,1;1,0];

find_first(v, x)={for(i=1, #v, if(v[i]==x, return(i));); return(0); }

a(i)=cf[i+1];

fundsol(d)={
  assert(type(d)=="t_INT" && !issquare(d));
  cf=contfrac(sqrt(d)); my(h=find_first(cf,2*a(0))-1); if(h%2, h*=2);
  my(d=digmat(a(0))); for(i=1, h-1, d*=digmat(a(i))); d[,1]~
};

fundpari(d)={
  assert(type(d)=="t_INT" && !issquare(d));
  my(u=quadunit(4*d)); if(norm(u)<0, u*=u); [real(u), imag(u)];
}

