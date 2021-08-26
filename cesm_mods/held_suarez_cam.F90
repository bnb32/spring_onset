#define MODHS 1
#undef MODHS
module held_suarez_cam
 ! --------------------------------------------------------------
 ! modified to read in relaxation temperature profile from file
 ! Mods are denoted by
 ! 
 ! !TREF-READ
 !    blah blah blah
 ! !END TREF-READ
 !
 ! New subroutines:
 ! trefread_readnl = allows namelist parameters controlling the
 !                   relaxation temperature profile to be read in
 !   

 ! Isla Simpson 24th Feb 2017
 ! Updated for CESM 2 release, Isla Simpson, 31st May 2018
 ! --------------------------------------------------------------

  use shr_kind_mod, only: r8 => shr_kind_r8
  !TREF-READ
 ! use ppgrid,       only: pcols, pver
  use ppgrid,  only: pcols, pver, begchunk, endchunk
  use spmd_utils , only: mpicom,mstrid=>masterprocid, mpi_integer, mpi_real8, &
                        mpi_logical, mpi_character, masterproc
  use cam_abortutils , only: endrun
  use cam_logfile, only : iulog
  !END TREF-READ


  implicit none
  private
  save

  public :: held_suarez_init, held_suarez_tend

  !TREF-READ
  public :: trefread_readnl
  !END TREF-READ 

  real(r8), parameter :: efoldf  =  1._r8  ! efolding time for wind dissipation
  real(r8), parameter :: efolda  = 40._r8  ! efolding time for T dissipation
  real(r8), parameter :: efolds  =  4._r8  ! efolding time for T dissipation
  real(r8), parameter :: sigmab  =  0.7_r8 ! threshold sigma level
  real(r8), parameter :: t00     = 200._r8 ! minimum reference temperature
  real(r8), parameter :: kf      = 1._r8/(86400._r8*efoldf) ! 1./efolding_time for wind dissipation

  real(r8), parameter :: onemsig = 1._r8 - sigmab ! 1. - sigma_reference

  real(r8), parameter :: ka      = 1._r8/(86400._r8 * efolda) ! 1./efolding_time for temperature diss.
  real(r8), parameter :: ks      = 1._r8/(86400._r8 * efolds)

  !TREF-READ
  character(len=256) :: treffile
  logical:: treffromfile
  real(r8),allocatable::tref(:,:,:) ! relaxation temperature read from file
  !TREF-READ


