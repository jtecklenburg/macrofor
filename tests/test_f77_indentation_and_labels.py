"""
Test F77 indentation and label formatting.

These tests verify that macrofor correctly formats F77 fixed format code:
1. Regular statements are indented with 6 spaces (column 7+)
2. Labels are right-aligned in columns 1-5
3. Comments start in column 1
"""

import tempfile
from pathlib import Path
import pytest
from macrofor.api import (
    set_fortran_style,
    genfor,
    declaref,
    equalf,
    dom,
    formatf,
    subroutinem,
    programm,
    commentf,
)


class TestF77Indentation:
    """Test proper F77 indentation (6 spaces for statements)."""

    def test_simple_statement_indentation(self):
        """F77: Simple statements should have 6-space indentation."""
        set_fortran_style('f77')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            code = [
                declaref('real*8', ['x', 'y', 'z']),
                equalf('x', '1.0'),
                equalf('y', '2.0'),
            ]
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = [l for l in content.split('\n') if l.strip()]
            
            # All lines should start with exactly 6 spaces
            for line in lines:
                assert line.startswith('      '), f"Line should have 6-space indent: '{line}'"
                assert not line.startswith('       '), f"Line should not have >6 space indent: '{line}'"
        finally:
            output_path.unlink()

    def test_subroutine_body_indentation(self):
        """F77: Subroutine body should have 6-space indentation."""
        set_fortran_style('f77')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            code = [
                subroutinem('compute', ['x', 'y'], [
                    declaref('real*8', ['x', 'y', 'result']),
                    equalf('result', 'x + y'),
                ])
            ]
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # Find body lines (skip comments and subroutine declaration)
            body_lines = []
            in_body = False
            for line in lines:
                if line.strip().startswith('subroutine'):
                    in_body = True
                    continue
                if line.strip().startswith('end subroutine'):
                    break
                if in_body and line.strip() and not line.strip().startswith('c'):
                    body_lines.append(line)
            
            # Body statements should have 6-space indentation
            assert len(body_lines) >= 2, "Should have at least 2 body statements"
            for line in body_lines:
                assert line.startswith('      '), f"Body line should have 6-space indent: '{line}'"
        finally:
            output_path.unlink()

    def test_program_body_indentation(self):
        """F77: Program body should have 6-space indentation."""
        set_fortran_style('f77')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            code = [
                programm('test', [
                    declaref('real*8', ['x']),
                    equalf('x', '42.0'),
                ])
            ]
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # Find body lines (between program and end)
            body_lines = []
            in_body = False
            for line in lines:
                if line.strip().startswith('program'):
                    in_body = True
                    continue
                if line.strip() == 'end':
                    break
                if in_body and line.strip():
                    body_lines.append(line)
            
            # All body statements should have 6-space indentation
            for line in body_lines:
                assert line.startswith('      '), f"Body line should have 6-space indent: '{line}'"
        finally:
            output_path.unlink()


class TestF77Labels:
    """Test proper F77 label formatting (right-aligned in columns 1-5)."""

    def test_do_loop_label_format(self):
        """F77: DO loop labels should be right-aligned in columns 1-5."""
        set_fortran_style('f77')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            code = [
                dom('i', 1, 10, [equalf('x(i)', 'i * 2')])
            ]
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # Find the continue line with label
            continue_line = None
            for line in lines:
                if 'continue' in line and any(c.isdigit() for c in line[:6]):
                    continue_line = line
                    break
            
            assert continue_line is not None, "Should have a labeled continue statement"
            
            # Extract label area (columns 1-5)
            label_area = continue_line[:5]
            
            # Label should be right-aligned (spaces, then digits)
            assert label_area.strip().isdigit(), f"Label area should contain only digits: '{label_area}'"
            assert label_area[0] == ' ', f"Label should not start in column 1: '{label_area}'"
            
            # Label number should be a multiple of 100 (100, 200, 300, ...)
            label_num = int(label_area.strip())
            assert label_num % 100 == 0, f"Label should be multiple of 100, got {label_num}"
            assert label_num >= 100, f"Label should be >= 100, got {label_num}"
        finally:
            output_path.unlink()

    def test_format_statement_label(self):
        """F77: FORMAT statement labels should be right-aligned in columns 1-5."""
        set_fortran_style('f77')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            code = [
                formatf(['I5', 'F10.2', 'A20'])
            ]
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = [l for l in content.split('\n') if l.strip()]
            
            assert len(lines) == 1, "Should have exactly one format statement"
            format_line = lines[0]
            
            # Should contain 'format'
            assert 'format' in format_line.lower()
            
            # Label area (columns 1-5)
            label_area = format_line[:5]
            
            # Should be right-aligned digits
            assert label_area.strip().isdigit(), f"Label area should be digits: '{label_area}'"
            assert label_area[0] == ' ', f"Label should not start in column 1: '{label_area}'"
        finally:
            output_path.unlink()

    def test_multiple_labels_sequential(self):
        """F77: Multiple labels should be sequential (100, 200, 300, ...)."""
        set_fortran_style('f77')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            code = [
                dom('i', 1, 10, [equalf('x(i)', 'i')]),
                dom('j', 1, 5, [equalf('y(j)', 'j * 2')]),
                formatf(['I5']),
                formatf(['F10.2']),
            ]
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # Extract all labels
            labels = []
            for line in lines:
                if line and any(c.isdigit() for c in line[:6]):
                    if 'continue' in line or 'format' in line:
                        label_area = line[:5].strip()
                        if label_area.isdigit():
                            labels.append(int(label_area))
            
            # Should have 4 labels (2 from do loops, 2 from format)
            assert len(labels) == 4, f"Should have 4 labels, got {len(labels)}: {labels}"
            
            # Should be sequential: 100, 200, 300, 400
            expected = [100, 200, 300, 400]
            assert labels == expected, f"Labels should be {expected}, got {labels}"
        finally:
            output_path.unlink()


