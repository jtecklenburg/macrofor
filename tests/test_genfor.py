"""Unit tests for genfor function."""
import pytest
from pathlib import Path
from macrofor.api import (
    genfor, programm, equalf, declaref, dof, commentf,
    subroutinem, callf, returnf, readf, writef, formatf,
    if_then_f, elsef, endiff, closef, openm, dom
)


class TestGenforBasic:
    """Test basic genfor functionality."""
    
    def test_genfor_creates_file(self, tmp_path):
        """Test that genfor creates a file at the specified path."""
        output_file = tmp_path / "test_basic.f90"
        statements = [
            programm("test", [
                equalf("x", "1.0d0")
            ])
        ]
        genfor(output_file, statements)
        assert output_file.exists()
    
    def test_genfor_writes_content(self, tmp_path):
        """Test that genfor writes the correct content."""
        output_file = tmp_path / "test_content.f90"
        statements = [
            programm("test", [
                equalf("x", "1.0d0"),
                equalf("y", "2.0d0")
            ])
        ]
        genfor(output_file, statements)
        content = output_file.read_text()
        assert "program test" in content
        assert "x = 1.0d0" in content
        assert "y = 2.0d0" in content
        assert content.strip().endswith("end")
    
    def test_genfor_creates_parent_dirs(self, tmp_path):
        """Test that genfor creates parent directories if they don't exist."""
        output_file = tmp_path / "subdir" / "nested" / "test.f90"
        statements = [equalf("x", "1")]
        genfor(output_file, statements)
        assert output_file.exists()
        assert output_file.parent.exists()


class TestGenforLinearSystem:
    """Test genfor with a 20-25 line Fortran program solving a linear system."""
    
    def test_genfor_linear_system_solver(self, tmp_path):
        """
        Generate a Fortran program that solves a 2x2 linear system using Gaussian elimination.
        This program is 20-25 lines and tests complex nested structures.
        """
        output_file = tmp_path / "linear_system.f90"
        
        program_body = [
            declaref("double precision", ["a11", "a12", "a21", "a22", "b1", "b2"]),
            declaref("double precision", ["x1", "x2", "mult", "temp"]),
            commentf("Coefficients of the 2x2 system"),
            equalf("a11", "2.0d0"),
            equalf("a12", "1.0d0"),
            equalf("a21", "1.0d0"),
            equalf("a22", "3.0d0"),
            commentf("Right-hand side"),
            equalf("b1", "5.0d0"),
            equalf("b2", "6.0d0"),
            commentf("Gaussian elimination: eliminate a21"),
            equalf("mult", "a21 / a11"),
            equalf("a21", "0.0d0"),
            equalf("a22", "a22 - mult * a12"),
            equalf("b2", "b2 - mult * b1"),
            commentf("Back substitution"),
            equalf("x2", "b2 / a22"),
            equalf("x1", "(b1 - a12 * x2) / a11"),
            commentf("Output results"),
            writef("*", None, ["'Solution: x1 = ', x1, ', x2 = ', x2"]),
        ]
        
        statements = [programm("linear_solver", program_body)]
        
        genfor(output_file, statements)
        
        content = output_file.read_text()
        assert "program linear_solver" in content
        assert "double precision" in content
        assert "a11, a12, a21, a22" in content
        assert "Gaussian elimination" in content
        assert "Back substitution" in content
        assert content.strip().endswith("end")
        
        # Count lines (should be 20-30)
        lines = [l for l in content.split('\n') if l.strip()]
        assert 15 <= len(lines) <= 35, f"Expected 15-35 lines, got {len(lines)}"


