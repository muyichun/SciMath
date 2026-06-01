import logging
from typing import Any, Generator

import sympy
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.sympy_utils import parse, to_latex

_DIRECTION_MAP = {"+": "+", "right": "+", "-": "-", "left": "-", "+-": "+-", "both": "+-"}


class SympyLimitTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        expression_str = tool_parameters.get("expression", "").strip()
        variable_str = tool_parameters.get("variable", "x").strip() or "x"
        point_str = tool_parameters.get("point", "").strip()
        direction_str = tool_parameters.get("direction", "+-").strip().lower() or "+-"

        if not expression_str:
            yield self.create_text_message("Error: expression parameter is required.")
            return
        if not point_str:
            yield self.create_text_message("Error: point parameter is required.")
            return

        direction = _DIRECTION_MAP.get(direction_str, "+-")

        try:
            expr = parse(expression_str)
            var = sympy.Symbol(variable_str)
            point = parse(point_str)
            result = sympy.limit(expr, var, point, direction)

            expr_latex = to_latex(expr)
            point_latex = to_latex(point)
            result_latex = to_latex(result)

            dir_label = {"+-": "", "+": "^+", "-": "^-"}[direction]
            limit_notation = (
                f"\\lim_{{{variable_str} \\to {point_latex}{dir_label}}} {expr_latex}"
            )
            full_latex = f"{limit_notation} = {result_latex}"

            text = (
                f"**极限结果**\n\n"
                f"$$\n{full_latex}\n$$"
            )

            yield self.create_text_message(text)
            yield self.create_json_message(
                {
                    "operation": "limit",
                    "expression": expression_str,
                    "variable": variable_str,
                    "point": point_str,
                    "direction": direction,
                    "result": str(result),
                    "result_latex": result_latex,
                    "result_markdown": f"$$\n{full_latex}\n$$",
                }
            )

        except Exception as e:
            logging.exception("sympy_limit error")
            yield self.create_text_message(f"Error computing limit: {e}")
