#!/usr/bin/env python

"""Use concurrent futures to sleep asynchronously.

Measure how long each sleep took.  By making subtle changes, you can learn a lot about
asynchronicity.  Submitting the sleeps in monotonically increasing duration (or not, the default)
and/or using processes instead of threads (the default) are alternatives.  Not to mention playing
with the max_workers argument to the executors' constructor.
"""

import concurrent.futures
import random
import sys
import textwrap
import time

from contextlib import redirect_stdout
from typing import NamedTuple


# pylint: disable=eval-used

# Make the above-mentioned changes a little more accessible
HOW_MANY_JOBS = 30
LONG_JOBS_FIRST = eval("reversed")
SLEEP_DURATIONS = "LONG_JOBS_FIRST(range(1, HOW_MANY_JOBS + 1))"
USE_THEAD_OR_PROCESS = "Thread"
POOL_EXECUTOR = eval(f"concurrent.futures.{USE_THEAD_OR_PROCESS}PoolExecutor")
MAX_WORKERS = None  # Make no mistake: "None" does not mean "none" here...
LONG_SLEEPER = random.choice(range(0, HOW_MANY_JOBS + 1))


class OversleptError(TimeoutError):
    """What to raise when we have slept too long."""


class JobResult(NamedTuple):
    """Ease the access to the results of the asynchronous operation."""

    what: int
    when: float

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}, what={self.what}, when={self.when}>"


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
    return JobResult(what=how_long, when=time.monotonic())

if __name__ == '__main__':

    start = time.monotonic()

    with POOL_EXECUTOR(max_workers=MAX_WORKERS) as worker_pool:

        workload = [worker_pool.submit(running_job, how_long=d, submitted=start)
                    for d in eval(SLEEP_DURATIONS)]  # &
        print("The workload", end='\n\n')
        for job in zip(eval(SLEEP_DURATIONS), workload):
            print(f"{' ' * 4}Job {job}")
        print(f"\nwas &-submitted after {time.monotonic() - start} second(s)")

        print("\nWaiting for unfinished jobs...\n")

        for job_done in concurrent.futures.as_completed(workload):

            try:
                job_result = JobResult._make(job_done.result())
                #print(f"{' ' * 4}{job_result}")
                so_many, how_many = job_result.what, job_result.when - start
                print(f"{' ' * 4}Async-sleeping for {so_many} sec(s) \"took\" {how_many} sec(s)")
            except Exception as exc:  # pylint: disable=broad-exception-caught
                with redirect_stdout(sys.stderr):
                    print(f"{' ' * 4}{job_done} was unhappy: {exc}")

    print(f"\nAll in all, it took {time.monotonic() - start} second(s)")
