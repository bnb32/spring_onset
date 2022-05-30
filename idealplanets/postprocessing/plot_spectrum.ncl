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
  copy_VarCoords(f->UU,ke)

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

if (CONTROL.eq."True") then
  tmp = get_field(cfile,field)
else  
  tmp = get_field(infile,field)
  ctmp = get_field(cfile,field)
  ctmp_avg = dim_avg_n_Wrap(ctmp,0)
end if

dims = dimsizes(tmp)
rank=dimsizes(dims)

if (ANOMALY.eq."True").and.(CONTROL.ne."True") then
  do i=0,dims(1)-1
    do j=0,dims(2)-1
      tmp(:,i,j)=tmp(:,i,j)-ctmp_avg(i,j)
    end do
  end do
end if

if (CONTROL.ne."True") then
  delete(ctmp)
  delete(ctmp_avg)
end if

outname=outdir+field+"_avg_spectrum_"+level+"_"+case_name

if (ANOMALY.eq."True") then
  outname=outname+"_anomaly"
end if  

res = True
res@tiXAxisString = "wave number"
res@gsnScale = True               
;res@vpHeightF = 0.43        ; Changes the aspect ratio
;res@vpWidthF  = 0.85
res@gsnMaximize = True
res@trYMinF   = 0.0       
res@tiMainString  = "Power Spectrum" ; title
res@gsnXYBarChart         = True
res@gsnXYBarChartColors = "blue"
res@gsnPaperOrientation = "portrait"

array=dim_avg_n_Wrap(tmp,0)
delete(tmp)

wave_nums=ispan(0,30,1)

power = wave_number_spc(array,"F")
res@tiYAxisString = field + " Power log( "+ power@units + " )"
wks = gsn_open_wks("png",outname) 
plot = gsn_csm_xy(wks,wave_nums,log(power(0:30)),res) 
draw(plot)
;frame(wks)

print("Saved file: " + outname + ".png")
