from Vars import *
from pywebio import *
import asyncio

MAX_MESSAGES = 100

class User:
    def __init__(self, name, id, admin):
        self.name = name
        self.id = id
        self.admin = admin

    def mute(self):
        muted.append(self.name)

    def unmute(self):
        muted.remove(self.name)

    def onJoin(self, box, ubox):
        users.append(self)
        global_messages.append(("📣", f"`{self.name}`, has joined to channel."))
        box.append(output.put_markdown(f"`{self.name}`, has joined to channel."))
        ubox.append(self.name)

    def onLeave(self, box, ubox):
        global_messages.append(("📣", f"`{self.name}`, has leaved from channel."))
        users.remove(self)
        box.append(output.put_markdown(f"`{self.name}`, has leaved from channel."))
        ubox.remove(self.name)

    async def refresh(self, box):
        global global_messages

        last_index = len(global_messages)

        while True:
            await asyncio.sleep(1)

            for m in global_messages[last_index:]:
                if m[0] != self.name and m[0] not in muted:
                    box.append(output.put_markdown(f"{m[0]}: {m[1]}"))

            if len(global_messages) >= MAX_MESSAGES:
                global_messages = global_messages[len(global_messages) // 2:]

            last_index = len(global_messages)