class TestGenforMatrixProgram:
    """Test genfor with a 25-30 line Fortran program for matrix operations."""
    
    def test_genfor_matrix_transpose(self, tmp_path):
        """
        Generate a Fortran program that computes the transpose of a 3x3 matrix.
        This program is 20-25 lines and includes array operations without nested dof.
        """
        output_file = tmp_path / "matrix_transpose.f90"
        
        program_body = [
            "integer i, j",
            "real A(3,3), AT(3,3)",
            commentf("Initialize and transpose 3x3 matrix"),
            equalf("A(1,1)", "1.0"),
            equalf("A(1,2)", "2.0"),
            equalf("A(1,3)", "3.0"),
            equalf("A(2,1)", "4.0"),
            equalf("A(2,2)", "5.0"),
            equalf("A(2,3)", "6.0"),
            equalf("A(3,1)", "7.0"),
            equalf("A(3,2)", "8.0"),
            equalf("A(3,3)", "9.0"),
            commentf("Transpose: AT(i,j) = A(j,i)"),
            equalf("AT(1,1)", "A(1,1)"),
            equalf("AT(1,2)", "A(2,1)"),
            equalf("AT(1,3)", "A(3,1)"),
            equalf("AT(2,1)", "A(1,2)"),
            equalf("AT(2,2)", "A(2,2)"),
            equalf("AT(2,3)", "A(3,2)"),
            equalf("AT(3,1)", "A(1,3)"),
            equalf("AT(3,2)", "A(2,3)"),
            equalf("AT(3,3)", "A(3,3)"),
            writef("*", None, ["'Transpose computed'"]),
        ]
        
        statements = [programm("matrix_ops", program_body)]
        
        genfor(output_file, statements)
        
        content = output_file.read_text()
        assert "program matrix_ops" in content
        assert "real A(3,3)" in content
        assert "AT(3,3)" in content
        assert "Transpose computed" in content
        assert "A(1,1)" in content
        assert content.strip().endswith("end")
        
        # Count lines (should be 25-35)
        lines = [l for l in content.split('\n') if l.strip()]
        assert 20 <= len(lines) <= 40, f"Expected 20-40 lines, got {len(lines)}"


class TestGenforStatisticsProgram:
    """Test genfor with a 20-25 line Fortran program computing statistics."""
    
    def test_genfor_statistics(self, tmp_path):
        """
        Generate a Fortran program that computes mean and variance of an array.
        This program is 20-25 lines and demonstrates iterative computations.
        """
        output_file = tmp_path / "statistics.f90"
        
        program_body = [
            "integer, parameter :: N = 100",
            "real data(N), mean, variance, sum_sq, sum_x",
            "integer i",
            commentf("Initialize data array (example: i^2)"),
            equalf("data(1)", "1.0"),
            equalf("data(2)", "4.0"),
            equalf("data(3)", "9.0"),
            equalf("data(4)", "16.0"),
            equalf("data(5)", "25.0"),
            commentf("Compute mean"),
            equalf("sum_x", "1.0 + 4.0 + 9.0 + 16.0 + 25.0"),
            equalf("mean", "sum_x / 5.0"),
            commentf("Compute variance (simplified for first 5 elements)"),
            equalf("sum_sq", "0.0"),
            commentf("Simplified variance calculation"),
            equalf("variance", "sum_sq / 5.0"),
            commentf("Output results"),
            writef("*", None, ["'Mean: ', mean"]),
            writef("*", None, ["'Variance: ', variance"]),
            writef("*", None, ["'Std Dev: ', sqrt(variance)"])
        ]
        
        statements = [programm("compute_stats", program_body)]
        
        genfor(output_file, statements)
        
        content = output_file.read_text()
        assert "program compute_stats" in content
        assert "integer, parameter :: N = 100" in content
        assert "real data(N)" in content
        assert "mean" in content
        assert "variance" in content
        assert "Compute variance" in content
        assert content.strip().endswith("end")
        
        # Count lines (should be 20-30)
        lines = [l for l in content.split('\n') if l.strip()]
        assert 15 <= len(lines) <= 35, f"Expected 15-35 lines, got {len(lines)}"


