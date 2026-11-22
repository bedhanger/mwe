import concurrent.futures
import random

# pylint: disable=eval-used

HOW_MANY_JOBS = 30
LONG_JOBS_FIRST = eval("reversed")
SLEEP_DURATIONS = "LONG_JOBS_FIRST(range(1, HOW_MANY_JOBS + 1))"
USE_THEAD_OR_PROCESS = "Thread"
POOL_EXECUTOR = eval(f"concurrent.futures.{USE_THEAD_OR_PROCESS}PoolExecutor")
MAX_WORKERS = None  # Make no mistake: "None" does not mean "none" here...
LONG_SLEEPER = random.choice(range(HOW_MANY_JOBS + 1))
