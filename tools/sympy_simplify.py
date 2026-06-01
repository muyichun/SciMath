import logging
from typing import Any, Generator

import sympy
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.sympy_utils import parse, to_latex

_OPERATIONS = {
    "simplify": sympy.simplify,
    "factor": sympy.factor,
    "expand": sympy.expand,
    "cancel": sympy.cancel,
    "apart": sympy.apart,
    "trigsimp": sympy.trigsimp,
    "radsimp": sympy.radsimp,
    "powsimp": sympy.powsimp,
    "expand_trig": sympy.expand_trig,
    "nsimplify": sympy.nsimplify,
}

_OP_LABELS = {
    "simplify": "General simplification",
    "factor": "Factor",
    "expand": "Expand",
    "cancel": "Cancel (rational)",
    "apart": "Partial fractions",
    "trigsimp": "Trigonometric simplification",
    "radsimp": "Rationalize denominator",
    "powsimp": "Simplify powers",
    "expand_trig": "Expand trigonometric",
    "nsimplify": "Numerical simplification",
}


class SympySimplifyTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        expression_str = tool_parameters.get("expression", "").strip()
        operation = tool_parameters.get("operation", "simplify").strip() or "simplify"

        if not expression_str:
            yield self.create_text_message("Error: expression parameter is required.")
            return

        if operation not in _OPERATIONS:
            yield self.create_text_message(
                f"Error: unknown operation '{operation}'. Choose from: {', '.join(_OPERATIONS)}."
            )
            return

        try:
            expr = parse(expression_str)
            result = _OPERATIONS[operation](expr)
            expr_latex = to_latex(expr)
            result_latex = to_latex(result)
            op_label = _OP_LABELS[operation]

            text = (
                f"**{op_label}结果**\n\n"
                f"输入：\n\n"
                f"$$\n{expr_latex}\n$$\n\n"
                f"结果：\n\n"
                f"$$\n{result_latex}\n$$"
            )

            yield self.create_text_message(text)
            yield self.create_json_message(
                {
                    "operation": operation,
                    "expression": expression_str,
                    "result": str(result),
                    "result_latex": result_latex,
                    "result_markdown": f"$$\n{result_latex}\n$$",
                }
            )

        except Exception as e:
            logging.exception("sympy_simplify error")
            yield self.create_text_message(f"Error applying {operation}: {e}")
