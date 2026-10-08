"""Use concurrent futures to sleep asynchronously.

Measure how long each sleep took.  By making subtle changes, you can learn a lot about
asynchronicity.  Submitting the sleeps in monotonically increasing duration (or not, the default)
and/or using processes instead of threads (the default) are alternatives.  Not to mention playing
with the max_workers argument to the executors' constructor.
"""

import concurrent.futures
import multiprocessing as mp
import random
import sys
import textwrap
import time
from contextlib import redirect_stdout
from dataclasses import dataclass

# pylint: disable=eval-used

# Make the above-mentioned changes a little more accessible
HOW_MANY_JOBS = 30
LONG_JOBS_FIRST = eval("reversed")
SLEEP_DURATIONS = "LONG_JOBS_FIRST(range(1, HOW_MANY_JOBS + 1))"
USE_THEAD_OR_PROCESS = "Thread"
POOL_EXECUTOR = eval(f"concurrent.futures.{USE_THEAD_OR_PROCESS}PoolExecutor")
MAX_WORKERS = None  # Make no mistake: "None" does not mean "none" here...
LONG_SLEEPER = random.choice(range(HOW_MANY_JOBS + 1))


class OversleptError(TimeoutError):
    """What to raise when we have slept too long."""


@dataclass
class JobResult:
    """Ease the access to the results of the asynchronous operation."""

    what: int
    when: float
    submitted: float

    def __str__(self) -> str:
        return f'Async-sleeping for {self.what} sec(s) "took" {self.when - self.submitted} sec(s)'


def running_job(how_long: int, submitted: float) -> JobResult:
    """Sleeping is the new running..."""

    time.sleep(how_long)

    if how_long == LONG_SLEEPER:
        # Hit the snooze button to gain an additional 10%...
        time.sleep(how_long * 0.1)
        raise OversleptError(textwrap.dedent(f'''
            We "slept" {time.monotonic() - submitted} sec(s), though we were only allowed {how_long}
        ''').strip())

    # Return the what and the when
    return JobResult(what=how_long, when=time.monotonic(), submitted=submitted)

def main():

    start = time.monotonic()

    with mp.Manager() as mpm:
        safeprint = mpm.Lock()  # This is pickleable, the plain lock is not; and it works for
                                # threads *and* processes.

        with POOL_EXECUTOR(max_workers=MAX_WORKERS) as worker_pool:

            workload = [worker_pool.submit(running_job, how_long=d, submitted=start)
                        for d in eval(SLEEP_DURATIONS)]  # &
            with safeprint:
                print("The workload", end='\n\n')
            for job in zip(eval(SLEEP_DURATIONS), workload):
                with safeprint:
                    print(f"Job {job}")
            with safeprint:
                print(f"\nwas &-submitted after {time.monotonic() - start} second(s)")

                print("\nWaiting for unfinished jobs...\n")

            for job_done in concurrent.futures.as_completed(workload):
                try:
                    with safeprint:
                        print(job_done.result())
                except OversleptError as exc:
                    with redirect_stdout(sys.stderr), safeprint:
                        print(f"{job_done} was unhappy: {exc}")
        with safeprint:
            print(f"\nAll in all, it took {time.monotonic() - start} second(s)") 