class TestF77Comments:
    """Test F77 comment formatting (column 1)."""

    def test_comment_in_column_one(self):
        """F77: Comments should start in column 1."""
        set_fortran_style('f77')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            code = [
                commentf('This is a test comment'),
                declaref('real*8', ['x']),
                commentf('Another comment'),
            ]
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # Find comment lines
            comment_lines = [l for l in lines if l.strip().startswith('c')]
            
            assert len(comment_lines) >= 2, "Should have at least 2 comment lines"
            
            for line in comment_lines:
                assert line[0] == 'c', f"Comment should start in column 1: '{line}'"
                assert not line.startswith(' '), f"Comment should not be indented: '{line}'"
        finally:
            output_path.unlink()


class TestF90Comparison:
    """Test that F90 behaves differently (2-space indent, no column restrictions)."""

    def test_f90_uses_2_space_indent(self):
        """F90: Nested statements should have 2-space indentation, not 6."""
        set_fortran_style('f90')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f90', delete=False) as f:
            code = [
                programm('test', [
                    declaref('real*8', ['x', 'y']),
                    equalf('x', '1.0'),
                ])
            ]
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # Find body lines (between program and end)
            body_lines = []
            in_body = False
            for line in lines:
                if line.strip().startswith('program'):
                    in_body = True
                    continue
                if line.strip() == 'end':
                    break
                if in_body and line.strip():
                    body_lines.append(line)
            
            # F90 nested statements should use 2-space indent
            assert len(body_lines) >= 2, "Should have at least 2 body statements"
            for line in body_lines:
                assert line.startswith('  '), f"F90 nested line should have 2-space indent: '{line}'"
                assert not line.startswith('      '), f"F90 should not have 6-space indent: '{line}'"
        finally:
            output_path.unlink()

    def test_f90_labels_not_in_column_format(self):
        """F90: Labels don't need to be in fixed columns."""
        set_fortran_style('f90')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f90', delete=False) as f:
            code = [
                dom('i', 1, 10, [equalf('x(i)', 'i')])
            ]
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # Find continue line
            continue_line = None
            for line in lines:
                if 'continue' in line and any(c.isdigit() for c in line):
                    continue_line = line
                    break
            
            assert continue_line is not None
            
            # In F90, label can be anywhere at start (with some indentation)
            # It should NOT be strictly in columns 1-5
            assert not continue_line.startswith('  1'), "F90 label should be formatted differently than F77"
        finally:
            output_path.unlink()


class TestMixedContent:
    """Test combinations of statements, labels, and comments."""

    def test_f77_complete_subroutine(self):
        """F77: Complete subroutine with statements, loops, and labels."""
        set_fortran_style('f77')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            code = [
                subroutinem('process', ['n'], [
                    commentf('Loop through array'),
                    dom('i', 1, 'n', [
                        equalf('x(i)', 'i * 2'),
                    ]),
                    commentf('Format for output'),
                    formatf(['I5', 'F10.2']),
                ])
            ]
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # Check comments are in column 1
            comment_lines = [l for l in lines if l.strip().startswith('c')]
            for line in comment_lines:
                assert line[0] == 'c', f"Comment should be in column 1: '{line}'"
            
            # Check regular statements have 6-space indent
            stmt_lines = [l for l in lines if l.strip() and 
                         not l.strip().startswith(('c', 'subroutine', 'end')) and
                         not any(c.isdigit() for c in l[:6])]
            for line in stmt_lines:
                if line.startswith('      do '):  # DO statement
                    assert True  # Expected
                elif line.strip():
                    assert line.startswith('      '), f"Statement should have 6-space indent: '{line}'"
            
            # Check labels are in columns 1-5
            label_lines = [l for l in lines if any(c.isdigit() for c in l[:6]) and 
                          ('continue' in l or 'format' in l)]
            for line in label_lines:
                label_area = line[:5]
                assert label_area.strip().isdigit(), f"Label area should be digits: '{label_area}'"
        finally:
            output_path.unlink()
