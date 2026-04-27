subroutine diffusion_step(u, v, u_tmp, v_tmp, nx, ny, dx, dy, dt, D_u, D_v, factor)
  implicit none
  integer, intent(in) :: nx, ny
  real, intent(in) :: dx, dy, dt, D_u, D_v, factor
  real, intent(in) :: u(nx,ny), v(nx,ny)
  real, intent(out) :: u_tmp(nx,ny), v_tmp(nx,ny)
  integer :: i, j, im1, ip1, jm1, jp1
  
  ! Explicit diffusion (5-point Laplacian, forward Euler)
  ! factor allows for half-steps in Strang splitting
  ! With periodic boundary conditions
  ! Result is written to u_tmp/v_tmp; caller swaps arrays to avoid copy-back.
  !$omp parallel do private(i, j, im1, ip1, jm1, jp1) schedule(static)
  do j = 1, ny
    do i = 1, nx
      ! Periodic boundary conditions
      im1 = i - 1
      if (im1 < 1) im1 = nx
      ip1 = i + 1
      if (ip1 > nx) ip1 = 1
      jm1 = j - 1
      if (jm1 < 1) jm1 = ny
      jp1 = j + 1
      if (jp1 > ny) jp1 = 1
      
      u_tmp(i,j) = u(i,j) + factor * dt * D_u * ((u(ip1,j)-2.0*u(i,j)+u(im1,j))/dx**2 + &
                                                   (u(i,jp1)-2.0*u(i,j)+u(i,jm1))/dy**2)
      v_tmp(i,j) = v(i,j) + factor * dt * D_v * ((v(ip1,j)-2.0*v(i,j)+v(im1,j))/dx**2 + &
                                                   (v(i,jp1)-2.0*v(i,j)+v(i,jm1))/dy**2)
    end do
  end do
  !$omp end parallel do
end subroutine diffusion_step
