assert(b)={if(!(b),error())}

digmat(a)=[a,1;1,0];

find_first(v, x)={for(i=1, #v, if(v[i]==x, return(i));); return(0); }

fundsol(d)={
  assert(type(d)=="t_INT" && !issquare(d));
  my(cf=contfrac(sqrt(d)), a0=cf[1], h=find_first(cf,2*a0)-1); if(h%2, h*=2);
  my(d=digmat(a0)); for(i=1, h-1, d*=digmat(cf[i+1])); d[,1]~
};

fundpari(d)={
  assert(type(d)=="t_INT" && !issquare(d));
  my(u=quadunit(4*d)); if(norm(u)<0, u*=u); [real(u), imag(u)];
}

