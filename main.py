
import psutil
from difflib import SequenceMatcher

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

def score(a,b):
    return SequenceMatcher(None,a.lower(),b.lower()).ratio()


class Ext(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, Handler())


class Handler(EventListener):
    def on_event(self,event,extension):
        q=(event.get_argument() or "").strip().lower()

        if q=="watch":
            return self.watch()

        return self.search(q)

    def search(self,q):
        items=[]

        for p in psutil.process_iter(["pid","name","cmdline","username"]):
            try:
                name=p.info["name"] or ""
                cmd=" ".join(p.info.get("cmdline") or [])
                pid=str(p.info["pid"])

                text=f"{name} {cmd} {pid}"
                s=score(q,text) if q else 1

                if q and s<0.2:
                    continue

                items.append((s,name,pid,cmd,p.info["username"]))
            except:
                continue

        items.sort(reverse=True,key=lambda x:x[0])
        items=items[:15]

        res=[]
        for _,name,pid,cmd,user in items:
            res.append(
                ExtensionResultItem(
                    icon="images/icon.png",
                    name=f"{name} ({pid})",
                    description=f"{user} | {cmd[:80]}",
                    on_enter=RunScriptAction(f"python3 kill_manager.py {pid}")
                )
            )
        return RenderResultListAction(res)

    def watch(self):
        procs=[]
        for p in psutil.process_iter(["pid","name","cpu_percent"]):
            try:
                procs.append((p.info["cpu_percent"],p.info["pid"],p.info["name"]))
            except:
                continue

        procs.sort(reverse=True,key=lambda x:x[0])

        res=[]
        for cpu,pid,name in procs[:15]:
            res.append(
                ExtensionResultItem(
                    icon="images/icon.png",
                    name=f"{name} ({pid})",
                    description=f"CPU {cpu}%",
                    on_enter=RunScriptAction(f"python3 kill_manager.py {pid}")
                )
            )

        # refresh button
        res.insert(0,
            ExtensionResultItem(
                icon="images/icon.png",
                name="Refresh",
                description="Reload process list",
                on_enter=RunScriptAction("python3 main.py watch")
            )
        )

        return RenderResultListAction(res)


if __name__=="__main__":
    Ext().run()
