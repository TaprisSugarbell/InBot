import asyncio

from InBot import app, logs_channel_update, logging_stream_info
from InBot.__vars__ import BOT_NAME, __version__
from InBot.helper import configure_wd
from InBot.helper.logs_utils import sayu_error
from InBot.helper.loop_in_thread import read_and_execute, run_asyncio


async def main():
    # await configure_wd()
    await app.start()
    await logs_channel_update()
    await asyncio.to_thread(run_asyncio, obj=read_and_execute, app=app)

if __name__ == "__main__":
    logging_stream_info(f"Starting {BOT_NAME}, version - {__version__}")
    try:
        app.run(main())
    except Exception as e:
        print(e)
        raise
        # app.run(sayu_error(e, app))
