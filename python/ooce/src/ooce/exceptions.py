"""Define exceptions with a preset message each

They can be overridden, of course.
We format them a little.
"""
import textwrap

class OutOfContextError(RuntimeError):

    def __init__(self, msg=None, klaas='<This class>', func='<a function>', *pargs, **kwargs):

        # The default message, which is also a bit educational
        self.default_msg = textwrap.dedent(f"""
            no context has been established before invoking the operation {func!r}

            Did you forget to use a with-statement?

            {klaas!r} requires that the context-manager-protocol be used when instances of it are
            created.  This was a conscious design decision, aimed at facilitating resource
            management (freeing the resource, in particular).  So rather than saying something like

                >>> I = {klaas}()
                >>> print(I)

            do this instead

                >>> with {klaas}() as I:
                >>>     print(I)

            Outwith a context, I is practically unusable.
        """).strip()

        # Call the base class' constructor to init the exception class
        super().__init__(msg or self.default_msg, *pargs, **kwargs)
