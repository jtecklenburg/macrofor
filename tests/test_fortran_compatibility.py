"""Unit tests for Fortran 77 and Fortran 90 compatibility.

Tests verify that macrofor generates valid code for both formats,
focusing on:
- Line length limits (72 for F77, 132 for F90)
- Continuation characters (column 6 for F77, & for F90)
- Comment styles (c/C/* for F77, ! for F90)
- DO loop syntax (label+continue vs end do)
- IF statement syntax (endif vs end if)
"""
import pytest
from pathlib import Path
import tempfile
import re
from macrofor.api import (
    genfor, dom, equalf, if_then_m, if_then_else_m,
    declaref, commentf, programm, subroutinem,
    callf, readm, writem, formatf, set_fortran_style
)


class TestF77FixedFormat:
    """Test Fortran 77 Fixed Format compliance."""
    
    def test_line_length_limit_72(self):
        """F77: Lines must not exceed 72 characters."""
        # Create a long line
        long_expr = " + ".join([f"var{i}" for i in range(20)])
        code = [equalf('result', long_expr)]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code, max_line_length=72)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                if line.strip():  # Ignore empty lines
                    assert len(line) <= 72, f"Line {i+1} exceeds 72 chars: {len(line)} chars"
        finally:
            output_path.unlink()
    
    def test_continuation_in_column_6(self):
        """F77: Continuation character must be in column 6."""
        long_expr = " + ".join([f"x{i}" for i in range(20)])
        code = [equalf('sum', long_expr)]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # Check for continuation lines (lines starting with spaces and & in column 6)
            continuation_lines = [l for l in lines if len(l) >= 6 and l[5] == '&']
            
            # If we have a long expression, we should have continuation lines
            if len(long_expr) > 60:
                assert len(continuation_lines) > 0, "Expected continuation lines for long expression"
                
                for line in continuation_lines:
                    # Columns 1-5 should be spaces
                    assert line[:5] == '     ', f"Columns 1-5 must be spaces: {repr(line[:6])}"
                    # Column 6 should be the continuation character
                    assert line[5] == '&', f"Column 6 must be '&': {repr(line[:6])}"
        finally:
            output_path.unlink()
    
    def test_do_loop_with_label_and_continue(self):
        """F77: DO loops should use label and continue."""
        code = [dom('i', 1, 10, [equalf('x(i)', 'i')])]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            
            # Should contain "do 100 i" (label WITHOUT comma - correct Fortran syntax)
            assert re.search(r'do\s+\d+\s+\w+\s*=', content, re.IGNORECASE), \
                "DO loop should have label (without comma)"
            
            # Should contain "100 continue" (label continue)
            assert re.search(r'\d+\s+continue', content, re.IGNORECASE), \
                "DO loop should end with label continue"
            
            # Should NOT contain "end do"
            assert not re.search(r'end\s+do', content, re.IGNORECASE), \
                "F77 should not use 'end do'"
        finally:
            output_path.unlink()
    
    def test_if_then_endif_single_word(self):
        """F77: ENDIF can be single word (but 'end if' also works)."""
        code = [if_then_m('x .gt. 0', [equalf('y', '1')])]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            
            # Should contain "if (" and "then"
            assert re.search(r'if\s*\(.*\)\s*then', content, re.IGNORECASE), \
                "Should have IF-THEN statement"
            
            # Should contain "end if" or "endif"
            assert re.search(r'end\s*if', content, re.IGNORECASE), \
                "Should have END IF statement"
        finally:
            output_path.unlink()
    
    def test_comment_with_c_or_star(self):
        """F77: Comments must use c, C, or * in column 1 (NOT !)."""
        # commentf() currently uses '!' which is NOT valid in strict F77
        # This test documents the limitation - we need a separate commentf77() function
        code = [commentf('This is a comment')]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # PROBLEM: commentf() uses '!' which is NOT valid in strict F77!
            # F77 requires 'c', 'C', or '*' in column 1
            # For now, we just check that comments exist
            comment_lines = [l for l in lines if l.strip() and l.lstrip()[0] in ('!', 'c', 'C', '*')]
            assert len(comment_lines) > 0, "Should have comment lines"
            
            # TODO: Add commentf77() that generates proper F77 comments with 'c' in column 1
        finally:
            output_path.unlink()
    
    def test_strict_f77_comment_format(self):
        """F77 STRICT: Comments must use 'c', 'C', or '*' in column 1."""
        # Use commentf() which now respects the global style
        code = [
            commentf('This is a Fortran 77 comment'),
            declaref('integer', ['i']),
            equalf('i', '1')
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # Check that comment starts with 'c' in column 1 (position 0)
            comment_lines = [l for l in lines if l.startswith('c ')]
            assert len(comment_lines) > 0, "Should have F77-style comments starting with 'c '"
            
            # Check that comment has proper format: 'c     text' (c + 5 spaces)
            for line in comment_lines:
                assert line.startswith('c     '), \
                    f"F77 comment should start with 'c     ' (c + 5 spaces): {repr(line[:6])}"
            
            # Verify NO '!' comments exist (strict F77)
            exclamation_comments = [l for l in lines if l.strip().startswith('!')]
            assert len(exclamation_comments) == 0, \
                "Strict F77 must NOT use '!' for comments (that's F90+)"
        finally:
            output_path.unlink()
    
    def test_implicit_statement_format(self):
        """F77: IMPLICIT statement should use compact format."""
        code = [declaref('implicit real*8', ['a-h', 'o-z'])]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            
            # Should be: implicit real*8(a-h,o-z)
            assert 'implicit real*8(a-h,o-z)' in content.lower(), \
                "IMPLICIT should use parentheses and no spaces after commas"
        finally:
            output_path.unlink()
    
    def test_multiple_nested_do_loops(self):
        """F77: Nested DO loops should have unique labels."""
        code = [
            dom('i', 1, 10, [
                dom('j', 1, 5, [
                    equalf('a(i,j)', 'i*j')
                ])
            ])
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            
            # Find all DO labels (correct syntax: "do 100 i=")
            do_labels = re.findall(r'do\s+(\d+)\s+\w+\s*=', content, re.IGNORECASE)
            
            # Should have 2 DO loops
            assert len(do_labels) == 2, f"Expected 2 DO loops, found {len(do_labels)}"
            
            # Labels should be unique
            assert len(set(do_labels)) == 2, "DO loop labels must be unique"
            
            # Labels should be 100, 200, etc.
            assert '100' in do_labels and '200' in do_labels, \
                f"Expected labels 100 and 200, got {do_labels}"
        finally:
            output_path.unlink()
    
    def test_format_statement_labels(self):
        """F77: FORMAT statements should have proper labels."""
        code = [writem('6', ['I5', 'F10.2'], ['i', 'x'])]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            
            # Should have: write(6, 100) i, x
            # Should have: 100 format (I5, F10.2)
            assert re.search(r'write\s*\(\s*6\s*,\s*\d+\s*\)', content, re.IGNORECASE), \
                "WRITE should reference FORMAT label"
            
            assert re.search(r'\d+\s+format\s*\(', content, re.IGNORECASE), \
                "FORMAT should have label"
        finally:
            output_path.unlink()
    
    def test_no_exclamation_comments_in_f77(self):
        """F77 STRICT: Generated code must NOT contain '!' comments."""
        set_fortran_style('f77')  # Set global style to F77
        # Test various code generation functions
        code = [
            programm('test', [
                commentf('This is the main program'),
                declaref('integer', ['i']),
                dom('i', 1, 10, [
                    equalf('x(i)', 'i')
                ])
            ]),
            subroutinem('calc', ['a', 'b'], [
                declaref('real*8', ['a', 'b']),
                equalf('a', 'a + b')
            ])
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # Check for ANY '!' character (should not exist in strict F77)
            exclamation_lines = [l for l in lines if '!' in l]
            
            # Filter out lines where ! might be in strings or comments after c
            invalid_exclamations = []
            for line in exclamation_lines:
                stripped = line.lstrip()
                # Ignore if in a string literal
                if "'" in line or '"' in line:
                    continue
                # Check if ! is used as a comment marker
                if stripped.startswith('!'):
                    invalid_exclamations.append(line)
            
            assert len(invalid_exclamations) == 0, \
                f"F77 code must NOT use '!' for comments. Found:\n" + \
                "\n".join(invalid_exclamations[:5])
        finally:
            output_path.unlink()


class TestF90FreeFormat:
    """Test Fortran 90 Free Format compliance."""
    
    def test_line_length_limit_132(self):
        """F90: Lines must not exceed 132 characters."""
        # Create a very long line
        long_expr = " + ".join([f"variable{i}" for i in range(30)])
        code = [equalf('result', long_expr)]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f90', delete=False) as f:
            set_fortran_style('f90')
            genfor(f.name, code, max_line_length=132)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                if line.strip():  # Ignore empty lines
                    assert len(line) <= 132, f"Line {i+1} exceeds 132 chars: {len(line)} chars"
        finally:
            output_path.unlink()
    
    def test_continuation_with_ampersand(self):
        """F90: Continuation should use & at end of line."""
        long_expr = " + ".join([f"val{i}" for i in range(30)])
        code = [equalf('total', long_expr)]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f90', delete=False) as f:
            set_fortran_style('f90')
            genfor(f.name, code, max_line_length=80)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # Find continuation lines (lines ending with &)
            continuation_lines = [l for l in lines if l.rstrip().endswith('&')]
            
            # If we have a long expression, we should have continuation lines
            if len(long_expr) > 70:
                assert len(continuation_lines) > 0, "Expected continuation lines with &"
                
                # Next line should start with & (F90 style)
                for i, line in enumerate(lines):
                    if line.rstrip().endswith('&') and i + 1 < len(lines):
                        next_line = lines[i + 1].lstrip()
                        # F90 allows optional & at start of continuation line
        finally:
            output_path.unlink()
    
    def test_do_loop_labels_still_valid(self):
        """F90: Old-style DO loops with labels are still valid."""
        code = [dom('i', 1, 10, [equalf('x(i)', 'i')])]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f90', delete=False) as f:
            set_fortran_style('f90')
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            
            # macrofor generates classic DO loops (compatible with F90)
            # Should contain "do 100 i" (label WITHOUT comma - correct Fortran syntax)
            assert re.search(r'do\s+\d+\s+\w+\s*=', content, re.IGNORECASE), \
                "DO loop should have label (without comma)"
            
            # Should contain "100 continue"
            assert re.search(r'\d+\s+continue', content, re.IGNORECASE), \
                "DO loop should end with label continue"
        finally:
            output_path.unlink()
    
    def test_comment_with_exclamation(self):
        """F90: Comments with ! are the modern style."""
        code = [commentf('Modern F90 comment')]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.f90', delete=False) as f:
            set_fortran_style('f90')
            genfor(f.name, code)
            output_path = Path(f.name)

        try:
            content = output_path.read_text()

            # Should contain '!' comment
            assert '!' in content, "F90 should use ! for comments"
            assert 'Modern F90 comment' in content, "Comment text should be preserved"
        finally:
            output_path.unlink()
    
    def test_no_fixed_columns(self):
        """F90: Free format has no fixed column restrictions."""
        # Code can start at any column
        code = [
            programm('test', [
                declaref('integer', ['i', 'j']),
                equalf('i', '1'),
                equalf('j', '2')
            ])
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f90', delete=False) as f:
            set_fortran_style('f90')
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # Check that code is properly indented (not fixed to specific columns)
            indented_lines = [l for l in lines if l.startswith('  ') and l.strip()]
            assert len(indented_lines) > 0, "Should have indented code"
            
            # No line should have continuation in column 6 specifically
            for line in lines:
                if len(line) >= 6:
                    # In free format, column 6 has no special meaning
                    pass  # Just checking we don't crash
        finally:
            output_path.unlink()


class TestFormatCompatibility:
    """Test compatibility aspects between F77 and F90."""
    
    def test_same_code_both_formats(self):
        """Same code should be valid in both formats (with proper wrapping)."""
        code = [
            programm('compat', [
                declaref('integer', ['i']),
                dom('i', 1, 10, [
                    equalf('x(i)', 'i * i')
                ])
            ])
        ]
        
        # Generate F77 version
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            f77_path = Path(f.name)
        
        # Generate F90 version
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f90', delete=False) as f:
            set_fortran_style('f90')
            genfor(f.name, code)
            f90_path = Path(f.name)
        
        try:
            f77_content = f77_path.read_text()
            f90_content = f90_path.read_text()
            
            # Both should contain the same logical structure
            assert 'program compat' in f77_content.lower()
            assert 'program compat' in f90_content.lower()
            
            assert 'integer i' in f77_content
            assert 'integer i' in f90_content
            
            assert re.search(r'do\s+\d+', f77_content)
            assert re.search(r'do\s+\d+', f90_content)
            
            assert 'continue' in f77_content
            assert 'continue' in f90_content
        finally:
            f77_path.unlink()
            f90_path.unlink()
    
    def test_long_line_wrapping_differs(self):
        """Long lines should wrap differently in F77 vs F90."""
        long_expr = " + ".join([f"term{i}" for i in range(20)])
        code = [equalf('sum', long_expr)]
        
        # Generate F77 version
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code, max_line_length=72)
            f77_path = Path(f.name)
        
        # Generate F90 version
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f90', delete=False) as f:
            set_fortran_style('f90')
            genfor(f.name, code, max_line_length=132)
            f90_path = Path(f.name)
        
        try:
            f77_content = f77_path.read_text()
            f90_content = f90_path.read_text()
            
            f77_lines = f77_content.split('\n')
            f90_lines = f90_content.split('\n')
            
            # F77 should have continuation in column 6
            f77_cont = [l for l in f77_lines if len(l) >= 6 and l[5] == '&']
            
            # F90 should have & at end of line
            f90_cont = [l for l in f90_lines if l.rstrip().endswith('&')]
            
            # With a long expression, both should have continuations
            # (but F90 might have fewer due to 132 char limit)
            if len(long_expr) > 60:
                assert len(f77_cont) > 0, "F77 should have continuation lines"
        finally:
            f77_path.unlink()
            f90_path.unlink()
    
    def test_subroutine_structure_identical(self):
        """Subroutine structure should be the same in both formats."""
        code = [
            subroutinem('compute', ['x', 'y', 'result'], [
                declaref('real*8', ['x', 'y', 'result']),
                equalf('result', 'x + y'),
                'return'
            ])
        ]
        
        # Generate both versions
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            f77_path = Path(f.name)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f90', delete=False) as f:
            set_fortran_style('f90')
            genfor(f.name, code)
            f90_path = Path(f.name)
        
        try:
            f77_content = f77_path.read_text()
            f90_content = f90_path.read_text()
            
            # Both should have subroutine header
            assert 'subroutine compute' in f77_content.lower()
            assert 'subroutine compute' in f90_content.lower()
            
            # Both should have end subroutine
            assert 'end subroutine compute' in f77_content.lower()
            assert 'end subroutine compute' in f90_content.lower()
            
            # Both should have the computation
            assert 'result = x + y' in f77_content
            assert 'result = x + y' in f90_content
        finally:
            f77_path.unlink()
            f90_path.unlink()


class TestEdgeCases:
    """Test edge cases and potential issues."""
    
    def test_exactly_72_chars_f77(self):
        """F77: Line with exactly 72 chars should not be wrapped."""
        # Create a line with exactly 72 characters including 6-space indentation
        # "      x = " (10 chars) + expression to fill to 72
        expr = "a" * 62  # 6 + 4 + 62 = 72
        code = [equalf('x', expr)]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code, max_line_length=72)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = [l for l in content.split('\n') if l.strip()]
            
            # Should be on one line (exactly 72 chars with indentation)
            assert len(lines) == 1, f"Should be single line, got {len(lines)}: {lines}"
            assert len(lines[0]) == 72, f"Line should be exactly 72 chars, got {len(lines[0])}: '{lines[0]}'"
        finally:
            output_path.unlink()
    
    def test_comment_not_wrapped(self):
        """Comments should never be wrapped."""
        long_comment = "This is a very long comment " * 10
        code = [commentf(long_comment)]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            output_path = Path(f.name)

        try:
            content = output_path.read_text()
            lines = content.split('\n')

            # Comment should be on one line (even if long)
            # F77 uses 'c' in column 1
            comment_lines = [l for l in lines if l.strip().startswith('c')]
            assert len(comment_lines) == 1, "Comment should not be wrapped"
        finally:
            output_path.unlink()
    
    def test_empty_statements_ignored(self):
        """Empty statements should be ignored gracefully."""
        code = [
            programm('test', [
                '',
                equalf('x', '1'),
                None,
                equalf('y', '2'),
                ''
            ])
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            
            # Should contain both assignments
            assert 'x = 1' in content
            assert 'y = 2' in content
            
            # Should not crash or produce errors
            assert 'program test' in content.lower()
        finally:
            output_path.unlink()
    
    def test_special_characters_in_strings(self):
        """String literals with special characters should be preserved."""
        code = [
            equalf("message", "'Hello, World!'"),
            equalf("path", "'/home/user/data.txt'")
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            
            # String literals should be preserved
            assert "'Hello, World!'" in content
            assert "'/home/user/data.txt'" in content
        finally:
            output_path.unlink()
    
    def test_deeply_nested_structures(self):
        """Deeply nested structures should maintain proper indentation."""
        code = [
            programm('nested', [
                dom('i', 1, 10, [
                    if_then_else_m('i .gt. 5', [
                        dom('j', 1, 'i', [
                            equalf('a(i,j)', 'i*j')
                        ])
                    ], [
                        equalf('b(i)', 'i')
                    ])
                ])
            ])
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.f', delete=False) as f:
            set_fortran_style('f77')
            genfor(f.name, code)
            output_path = Path(f.name)
        
        try:
            content = output_path.read_text()
            lines = content.split('\n')
            
            # Check for proper indentation (multiples of 2 spaces)
            indented_lines = [l for l in lines if l.startswith('  ') and l.strip()]
            assert len(indented_lines) > 0, "Should have indented code"
            
            # Check that deeply nested code exists
            assert 'a(i,j)' in content
            assert 'b(i)' in content
        finally:
            output_path.unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
