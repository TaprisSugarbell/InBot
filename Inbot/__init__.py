import os
import logging
from logging import handlers

log_ = "./logs/"
if os.path.exists(log_):
    pass
else:
    os.makedirs("./logs/", exist_ok=True)

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING,
                    handlers=[
                        handlers.RotatingFileHandler(
                            filename="./logs/sayu.log",
                            maxBytes=3145728,
                            backupCount=1
                        ),
                        logging.StreamHandler()
                    ]
                    )

sayulogs = logging.getLogger("SayuImages")



