import logging


logging.basicConfig(
    level=logging.INFO,
    format="[%(filename)s:%(lineno)s:%(funcName)20s()] %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)