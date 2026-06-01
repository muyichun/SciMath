import sympy
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)
SYMPY_LOCALS = {k: v for k, v in vars(sympy).items() if not k.startswith("_")}


def parse(expr_str: str, extra: dict = None) -> sympy.Basic:
    local_dict = {**SYMPY_LOCALS, **(extra or {})}
    return parse_expr(expr_str.strip(), local_dict=local_dict, transformations=TRANSFORMS)


def parse_equation(eq_str: str, extra: dict = None) -> sympy.Basic:
    """Parse 'lhs = rhs' into Eq(lhs, rhs), or just lhs (implying = 0)."""
    eq_str = eq_str.strip()
    if "==" in eq_str:
        lhs, rhs = eq_str.split("==", 1)
        return sympy.Eq(parse(lhs, extra), parse(rhs, extra))
    if "=" in eq_str:
        lhs, rhs = eq_str.split("=", 1)
        return sympy.Eq(parse(lhs, extra), parse(rhs, extra))
    return parse(eq_str, extra)


def split_list(s: str) -> list[str]:
    """Split a semicolon- or comma-separated string, stripping whitespace."""
    if ";" in s:
        return [x.strip() for x in s.split(";") if x.strip()]
    return [x.strip() for x in s.split(",") if x.strip()]


def to_latex(expr) -> str:
    return sympy.latex(expr)
