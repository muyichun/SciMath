import logging
from typing import Any, Generator

import sympy
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.sympy_utils import parse, to_latex


class SympyDiffTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        expression_str = tool_parameters.get("expression", "").strip()
        variable_str = tool_parameters.get("variable", "x").strip() or "x"
        order_str = tool_parameters.get("order", "1") or "1"

        if not expression_str:
            yield self.create_text_message("Error: expression parameter is required.")
            return

        try:
            order = int(order_str)
        except (ValueError, TypeError):
            yield self.create_text_message(f"Error: order must be an integer, got '{order_str}'.")
            return

        try:
            expr = parse(expression_str)
            var = sympy.Symbol(variable_str)
            result = sympy.diff(expr, var, order)

            expr_latex = to_latex(expr)
            result_latex = to_latex(result)

            if order == 1:
                deriv_notation = f"\\frac{{d}}{{d{variable_str}}}\\left({expr_latex}\\right)"
            else:
                deriv_notation = f"\\frac{{d^{order}}}{{d{variable_str}^{order}}}\\left({expr_latex}\\right)"

            full_latex = f"{deriv_notation} = {result_latex}"
            text = (
                f"**求导结果**\n\n"
                f"原函数：\n\n"
                f"$$\nf({variable_str}) = {expr_latex}\n$$\n\n"
                f"对 {variable_str} 求 {order} 阶导：\n\n"
                f"$$\n{full_latex}\n$$"
            )

            yield self.create_text_message(text)
            yield self.create_json_message(
                {
                    "operation": "differentiate",
                    "expression": expression_str,
                    "variable": variable_str,
                    "order": order,
                    "result": str(result),
                    "result_latex": result_latex,
                    "result_markdown": f"$$\n{full_latex}\n$$",
                }
            )

        except Exception as e:
            logging.exception("sympy_diff error")
            yield self.create_text_message(f"Error differentiating expression: {e}")
