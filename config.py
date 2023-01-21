import os
from pathlib import Path

from dotmap import DotMap

from utils.utils_data import load_ini

cwd = Path(__file__).parent.resolve()
config = load_ini(os.path.join(cwd, "config.ini"))

cfg = DotMap()
cfg.cwd = cwd
cfg.database_path = os.path.join(cwd, config["PARAMS"]["DATABASE_FILENAME"])
cfg.model_name = config["PARAMS"]["MODEL_NAME"]
cfg.model_savepath = os.path.join(cwd, config["PARAMS"]["MODEL_SAVEFILE"])