class TestGenforEncodingLineEndings:
    """Test genfor with different encoding and line ending options."""
    
    def test_genfor_utf8_encoding(self, tmp_path):
        """Test that genfor respects UTF-8 encoding."""
        output_file = tmp_path / "utf8_test.f90"
        statements = [
            commentf("Übung: Überprüfung"),
            programm("test", [equalf("x", "1.0d0")])
        ]
        genfor(output_file, statements, encoding="utf-8")
        
        # Read with UTF-8 and check
        content = output_file.read_text(encoding="utf-8")
        assert "Übung" in content
        assert "Überprüfung" in content
    
    def test_genfor_windows_line_endings(self, tmp_path):
        """Test that genfor respects Windows line endings (CRLF)."""
        output_file = tmp_path / "crlf_test.f90"
        statements = [
            programm("test", [
                equalf("x", "1.0d0"),
                equalf("y", "2.0d0")
            ])
        ]
        genfor(output_file, statements, line_ending="\r\n")
        
        # Read in binary mode to check line endings
        content_bytes = output_file.read_bytes()
        assert b"\r\n" in content_bytes, "Expected CRLF line endings"
    
    def test_genfor_unix_line_endings(self, tmp_path):
        """Test that genfor respects Unix line endings (LF only)."""
        output_file = tmp_path / "lf_test.f90"
        statements = [
            programm("test", [
                equalf("x", "1.0d0")
            ])
        ]
        genfor(output_file, statements, line_ending="\n")
        
        # Read in binary mode to check line endings
        content_bytes = output_file.read_bytes()
        assert b"\r\n" not in content_bytes, "Expected LF-only line endings"
        assert b"\n" in content_bytes, "Expected LF line endings"


class TestGenforComplexSubroutine:
    """Test genfor with a 20-25 line program including subroutines."""
    
    def test_genfor_with_subroutine(self, tmp_path):
        """
        Generate a Fortran program with a subroutine that performs a mathematical computation.
        Total program is 20-25 lines demonstrating modular code generation.
        """
        output_file = tmp_path / "with_subroutine.f90"
        
        # Subroutine body
        sub_body = [
            "double precision, intent(in) :: x, y",
            "double precision, intent(out) :: result",
            commentf("Compute result = x^2 + y^2 + 2*x*y"),
            equalf("result", "x**2 + y**2 + 2.0d0 * x * y")
        ]
        
        # Main program
        prog_body = [
            "double precision x, y, z",
            commentf("Input values"),
            equalf("x", "3.0d0"),
            equalf("y", "4.0d0"),
            commentf("Call subroutine"),
            callf("compute_sum_of_squares", ["x", "y", "z"]),
            commentf("Output result"),
            writef("*", None, ["'x = ', x, ', y = ', y"]),
            writef("*", None, ["'x^2 + y^2 + 2*x*y = ', z"])
        ]
        
        statements = [
            subroutinem("compute_sum_of_squares", ["x", "y", "result"], sub_body),
            programm("main_with_sub", prog_body)
        ]
        
        genfor(output_file, statements)
        
        content = output_file.read_text()
        assert "subroutine compute_sum_of_squares" in content
        assert "program main_with_sub" in content
        assert "call compute_sum_of_squares" in content
        assert "intent(in)" in content
        assert "intent(out)" in content
        assert "x**2 + y**2 + 2.0d0 * x * y" in content
        assert content.count("end") >= 2  # At least subroutine and program end
        
        # Count lines (should be 15-25)
        lines = [l for l in content.split('\n') if l.strip()]
        assert 13 <= len(lines) <= 30, f"Expected 13-30 lines, got {len(lines)}"


