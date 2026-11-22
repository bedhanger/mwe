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
from contextlib import nullcontext, redirect_stdout
from typing import Never, Self

from .constants import (
    HOW_MANY_JOBS,
    LONG_JOBS_FIRST,
    LONG_SLEEPER,
    MAX_WORKERS,
    POOL_EXECUTOR,
    RUIN_CONCURRENCY,
    SLEEP_DURATIONS,
    USE_THEAD_OR_PROCESS,
)
from .utils import JobResult, OversleptError

# pylint: disable=eval-used

class Asleeps:
    """A context manager to simulate the submissions and waits for the completions, as they become
    "available", of asynchronous sleeps.
    """

    def __init__(
        self,
        how_many_jobs: int = HOW_MANY_JOBS,
        long_jobs_first = LONG_JOBS_FIRST,
        sleep_durations: str = SLEEP_DURATIONS,
        use_thead_or_process: str = USE_THEAD_OR_PROCESS,
        pool_executor = POOL_EXECUTOR,
        max_workers = MAX_WORKERS,
        long_sleeper: int = LONG_SLEEPER,
        ruin_concurrency: bool = RUIN_CONCURRENCY
    ) -> None:

        self.how_many_jobs = how_many_jobs
        self.long_jobs_first = long_jobs_first
        self.sleep_durations = sleep_durations
        self.use_thead_or_process = use_thead_or_process
        self.pool_executor = pool_executor
        self.max_workers = max_workers
        self.long_sleeper = long_sleeper
        self.ruin_concurrency = ruin_concurrency

    def __enter__(self) -> Self:

        self.mpm = mp.Manager()
        self.safeprint = self.mpm.Lock()  # This is pickleable, the plain lock is not; and it works
                                          # for threads *and* processes.
        self.start = time.monotonic()

        worker_pool = self.pool_executor(max_workers=self.max_workers)

        # Use the pool_executor as a context-manager at your own risk: exiting it will wait for all
        # tasks to finish, which renders this class' __exit__ moot!
        with worker_pool if self.ruin_concurrency else nullcontext():
            self.workload = [worker_pool.submit(self.running_job, how_long=d, submitted=self.start)
                             for d in eval(self.sleep_durations)]  # &
            with self.safeprint:
                print("The workload", end='\n\n')
            for job in zip(eval(self.sleep_durations), self.workload):
                with self.safeprint:
                    print(f"Job {job}")
            with self.safeprint:
                print(f"\nwas &-submitted after {time.monotonic() - self.start} second(s)")

        return self

    def __run__(self) -> Never:
        raise NotImplementedError("No, you cannot call this directly, use a with statement!")

    def __exit__(self, exc_value, exc_type, traceback) -> bool:

        # Wait.
        for job_done in concurrent.futures.as_completed(self.workload):
            try:
                with self.safeprint:
                    print(job_done.result())
            except OversleptError as exc:
                with redirect_stdout(sys.stderr), self.safeprint:
                    print(f"{job_done} was unhappy: {exc}")
        with self.safeprint:
            print(f"\nAll in all, it took {time.monotonic() - self.start} second(s)") 

        return exc_value is not None

    def running_job(self, how_long: int, submitted: float) -> JobResult:
        """Sleeping is the new running..."""

        time.sleep(how_long)

        if how_long == self.long_sleeper:
            # Hit the snooze button to gain an additional 10%...
            time.sleep(how_long * 0.1)
            raise OversleptError(textwrap.dedent(f'''
                We "slept" {time.monotonic() - submitted} sec(s), though we were only allowed {how_long}
            ''').strip())

        # Return the what and the when
        return JobResult(what=how_long, when=time.monotonic(), submitted=submitted)


def main():
    """The entry-point."""

    with Asleeps() as the_way_to_do_it:
        assert the_way_to_do_it is not None
        print("\nWaiting for unfinished jobs...\n")

    with Asleeps(
        ruin_concurrency=True,  # This will "break" concurrency!
        long_sleeper=random.choice(range(HOW_MANY_JOBS + 1))  # This will just create a different
                                                              # long sleeper...
    ) as the_way_NOT_to_do_it:
        assert the_way_NOT_to_do_it is not None  # Alas, it should be!
        assert the_way_NOT_to_do_it is not the_way_to_do_it
        print("\nYou will see *this* line when all the fun is over...\n")
