;==========================================================    

print("control: " + cfile)
print("field: " + field)
print("level: " + level)
print("AVG: " + AVG)

gridType   = 1 ; fixed grid
plev       = (/ level /) ; nominal

f = addfile(cfile,"r")

function get_field(infile,field)

local tmp, tmp_new
begin

  
  f  = addfile (infile, "r")
  
  u   = f->U ; (time,lev,lat,lon) 
  v   = f->V                     
  t   = f->T ; K
  ps  = f->PS ; Pa
  z   = f->Z3 ; m
  
  hyam = f->hyam
  hybm = f->hybm
  p0   = f->P0 ; p0=100000
  p0mb = p0/100
  ps@long_name = "surface pressure"
 
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

tmp = get_field(cfile,field)

dims = dimsizes(tmp)
rank = dimsizes(dims)

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
res@cnLevelSelectionMode = "ManualLevels"
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
;res@trGridType = "TriangularMesh"

minVal = min(tmp(dims(0)-2,:,:))/2
maxVal = max(tmp(dims(0)-2,:,:))/2
;res@cnMinLevelValF = min(tmp)
;res@cnMaxLevelValF = max(tmp)
;res@cnLevelSpacingF = (max(tmp)-min(tmp))/16
symMinMaxPlt( (/ minVal,maxVal /), 16, True, res)
res@cnLevelSpacingF = 0.5*res@cnLevelSpacingF

if (rank.eq.3) then
  res@gsnCenterString = plev(0) + " hPa"
end if

if (AVG.eq."True") then
  array=dim_avg_n_Wrap(tmp,0)
else
  array=tmp
end if
delete(tmp)

if (AVG.eq."True") then 
  
  res@tiMainString = field+" AVG"   
  wks = gsn_open_wks("pdf",outname) 
  plot1 = gsn_csm_contour_map_polar(wks,array(:,:),res) 
  ;plot1 = gsn_csm_contour_map(wks,array(:,:),res) 
  
  draw(plot1)
  frame(wks)

else
  do nt=0,dims(0)-2
    do dt=0,substeps-1
      tstep=substeps*nt+dt
      res@tiMainString = field+" - Timestep " + tstep   
      wks = gsn_open_wks("pdf",outname+"_"+sprinti("%0.4i",tstep)) 
      if (nt.eq.(dims(0)-2)) then
        tmp=array(nt,:,:)
      else
        tmp=array(nt,:,:)*(1-int2flt(dt)/substeps)+array(nt+1,:,:)*(int2flt(dt)/substeps)
      end if

      copy_VarCoords(array(nt,:,:),tmp)
      ;plot1 = gsn_csm_contour_map(wks,tmp,res)
      plot1 = gsn_csm_contour_map_polar(wks,tmp,res)
      
      draw(plot1)
      frame(wks)

      print("timestep: " + tstep)
      delete(tmp)
      delete(wks)
      delete(plot1)
      
    end do
  end do
end if  
