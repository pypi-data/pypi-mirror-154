from pyappconf import AppConfig, ConfigFormats

from tests.config import CONFIGS_DIR

SETTINGS_ONE = AppConfig(
    app_name="MyApp",
    config_name="one",
    custom_config_folder=CONFIGS_DIR,
    default_format=ConfigFormats.YAML,
)
