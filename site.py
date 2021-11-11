import sql
import ui
import pywebio

async def main():
    pywebio.session.run_async(ui.main())

if __name__ == "__main__":
    pywebio.start_server(main, port = 7000, cdn = False)