import json
import requests
import logging
from time import sleep
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

logger = logging.getLogger(__name__)


class DeeplExtension(Extension):

    def __init__(self):
        super(DeeplExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        if event.get_argument() is None:
            return

        items = []
        apikey = extension.preferences['deepl_apikey']
        targetlang = extension.preferences['target_lang']

        url = 'https://api-free.deepl.com/v2/translate'
        myobj = {'auth_key': apikey,
                'text':event.get_argument(),
                'target_lang':targetlang
                }

        x = requests.post(url, data = myobj)
        result = json.loads(x.content)

        resulttext = result['translations'][0]['text']
        detectedlang = result['translations'][0]['detected_source_language']

        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name=resulttext,
                                         description='Detected lang: %s' % detectedlang,
                                         highlightable=False,
                                         on_enter=CopyToClipboardAction(resulttext)
                                         ))

        myobj = {'auth_key': apikey,
                'text':event.get_argument(),
                'target_lang':'EN',
                'source_lang': targetlang
                }

        x = requests.post(url, data = myobj)
        result = json.loads(x.content)

        resulttext = result['translations'][0]['text']
        detectedlang = result['translations'][0]['detected_source_language']

        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name=resulttext,
                                         description='Detected lang: %s' % detectedlang,
                                         highlightable=False,
                                         on_enter=CopyToClipboardAction(resulttext)
                                         ))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name=data['new_name'],
                                                           on_enter=HideWindowAction())])


if __name__ == '__main__':
    DeeplExtension().run()
