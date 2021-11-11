from pywebio import *
import random
from pywebio.output import OutputPosition

from pywebio.session import run_async
import sql
from Vars import *
from classes import *

async def main():
    name = await input.input("Login: ")
    password = await input.input("Pasword: ")
    sql.cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = sql.cursor.fetchone()

    if user:
        if user[2] != password:
            output.put_error("Uncorrect password")
            await main()
        else:
            await registered(User(name, user[1], user[1] == 1))
    else:
        id = random.randint(100, 1000)
        sql.put(id, name, password)
        await registered(User(name, id, False))

def get(iterable, cons):
    for i in iterable:
        if cons(i): return i

def validate(m: dict):
    if m['cmd'] == "Send" and not m["msg"]:
        return ("msg", "Input message!")
    elif m['cmd'] == "Mute" and not m["msg"]:
        return ("msg", "Input name!")
    return None

async def registered(user: User):
    msg_box = output.output("Text")
    users_box = output.output("Users")

    output.put_scrollable(msg_box, height = 300, keep_bottom = True)
    output.put_column(users_box, position = OutputPosition.TOP)

    user.onJoin(msg_box, users_box)
    
    task = run_async(user.refresh(msg_box))

    while True:
        data = await input.input_group("New message!", [
            input.input(placeholder = "Text", name = "msg"),
            input.actions(name = "cmd", buttons = ["Send", {"label": "Leave from channel.", "type": "cancel"}, "Mute"]),
        ], validate = validate)

        if not data: break

        if data['cmd'] == "Mute":
            if user.admin:
                muted.append(data['msg'])
                global_messages.append(("📣", f"{data['msg']} has muted by {user.name}"))
            else:
                output.put_error("You're not admin!")
            continue

        msg_box.append(output.put_markdown(f"{user.name}: {data['msg']}"))
        global_messages.append((user.name, data["msg"]))

    task.close()

    output.toast("You're leaved from channel!")

    user.onLeave(msg_box, users_box)
