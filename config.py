import logging
from datetime import datetime

# Configure logging with DEBUG log level.
logging.basicConfig(
    filename=f"logger_{datetime.today().strftime('%Y%m%d')}.log",
    level=logging.DEBUG,
    format="%(filename)s:%(lineno)s %(levelname)s:%(message)s",
)