import logging
from typing import Any, Generator

import sympy
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.sympy_utils import SYMPY_LOCALS, TRANSFORMS, to_latex
from sympy.parsing.sympy_parser import parse_expr


def _build_ode_locals(var_name: str, func_name: str) -> dict:
    """Build a parse namespace with the independent variable and function object."""
    var = sympy.Symbol(var_name)
    func = sympy.Function(func_name)
    return {**SYMPY_LOCALS, var_name: var, func_name: func, "Function": sympy.Function}


class SympyDSolveTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        ode_str = tool_parameters.get("ode", "").strip()
        func_str = tool_parameters.get("func", "f(x)").strip() or "f(x)"
        ics_str = tool_parameters.get("ics", "").strip()

        if not ode_str:
            yield self.create_text_message("Error: ode parameter is required.")
            return

        try:
            # Parse func like "f(x)" to get func_name="f", var_name="x"
            if "(" in func_str and ")" in func_str:
                func_name = func_str[: func_str.index("(")].strip()
                var_name = func_str[func_str.index("(") + 1 : func_str.index(")")].strip()
            else:
                func_name = func_str.strip()
                var_name = "x"

            local_dict = _build_ode_locals(var_name, func_name)
            var = local_dict[var_name]
            func = local_dict[func_name]
            func_applied = func(var)

            # Parse ODE expression (left side only, assuming = 0 if no =)
            ode_expr_str = ode_str
            if "=" in ode_str and "==" not in ode_str:
                lhs, rhs = ode_str.split("=", 1)
                ode_eq = sympy.Eq(
                    parse_expr(lhs.strip(), local_dict=local_dict, transformations=TRANSFORMS),
                    parse_expr(rhs.strip(), local_dict=local_dict, transformations=TRANSFORMS),
                )
            else:
                ode_eq = parse_expr(ode_str, local_dict=local_dict, transformations=TRANSFORMS)

            # Parse initial conditions if provided (format: "f(0)=1, Derivative(f(0),x)=0")
            ics = None
            if ics_str:
                ics = {}
                for ic in ics_str.split(";"):
                    ic = ic.strip()
                    if "=" in ic:
                        lhs, rhs = ic.split("=", 1)
                        lhs_expr = parse_expr(
                            lhs.strip(), local_dict=local_dict, transformations=TRANSFORMS
                        )
                        rhs_expr = parse_expr(
                            rhs.strip(), local_dict=local_dict, transformations=TRANSFORMS
                        )
                        ics[lhs_expr] = rhs_expr

            solution = sympy.dsolve(ode_eq, func_applied, ics=ics)

            ode_latex = to_latex(ode_eq)
            sol_latex = to_latex(solution)

            text = f"**微分方程解**\n\n方程：\n\n$$\n{ode_latex}\n$$\n\n"
            if ics:
                text += f"初始条件：{ics_str}\n\n"
            text += f"通解：\n\n$$\n{sol_latex}\n$$"

            yield self.create_text_message(text)
            yield self.create_json_message(
                {
                    "operation": "dsolve",
                    "ode": ode_str,
                    "func": func_str,
                    "ics": ics_str or None,
                    "solution": str(solution),
                    "solution_latex": sol_latex,
                    "result_markdown": f"$$\n{sol_latex}\n$$",
                }
            )

        except Exception as e:
            logging.exception("sympy_dsolve error")
            yield self.create_text_message(
                f"Error solving ODE: {e}\n"
                f"Tip: express ODE using f(x).diff(x) for f'(x), f(x).diff(x,2) for f''(x).\n"
                f"Example: 'f(x).diff(x) - f(x)' solves f'(x) = f(x)."
            )
