subroutine write_ppm_p6(filename, img, width, height)
  character(len=*), intent(in) :: filename
  integer, intent(in) :: width, height
  integer, dimension(width, height), intent(in) :: img
  integer :: i, j, unit
  open(newunit=unit, file=filename, form='unformatted', access='stream', status='replace')
  write(unit) 'P6', char(10)
  write(unit) trim(adjustl(itoa(width)))//' '//trim(adjustl(itoa(height)))//char(10)
  write(unit) '255', char(10)
  do j = 1, height
    do i = 1, width
      ! Write grayscale as RGB
      write(unit) achar(img(i,j)), achar(img(i,j)), achar(img(i,j))
    end do
  end do
  close(unit)
contains
  function itoa(i) result(str)
    integer, intent(in) :: i
    character(len=20) :: str
    write(str, '(I0)') i
  end function itoa
end subroutine write_ppm_p6
