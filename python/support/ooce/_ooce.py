"""no context has been established before invoking {func.__name__!r}

Did you forget to use a with-statement?

{self.__class__.__name__!r} requires that the context-manager-protocol be used when instances of it
are created.  This was a conscious design decision, aimed at facilitating resource management
(freeing the resource, in particular).  So rather than saying something like

    >>> R = {self.__class__.__name__}()
    >>> print(R)

do this instead

    >>> with {self.__class__.__name__}() as R:
    >>>     print(R)

Outwith a context, R is practically unusable."""

class OutOfContextError(RuntimeError):
    """Preset the exception messge if none was specified"""

    def __init__(self, msg=None, *pargs, **kwargs):
        super().__init__(msg or __doc__, *pargs, **kwargs)
