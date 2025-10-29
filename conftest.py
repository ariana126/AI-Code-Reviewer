import os
import sys

import dotenv

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

dotenv.load_dotenv(".env.test", override=True)