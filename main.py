#!/usr/bin/env python3
import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from calculator_logic import Calculator
from simpleeval import NameNotDefined, OperatorNotDefined, FunctionNotDefined

logger = logging.getLogger(__name__)

class CalculatorExtension(Extension):

    def __init__(self):
        super(CalculatorExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.calculator = Calculator()

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = (event.get_argument() or "").strip()
        items = []

        if not query:
            return RenderResultListAction([
                ExtensionResultItem(icon='images/icon.png',
                                    name='Type a math expression',
                                    description='Example: 2 + 2 or sqrt(16)',
                                    on_enter=CopyToClipboardAction(""))
            ])

        try:
            result = extension.calculator.evaluate(query)
            result_str = extension.calculator.format_result(result)

            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=result_str,
                                             description='Press Enter to copy result',
                                             on_enter=CopyToClipboardAction(result_str)))
        except (NameNotDefined, OperatorNotDefined, FunctionNotDefined, SyntaxError, TypeError, ZeroDivisionError, ValueError) as e:
             # User error
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='Invalid Expression',
                                             description=str(e),
                                             on_enter=CopyToClipboardAction(str(e))))
        except Exception as e:
            # Internal or unexpected error
            logger.error(f"Error evaluating query: {e}", exc_info=True)
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='Error',
                                             description="An unexpected error occurred",
                                             on_enter=CopyToClipboardAction("Error")))

        return RenderResultListAction(items)

if __name__ == '__main__':
    CalculatorExtension().run()