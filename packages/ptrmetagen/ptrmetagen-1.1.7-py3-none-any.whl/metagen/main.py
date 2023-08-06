from metagen.config.config import load_config, BASE_CONFIF_FILE
from metagen.register import register_factory


CONFIG = load_config(BASE_CONFIF_FILE)
register = register_factory.get(registerName=CONFIG.registerName)()