!======================================================================= 
contains
!======================================================================= 

  subroutine held_suarez_init(pbuf2d)
    use physics_buffer,     only: physics_buffer_desc
    use cam_history,        only: addfld, add_default
    use physconst,          only: cappa, cpair
    use ref_pres,           only: pref_mid_norm, psurf_ref
    use held_suarez,        only: held_suarez_1994_init

    !TREF-READ
    use error_messages, only: alloc_err
    !END TREF-READ

    type(physics_buffer_desc), pointer :: pbuf2d(:,:)

    !QPERT-READ
    integer :: istat
    !END QPERT-READ


    ! Set model constant values
    call held_suarez_1994_init(cappa, cpair, psurf_ref, pref_mid_norm)

    !TREF-READ
     allocate(tref(pcols,pver,begchunk:endchunk),stat=istat)
     call alloc_err(istat,'UPDATE_TREF_EUL','tref',pcols*pver*(endchunk-begchunk))
     tref(:pcols,:pver,begchunk:endchunk)=0._r8
     if (treffromfile) then
      call update_tref(treffile)
     endif
    !END TREF-READ


    ! This field is added by radiation when full physics is used
    call addfld('QRS', (/ 'lev' /), 'A', 'K/s', &
         'Temperature tendency associated with the relaxation toward the equilibrium temperature profile')
    call add_default('QRS', 1, ' ')
 end subroutine held_suarez_init

  subroutine held_suarez_tend(state, ptend, ztodt)
    !----------------------------------------------------------------------- 
    ! 
    ! Purpose: 
    !  algorithm 1: Held/Suarez IDEALIZED physics
    !  algorithm 2: Held/Suarez IDEALIZED physics (Williamson modified stratosphere
    !  algorithm 3: Held/Suarez IDEALIZED physics (Lin/Williamson modified strato/meso-sphere
    !
    ! Author: J. Olson
    ! 
    !-----------------------------------------------------------------------
    use physconst,          only: cpairv
    use phys_grid,          only: get_rlat_all_p
    use physics_types,      only: physics_state, physics_ptend
    use physics_types,      only: physics_ptend_init
    use cam_abortutils,     only: endrun
    use cam_history,        only: outfld
    use held_suarez,        only: held_suarez_1994

    !
    ! Input arguments
    !
    type(physics_state), intent(inout) :: state
    real(r8),            intent(in)    :: ztodt            ! Two times model timestep (2 delta-t)
                                                           !
                                                           ! Output argument
                                                           !
    type(physics_ptend), intent(out)   :: ptend            ! Package tendencies
                                                           !
    !---------------------------Local workspace-----------------------------

    integer                            :: lchnk            ! chunk identifier
    integer                            :: ncol             ! number of atmospheric columns

    real(r8)                           :: clat(pcols)      ! latitudes(radians) for columns
    real(r8)                           :: pmid(pcols,pver) ! mid-point pressure
    integer                            :: i, k             ! Longitude, level indices

    !TREF-READ
    real (r8)                          :: treflchnk(pcols,pver) ! Tref of current chunk                        !END TREF-READ


    !
    !-----------------------------------------------------------------------
    !

    lchnk = state%lchnk
    ncol  = state%ncol

    call get_rlat_all_p(lchnk, ncol, clat)
    do k = 1, pver
      do i = 1, ncol
        pmid(i,k) = state%pmid(i,k)
        !TREF-READ
        if (treffromfile) then
          treflchnk(i,k)=tref(i,k,lchnk)
        end if
        !END TREF-READ
      end do
    end do

    ! initialize individual parameterization tendencies
    call physics_ptend_init(ptend, state%psetcols, 'held_suarez', ls=.true., lu=.true., lv=.true.)

    !TREF-READ
    if (treffromfile) then
    call held_suarez_1994(pcols, ncol, clat, pmid, &
         state%u, state%v, state%t, ptend%u, ptend%v, ptend%s, treflchnk)
    else
    call held_suarez_1994(pcols, ncol, clat, pmid, &
         state%u, state%v, state%t, ptend%u, ptend%v, ptend%s)
    end if !treffromfile 
    !END TREF-READ

    ! Note, we assume that there are no subcolumns in simple physics
    pmid(:ncol,:) = ptend%s(:ncol, :)/cpairv(:ncol,:,lchnk)
    if (pcols > ncol) then
      pmid(ncol+1:,:) = 0.0_r8
    end if
    call outfld('QRS', pmid, pcols, lchnk)

  end subroutine held_suarez_tend

  !TREF-READ
    subroutine trefread_readnl(nlfile)
! -----------------------------------------------------------------------
! Read in namelist parameters treffromfile and treffile
! treffile = controls whether the relaxation temperature profile
! is the default (treffile=.False.) or is read in from
! file (treffile=.True.) 
! Isla Simpson (24th Feb 17)
! -----------------------------------------------------------------------
    use namelist_utils  ,only:find_group_name
    use units           ,only:getunit,freeunit
    character(len=*),intent(in)::nlfile
    integer :: unitn, ierr
    character(len=*), parameter :: sub = 'trefread_readnl'


    namelist /trefread_nl/ treffromfile,treffile

    !Set default namelist values
    treffromfile=.False.
    treffile='randomfile'

    !Read in namelist values
    if (masterproc) then
     unitn = getunit()
     open(unitn,file=trim(nlfile),status='old')
     call find_group_name(unitn,'trefread_nl',status=ierr)
     if (ierr.eq.0) then
       read(unitn,trefread_nl,iostat=ierr)
       if (ierr.ne.0) then
         call endrun('trefread_readnl:: ERROR reading namelist')
       endif
     endif
     close(unitn)
     call freeunit(unitn)
    endif


   call mpi_bcast(treffromfile   , 1, mpi_logical, mstrid, mpicom, ierr)
   if (ierr /= 0) call endrun(sub//": FATAL: mpi_bcast: held_suarez_1994")
   call mpi_bcast(treffile       , len(treffile), mpi_character, mstrid, mpicom, ierr)
   if (ierr /= 0) call endrun(sub//": FATAL: mpi_bcast: held_suarez_1994")

   return
  end subroutine
!END TREF-READ 

  !TREF-READ
  subroutine update_tref(treffilein)
  ! --------------------------------
  ! Read in relaxation temperature profile from a netcdf file 
  ! Isla Simpson 31st May 2018
  ! --------------------------------
   use cam_grid_support, only: cam_grid_get_dim_names, cam_grid_id
   use pio, only: pio_nowrite, file_desc_t, pio_closefile
   use ioFileMod, only: getfil
   use cam_pio_utils, only: cam_pio_openfile
   use ncdio_atm, only: infld

   character(len=*), intent(in) :: treffilein
   character(len=8) :: dim1name, dim2name
   integer :: grid_id
   type(file_desc_t), pointer :: ncidtref
   character(len=256) :: trefpath
   logical :: found=.false.

   grid_id = cam_grid_id('physgrid')
   call cam_grid_get_dim_names(grid_id, dim1name, dim2name)

   allocate(ncidtref)
   call getfil(treffilein, trefpath)
   call cam_pio_openfile(ncidtref, trim(trefpath), PIO_NOWRITE)
   call infld('tref',ncidtref,dim1name,'lev',dim2name,1,pcols,1,pver, &
     begchunk,endchunk, tref, found, gridname='physgrid')
   if (.not.found) then
      write(iulog,*) 'TREF, variable tref not found in input file ',treffile
    call endrun('TREF :: Error, variable tref not found in input file')
  end if


  call pio_closefile(ncidtref)
  end subroutine
  !------------------------------------------
  !END TREF-READ






end module held_suarez_cam
