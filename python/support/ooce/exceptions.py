"""Define exceptions with a preset message each

They can be overridden, of course.
We format them a little.
"""
import textwrap

class OutOfContextError(RuntimeError):

    def __init__(self, msg=None, cls=None, func=None, *pargs, **kwargs):

        # The default message, which is also a bit educational
        self.msg = textwrap.dedent(f"""
            no context has been established before invoking {func!r}

            Did you forget to use a with-statement?

            {cls!r} requires that the context-manager-protocol be used when instances of it are
            created.  This was a conscious design decision, aimed at facilitating resource
            management (freeing the resource, in particular).  So rather than saying something like

                >>> I = {cls}()
                >>> print(I)

            do this instead

                >>> with {cls}() as I:
                >>>     print(I)

            Outwith a context, I is practically unusable.
        """).strip()

        # Call the base class' constructor to init the exception class
        super().__init__(msg or self.msg, *pargs, **kwargs)
