#!/usr/bin/env python3
import math
import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

logger = logging.getLogger(__name__)

class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument() or ""
        
        # Define the allowable safe environment
        # We allow everything from the math module, plus basic builtins if needed (usually none for strict math)
        safe_dict = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        # Add commonly used aliases if desired, e.g. abs which is a builtin
        safe_dict['abs'] = abs
        safe_dict['round'] = round
        safe_dict['min'] = min
        safe_dict['max'] = max
        
        items = []

        if not query.strip():
            return RenderResultListAction([
                ExtensionResultItem(icon='images/icon.png',
                                    name='Type a math expression',
                                    description='Example: 2 + 2 or sqrt(16)',
                                    on_enter=CopyToClipboardAction(""))
            ])

        try:
            # Evaluate the expression in the safe environment
            # Allow users to ommit 'math.' prefix
            query = query.replace('^', '**')
            result = eval(query, {"__builtins__": None}, safe_dict)
            
            # Format the result to remove trailing .0 for integers
            if isinstance(result, float) and result.is_integer():
                result_str = str(int(result))
            else:
                result_str = str(result)

            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=result_str,
                                             description='Result for "%s"' % query,
                                             on_enter=CopyToClipboardAction(result_str)))
        except Exception as e:
            # Handle errors (semantics, syntax, zero division, etc.)
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='Error',
                                             description=str(e),
                                             on_enter=CopyToClipboardAction(str(e))))

        return RenderResultListAction(items)

if __name__ == '__main__':
    DemoExtension().run()