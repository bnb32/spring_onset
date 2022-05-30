;==========================================================    

print("infile: " + infile)
print("control: " + cfile)
print("field: " + field)
print("level: " + level)

gridType   = 1 ; fixed grid
plev       = (/ level /) ; nominal

function get_field(infile,field)

local tmp, tmp_new
begin

  f  = addfile (infile, "r")
  
  u   = f->U ; (time,lev,lat,lon)
  v   = f->V   
  t   = f->T ; K
  ps  = f->PS ; Pa
  z   = f->Z3 ; m
  ke  = f->UU + f->VV
  
  hyam = f->hyam
  hybm = f->hybm
  p0   = f->P0 ; p0=100000
  p0mb = p0/100
  ps@long_name = "surface pressure"
  
  ke@long_name = "kinetic energy"
  ke@units = f->UU@units

  if ((field.eq."P").or.(field.eq."PV")) then
    p = pres_hybrid_ccm (ps,p0,hyam,hybm) 
    copy_VarCoords(t, p)
    p@units = ps@units
    p@long_name = "hybrid pressure levels"
  end if

  delete(f)

  if (field.eq."PV") then
    PV = pot_vort_hybrid(p,u,v,t,t&lat, gridType, 0 )
    printVarSummary(PV)
    printMinMax(PV,0)
  end if
  
  if (field.eq."PV") then
    tmp=PV
    delete(PV)
  else if (field.eq."Z3") then
    tmp=z
    delete(z)
  else if (field.eq."U") then
    tmp=u
    delete(u)
  else if (field.eq."V") then
    tmp=v
    delete(v)
  else if (field.eq."T") then
    tmp=t
    delete(t)
  else if (field.eq."PS") then
    tmp=ps
    delete(ps)
  else if (field.eq."KE") then
    tmp=ke
    delete(ke)
  else if (field.eq."P") then
    tmp=p
    delete(p)

  end if
  end if  
  end if  
  end if
  end if
  end if
  end if
  end if
  
  rank=dimsizes(dimsizes(tmp))
  
  interp = 2
  extrap = False

  if (rank.eq.4) then
    tmp_new = vinth2p(tmp,hyam,hybm,plev,ps,interp,p0mb,1,extrap)
    tmp_new@units = tmp@units
    delete(tmp)
    tmp = tmp_new(:,{plev(0)},:,:)
    delete(tmp_new)
  end if
  return(tmp)
end

;************************************************
; create plots
;************************************************

tmp1 = get_field(infile,field)
tmp2 = get_field(cfile,field)
ctmp = dim_avg_n_Wrap(tmp2,0)
tmp = tmp1

dims = dimsizes(tmp)
rank=dimsizes(dims)

do i=0,dims(1)-1
  do j=0,dims(2)-1
    tmp(:,i,j)=tmp(:,i,j)-ctmp(i,j)
  end do
end do

copy_VarCoords(tmp1, tmp)
delete(tmp1)
delete(tmp2)
delete(ctmp)

do t=7,dims(0)-2
  mean0=avg(wave_number_spc(dim_avg_n_Wrap(tmp(t-7:t-1,:,:),0),"F"))
  mean1=avg(wave_number_spc(dim_avg_n_Wrap(tmp(t-6:t,:,:),0),"F"))
  frac_diff=(mean1-mean0)/mean0
  print(t + ", " + frac_diff)
end do  
