
program newton_fractal
  implicit none
  integer, parameter :: width = 800, height = 800
  integer :: i, j, iter, maxiter
  double precision :: xmin, xmax, ymin, ymax
  double precision :: zr, zi, nz_re, nz_im
  double precision :: a, b, c, d, denom, nr, ni
  double precision :: x, y
  double precision :: tol, dist
  integer :: val
  integer, dimension(width,height) :: img

  tol = 1.0d-8

  xmin = -1.5d0
  xmax = 1.5d0
  ymin = -1.5d0
  ymax = 1.5d0
  maxiter = 50

  do j = 1, height
    do i = 1, width
      zr = xmin + (i-1) * (xmax - xmin) / (width - 1)
      zi = ymin + (j-1) * (ymax - ymin) / (height - 1)
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
      val = int(255.0d0 * iter / maxiter)
      img(i,j) = val
    end do
  end do

  open(unit=10, file='newton_out.pgm', status='replace')
  write(10,*) 'P2'
  write(10,*) width, height
  write(10,*) 255
  do j = 1, height
    do i = 1, width
      write(10,'(I3,1X)', advance='no') img(i,j)
    end do
    write(10,*)
  end do
  close(10)
end program newton_fractal
