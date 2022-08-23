import logging

FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(
    filename="logfile.log",
    format=FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger()
