from dataclasses import dataclass


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
