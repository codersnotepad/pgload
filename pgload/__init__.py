# Let users know if they're missing any of our hard dependencies
hard_dependencies = ["psycopg2"]
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append("{0}: {1}".format(dependency, str(e)))

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(missing_dependencies)
    )
del hard_dependencies, dependency, missing_dependencies

from .pgload import pgload

pgload = pgload()
__version__ = "0.2.6"
__help__ = vars(pgload)
validate_data = pgload.validate_data
scd2_load = pgload.scd2_load
