;==========================================================    

print("infile: " + infile)
print("control: " + cfile)
print("field: " + field)
print("level: " + level)
print("AVG: " + AVG)
print("ANOMALY: " + ANOMALY)

gridType   = 1 ; fixed grid
plev       = (/ level /) ; nominal

f = addfile(infile,"r")
if (case_type.eq."drycore").and.(CONTROL.ne."True") then
  f1 = addfile(base_tref_file,"r")
  f2 = addfile(anomaly_file,"r")
  anomaly = (f2->tref(0,0,:,:))-(f1->tref(0,0,:,:))
  copy_VarCoords(f1->tref(0,0,:,:),anomaly)
  
end if
if (case_type.eq."aqua").and.(CONTROL.ne."True") then
  f1 = addfile(base_sst_file,"r")
  f2 = addfile(anomaly_file,"r")
  anomaly = (f2->SST_cpl(0,:,:))-(f1->SST_cpl(0,:,:))
  copy_VarCoords(f1->SST_cpl(0,:,:),anomaly)
end if  

function get_field(infile,field)

local tmp, tmp_new
begin

  
  f  = addfile (infile, "r")
  
  u   = f->U ; (time,lev,lat,lon) 
  v   = f->V                     
  t   = f->T ; K
  ps  = f->PS ; Pa
  z   = f->Z3 ; m
  ke  = f->UU+f->VV
  
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
    PV  = pot_vort_hybrid(p,u,v,t,t&lat, gridType, 0 )
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
  else if (field.eq."P") then
    tmp=p
    delete(p)
  else if (field.eq."KE") then
    tmp=ke
    delete(ke)

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
rank = dimsizes(dims)

if (ANOMALY.eq."True").and.(CONTROL.ne."True") then
  do i=0,dims(1)-1
    do j=0,dims(2)-1
      tmp(:,i,j)=tmp(:,i,j)-ctmp_avg(i,j)
    end do
  end do
end if

if (AVG.eq."True") then
  array = dim_avg_n_Wrap(tmp,0)
else
  array = tmp  
end if  

if (CONTROL.ne."True") then
  delete(ctmp)
  delete(ctmp_avg)
end if

if (AVG.eq."True") then
  outname=outdir+field+"_avg_"+level+"_"+case_name
else
  outname=outdir+field+"_"+level+"_"+case_name
end if

res                      = True
res@gsnMaximize          = True
res@cnFillOn             = True ; turn on color
res@cnLinesOn            = False
res@cnLineLabelsOn       = False
;res@cnLevelSelectionMode = "ManualLevels"
res@cnLevelSelectionMode = "AutomaticLevels"
res@gsnPaperOrientation  = "portrait"
res@cnConstFEnableFill = True
res@cnConstFLabelOn = False
res@mpOutlineOn = False
res@mpFillOn = False
res@gsnDraw      = False
res@gsnFrame     = False
res@gsnLeftString = ""
res@gsnRightString = ""
res@gsnPolar = "NH"
;res@lbLabelFontHeightF = "0.015"
;res@lbLabelAngleF = 90.0

minVal = min(array)
maxVal = max(array)
diff = maxVal-minVal
meanVal = avg(array)
minVal = meanVal - diff/4.0
maxVal = meanVal + diff/4.0

res@cnMinLevelValF = minVal
res@cnMaxLevelValF = maxVal
res@cnLevelSpacingF = (maxVal-minVal)/16
;symMinMaxPlt( (/ minVal,maxVal /), 16, True, res)
res@cnLevelSpacingF = 0.5*res@cnLevelSpacingF

mapres = True
mapres@gsnMaximize          = True
mapres@cnLineLabelsOn       = False
;mapres@cnLevelSelectionMode = "ManualLevels"
mapres@cnLevelSelectionMode = "AutomaticLevels"
mapres@gsnPaperOrientation  = "portrait"
mapres@cnConstFEnableFill = False
mapres@cnConstFLabelOn = False
mapres@gsnDraw      = False
mapres@gsnFrame     = False
mapres@cnFillOn = False
mapres@cnLinesOn = True
mapres@cnLineColor = "Black"
mapres@cnLineThicknessF = 4.0
mapres@gsnLeftString = ""
mapres@gsnRightString = ""

if (CONTROL.ne."True") then
  minVal := avg(anomaly)-(max(anomaly)-min(anomaly))/4.0
  maxVal := avg(anomaly)+(max(anomaly)-min(anomaly))/4.0
end if

mapres@cnMinLevelValF = minVal
mapres@cnMaxLevelValF = maxVal
mapres@cnLevelSpacingF = maxVal-minVal
;symMinMaxPlt( (/ minVal,maxVal /), 1, True, mapres)
;mapres@cnLevelSpacingF = 0.5*mapres@cnLevelSpacingF

if (rank.eq.3) then
  res@gsnCenterString = plev(0) + " hPa"
end if

if (AVG.eq."True") then 

  res@tiMainString = field+" AVG "   
  wks = gsn_open_wks("png",outname) 
  plot1 = gsn_csm_contour_map_polar(wks,array(:,:),res) 
  
  if (CONTROL.eq."True") then
    draw(plot1)
  else 
    plot2 = gsn_csm_contour(wks,anomaly,mapres)
    overlay(plot1,plot2)
    draw(plot1)
  end if

  frame(wks)

  print("Saved file: " + outname + ".png")

else
  do nt=0,dims(0)-2
    do dt=0,substeps-1
      tstep=substeps*nt+dt
      res@tiMainString = field+" - Timestep " + tstep
      tmp_outname = outname+"_"+sprinti("%0.4i",tstep)
      wks = gsn_open_wks("png",tmp_outname) 
      if (nt.eq.(dims(0)-2)) then
        tmp=array(nt,:,:)
      else
        tmp=array(nt,:,:)*(1-int2flt(dt)/substeps)+array(nt+1,:,:)*(int2flt(dt)/substeps)
      end if

      copy_VarCoords(array(nt,:,:),tmp)
      plot1 = gsn_csm_contour_map_polar(wks,tmp,res)
      
      if (CONTROL.eq."True") then
        draw(plot1)
      else 
        plot2 = gsn_csm_contour(wks,anomaly,mapres)
        overlay(plot1,plot2)
        draw(plot1)
      end if  
      
      frame(wks)

      print("timestep: " + tstep)
      print("Saved file: " + tmp_outname + ".png")

      delete(tmp)
      delete(wks)
      delete(plot1)
      
      if (CONTROL.ne."True") then
        delete(plot2)
      end if

    end do
  end do
end if  
