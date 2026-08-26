import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_FILE = BASE_DIR / "app.log"

LOG_FILE.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOG_FILE,
    filemode="a"  # Append mode
)

logger = logging.getLogger(__name__)

