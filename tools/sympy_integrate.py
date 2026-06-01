import logging
from typing import Any, Generator

import sympy
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.sympy_utils import parse, to_latex


class SympyIntegrateTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        expression_str = tool_parameters.get("expression", "").strip()
        variable_str = tool_parameters.get("variable", "x").strip() or "x"
        lower_str = tool_parameters.get("lower_bound", "").strip()
        upper_str = tool_parameters.get("upper_bound", "").strip()

        if not expression_str:
            yield self.create_text_message("Error: expression parameter is required.")
            return

        is_definite = bool(lower_str and upper_str)

        try:
            expr = parse(expression_str)
            var = sympy.Symbol(variable_str)
            expr_latex = to_latex(expr)

            if is_definite:
                lower = parse(lower_str)
                upper = parse(upper_str)
                result = sympy.integrate(expr, (var, lower, upper))
                result_simplified = sympy.simplify(result)
                result_latex = to_latex(result_simplified)
                lower_latex = to_latex(lower)
                upper_latex = to_latex(upper)

                integral_notation = (
                    f"\\int_{{{lower_latex}}}^{{{upper_latex}}} {expr_latex} \\, d{variable_str}"
                )
                full_latex = f"{integral_notation} = {result_latex}"
                text = (
                    f"**定积分结果**\n\n"
                    f"$$\n{full_latex}\n$$"
                )
                json_out = {
                    "operation": "definite_integral",
                    "expression": expression_str,
                    "variable": variable_str,
                    "lower_bound": lower_str,
                    "upper_bound": upper_str,
                    "result": str(result_simplified),
                    "result_latex": result_latex,
                    "result_markdown": f"$$\n{full_latex}\n$$",
                }
            else:
                result = sympy.integrate(expr, var)
                result_latex = to_latex(result)

                integral_notation = f"\\int {expr_latex} \\, d{variable_str}"
                full_latex = f"{integral_notation} = {result_latex} + C"
                text = (
                    f"**不定积分结果**\n\n"
                    f"$$\n{full_latex}\n$$"
                )
                json_out = {
                    "operation": "indefinite_integral",
                    "expression": expression_str,
                    "variable": variable_str,
                    "result": str(result),
                    "result_latex": result_latex + " + C",
                    "result_markdown": f"$$\n{full_latex}\n$$",
                }

            yield self.create_text_message(text)
            yield self.create_json_message(json_out)

        except Exception as e:
            logging.exception("sympy_integrate error")
            yield self.create_text_message(f"Error computing integral: {e}")
