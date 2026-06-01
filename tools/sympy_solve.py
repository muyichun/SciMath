import logging
from typing import Any, Generator

import sympy
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.sympy_utils import parse_equation, split_list, to_latex


class SympySolveTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        equations_str = tool_parameters.get("equations", "").strip()
        variables_str = tool_parameters.get("variables", "").strip()

        if not equations_str:
            yield self.create_text_message("Error: equations parameter is required.")
            return

        try:
            eq_strs = split_list(equations_str)
            equations = [parse_equation(s) for s in eq_strs]

            if variables_str:
                var_names = split_list(variables_str)
                variables = [sympy.Symbol(v) for v in var_names]
            else:
                variables = sorted(
                    {s for eq in equations for s in eq.free_symbols},
                    key=lambda s: s.name,
                )

            if len(equations) == 1:
                solutions = sympy.solve(equations[0], variables if len(variables) > 1 else variables[0])
            else:
                solutions = sympy.solve(equations, variables)

            eq_latex = [to_latex(eq) for eq in equations]
            sol_latex = to_latex(solutions)

            eq_display = " ,\\ ".join(eq_latex)
            text = (
                f"**解方程结果**\n\n"
                f"方程：\n\n"
                f"$$\n{eq_display}\n$$\n\n"
                f"变量：{', '.join(str(v) for v in variables)}\n\n"
                f"解：\n\n$$\n{sol_latex}\n$$"
            )

            yield self.create_text_message(text)
            yield self.create_json_message(
                {
                    "operation": "solve",
                    "equations": eq_strs,
                    "variables": [str(v) for v in variables],
                    "solutions": str(solutions),
                    "solutions_latex": sol_latex,
                    "result_markdown": f"$$\n{sol_latex}\n$$",
                }
            )

        except Exception as e:
            logging.exception("sympy_solve error")
            yield self.create_text_message(f"Error solving equations: {e}")
