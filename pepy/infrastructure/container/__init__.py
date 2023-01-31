from . import _config as config
from ._start import (
    project_repository,
    command_bus,
    badge_service,
    personalized_badge_service,
    logger,
    stats_viewer,
    mongo_client,
    admin_password_checker,
)

logger.debug("container initiated")
