import logging
from typing import Any, Generator

import sympy
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.sympy_utils import parse, to_latex


class SympySeriesExpansionTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        expression_str = tool_parameters.get("expression", "").strip()
        variable_str = tool_parameters.get("variable", "x").strip() or "x"
        point_str = tool_parameters.get("point", "0").strip() or "0"
        order_str = tool_parameters.get("order", "6") or "6"

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
            point = parse(point_str)

            series = expr.series(var, point, order)
            series_removed = series.removeO()

            expr_latex = to_latex(expr)
            series_latex = to_latex(series)
            series_removed_latex = to_latex(series_removed)
            point_latex = to_latex(point)

            text = (
                f"**级数展开结果**\n\n"
                f"原函数，在 {variable_str} = {point_str} 处展开至 {order} 阶：\n\n"
                f"$$\nf({variable_str}) = {expr_latex}\n$$\n\n"
                f"展开式：\n\n"
                f"$$\n{series_latex}\n$$\n\n"
                f"多项式近似（去掉余项）：\n\n"
                f"$$\n{series_removed_latex}\n$$"
            )

            yield self.create_text_message(text)
            yield self.create_json_message(
                {
                    "operation": "series_expansion",
                    "expression": expression_str,
                    "variable": variable_str,
                    "point": point_str,
                    "order": order,
                    "result": str(series),
                    "result_latex": series_latex,
                    "result_markdown": f"$$\n{series_latex}\n$$",
                    "result_without_O": str(series_removed),
                    "result_without_O_latex": series_removed_latex,
                    "result_without_O_markdown": f"$$\n{series_removed_latex}\n$$",
                }
            )

        except Exception as e:
            logging.exception("sympy_series error")
            yield self.create_text_message(f"Error computing series expansion: {e}")
