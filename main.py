import psutil
from difflib import SequenceMatcher

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

def score(a,b):
    return SequenceMatcher(None,a,b).ratio()

class Ext(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, Handler())

class Handler(EventListener):
    def on_event(self, event, extension):
        q = (event.get_argument() or "").lower().strip()

        items = []
        for p in psutil.process_iter(["pid","name","cmdline","username"]):
            try:
                name = p.info["name"] or ""
                cmd = " ".join(p.info.get("cmdline") or [])
                pid = str(p.info["pid"])

                text = f"{name} {cmd} {pid}"
                s = score(q, text)

                if q and s < 0.25:
                    continue

                items.append((s,name,pid,cmd))
            except:
                continue

        items.sort(reverse=True,key=lambda x:x[0])
        items = items[:15]

        res = []
        for _,name,pid,cmd in items:
            res.append(
                ExtensionResultItem(
                    icon="images/icon.png",
                    name=f"{name} ({pid})",
                    description=cmd[:80],
                    on_enter=RunScriptAction(f"python3 kill_manager.py {pid}")
                )
            )

        return RenderResultListAction(res)

if __name__ == "__main__":
    Ext().run()