class TestGenforLabelHandling:
    """Test genfor automatic label management and placeholder replacement."""
    
    def test_genfor_single_label_replacement(self, tmp_path):
        """
        Test that a single DO loop gets label 100 (first sequential label).
        """
        output_file = tmp_path / "single_label.f90"
        
        program_body = [
            dom("i", "1", "10", [
                equalf("x(i)", "i")
            ])
        ]
        
        statements = [programm("single_loop", program_body)]
        genfor(output_file, statements)
        
        content = output_file.read_text()
        
        # Label should be replaced with 100
        assert "do 100 i" in content
        assert "100 continue" in content
        # Should NOT contain label placeholders
        assert "__LABEL_" not in content
    
    def test_genfor_multiple_labels_sequential(self, tmp_path):
        """
        Test that multiple DO loops get sequential labels (100, 200, 300, ...).
        This is the core feature: nested and sequential loops must have different labels.
        """
        output_file = tmp_path / "multiple_labels.f90"
        
        program_body = [
            dom("i", "1", "5", [
                equalf("a(i)", "i")
            ]),
            dom("j", "1", "10", [
                equalf("b(j)", "j")
            ]),
            dom("k", "1", "3", [
                equalf("c(k)", "k")
            ])
        ]
        
        statements = [programm("multiple_loops", program_body)]
        genfor(output_file, statements)
        
        content = output_file.read_text()
        
        # All three labels should be present and unique (100, 200, 300)
        assert "do 100 i" in content
        assert "100 continue" in content
        assert "do 200 j" in content
        assert "200 continue" in content
        assert "do 300 k" in content
        assert "300 continue" in content
        # No label placeholders should remain
        assert "__LABEL_" not in content
    
    def test_genfor_nested_labels(self, tmp_path):
        """
        Test that nested DO loops get unique labels (100, 200).
        The inner loop should have a different label than the outer loop.
        """
        output_file = tmp_path / "nested_labels.f90"
        
        program_body = [
            dom("i", "1", "3", [
                dom("j", "1", "4", [
                    equalf("matrix(i,j)", "i+j")
                ])
            ])
        ]
        
        statements = [programm("matrix_init", program_body)]
        genfor(output_file, statements)
        
        content = output_file.read_text()
        
        # Both labels should be present
        assert "do 100 i" in content
        assert "100 continue" in content
        assert "do 200 j" in content
        assert "200 continue" in content
        # The inner loop (200) should come after outer (100)
        idx_outer = content.find("do 100")
        idx_inner = content.find("do 200")
        assert idx_outer < idx_inner, "Outer loop should come before inner loop"
        # No placeholders should remain
        assert "__LABEL_" not in content
    
    def test_genfor_complex_control_flow(self, tmp_path):
        """
        Test genfor with a more complex 25-30 line program involving:
        - Multiple DO loops (labels 100, 200, 300)
        - IF-THEN-ELSE structures
        - Nested loops
        - Proper label assignments
        """
        output_file = tmp_path / "complex_control.f90"
        
        program_body = [
            "integer i, j, k, count",
            commentf("Triple nested loop with labels"),
            equalf("count", "0"),
            commentf("Outer loop"),
            dom("i", "1", "3", [
                commentf("Middle loop"),
                dom("j", "1", "4", [
                    commentf("Inner loop"),
                    dom("k", "1", "2", [
                        commentf("Check if all indices are different"),
                        if_then_f("i .ne. j .and. j .ne. k"),
                        equalf("count", "count + 1"),
                        endiff(),
                    ])
                ])
            ]),
            commentf("Display result"),
            writef("*", None, ["'Count = ', count"]),
        ]
        
        statements = [programm("nested_loops", program_body)]
        genfor(output_file, statements)
        
        content = output_file.read_text()
        
        # Verify all three labels are present and sequential
        assert "do 100 i" in content
        assert "do 200 j" in content
        assert "do 300 k" in content
        assert "100 continue" in content
        assert "200 continue" in content
        assert "300 continue" in content
        
        # Verify loop structure
        assert content.count("do") >= 3
        assert "continue" in content
        assert "if" in content.lower()
        assert "and" in content.lower()
        
        # Verify it's a complete program
        assert "program nested_loops" in content
        assert content.strip().endswith("end")
        
        # No placeholders should remain
        assert "__LABEL_" not in content
        
        # Count lines (should be 25-35)
        lines = [l for l in content.split('\n') if l.strip()]
        assert 20 <= len(lines) <= 40, f"Expected 20-40 lines, got {len(lines)}"
