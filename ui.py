from pywebio import *
import random

from pywebio.session import run_async
import sql
import asyncio

users = []
global_messages = []
muted = []

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

    def onJoin(self, box):
        users.append(self)
        global_messages.append(("NOTE", f"`{self.name}`, has joined to channel."))
        box.append(output.put_markdown(f"`{self.name}`, has joined to channel."))

    def onLeave(self, box):
        global_messages.append(("NOTE", f"`{self.name}`, has leaved from channel."))
        users.remove(self)
        box.append(output.put_markdown(f"`{self.name}`, has leaved from channel."))

    async def refresh_messages(self, box):
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




async def show_reg():
    name = await input.input("Login: ")
    password = await input.input("Pasword: ")
    sql.cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = sql.cursor.fetchone()

    if user:
        if user[2] != password:
            output.put_error("Uncorrect password")
            await show_reg()
        else:
            await registered(User(name, user[1], user[1] == 1))
    else:
        id = random.randint(100, 1000)
        sql.put(id, name, password)
        await registered(User(name, id, False))

def get(iterable, cons):
    for i in iterable:
        if cons(i): return i

async def registered(user: User):
    msg_box = output.output("Text")
    output.put_scrollable(msg_box, height = 300, keep_bottom = True)
    user.onJoin(msg_box)
    
    task = run_async(user.refresh_messages(msg_box))

    while True:
        data = await input.input_group("New message!", [
            input.input(placeholder = "Text", name = "msg"),
            input.actions(name = "cmd", buttons = ["Send", {"label": "Leave from channel.", "type": "cancel"}])
        ], validate = lambda m: ("msg", "Input text of message!") if m["cmd"] == "Send" and not m["msg"] else None)

        if not data: break
        #костыльно но сойдет
        if user.admin and "/mute" in data["msg"]: 
            muted.append(data['msg'].split()[1])
            global_messages.append(("NOTE:", f"{data['msg'].split()[1]} has muted!"))

        msg_box.append(output.put_markdown(f"{user.name}: {data['msg']}"))
        global_messages.append((user.name, data["msg"]))

    task.close()

    output.toast("You're leaved from channel!")

    user.onLeave(msg_box)
