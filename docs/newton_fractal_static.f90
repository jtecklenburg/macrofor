
program newton_fractal
  use, intrinsic :: iso_fortran_env, only: int8
  implicit none
  integer, parameter :: width = 800, height = 800
  integer, parameter :: supersample = 4
  integer :: i, j, si, sj, iter, maxiter
  double precision :: xmin, xmax, ymin, ymax
  double precision :: zr, zi, nz_re, nz_im
  double precision :: a, b, c, d, denom, nr, ni
  double precision :: x, y
  double precision :: tol, dist
  integer :: val
  integer, dimension(width,height) :: img
  double precision :: sumval
  double precision :: dx, dy

  tol = 1.0d-8

  xmin = -1.5d0
  xmax = 1.5d0
  ymin = -1.5d0
  ymax = 1.5d0
  maxiter = 30

  dx = (xmax - xmin) / (width - 1)
  dy = (ymax - ymin) / (height - 1)

  !$omp parallel do
  do j = 1, height
    do i = 1, width
      sumval = 0.0d0
      do sj = 0, supersample-1
        do si = 0, supersample-1
          zr = xmin + (i-1 + (si+0.5d0)/supersample) * dx
          zi = ymin + (j-1 + (sj+0.5d0)/supersample) * dy
          x = zr
          y = zi
          iter = 0
          do while (iter < maxiter)
            ! include dynamic evaluation of f and f' (a,b,c,d)
            include 'newton_dynamic.inc'
            ! static Newton update (expressed with a,b,c,d)
            denom = c*c + d*d
            nr = a*c + b*d
            ni = b*c - a*d
            nz_re = zr - nr/denom
            nz_im = zi - ni/denom
            ! Check convergence
            dist = sqrt((nz_re - zr)**2 + (nz_im - zi)**2)
            if (dist < tol) exit
            zr = nz_re
            zi = nz_im
            x = zr
            y = zi
            iter = iter + 1
          end do
          sumval = sumval + dble(iter)
        end do
      end do
      val = int(255.0d0 * sumval / (maxiter * supersample * supersample))
      img(i,j) = val
    end do
  end do

  call write_ppm_p6('newton_out.ppm', img, width, height)
end program newton_fractal
