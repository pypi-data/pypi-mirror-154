import functools

from .spatial import spatial_stack, spatial_unstack


def stack_then_unstack(_func=None, *, merge_with_input=False):
    """Decorator to automatically run spatial stack before
    and spatial unstack after a function.

    Assumes that

    Parameters
    ----------
    _func : function
        Function to decorate
    merge_with_input : bool
        Whether to return result together with the input dataset, or just the
        stand-alone dataarray.
    """

    def decorator_stack_then_unstack(func):
        @functools.wraps(func)
        def wrapper_stack_then_unstack(*args, **kwargs):

            # Convert to mutable
            args = list(args)

            # The spatial object is assumed to be the first argument.
            ds = args[0].copy()

            # Stack the object
            stacked = spatial_stack(ds)

            # Swap the first object with the stacked object
            args[0] = stacked

            # Run the function
            result = func(*args, **kwargs)

            # Merge with stacked dataset to get coords/dims/attrs and then unstack
            stacked = stacked.update(result)[[v for v in result.data_vars]]
            result_unstacked = spatial_unstack(stacked)

            # return standalone dataset or everything (merged with input)
            if merge_with_input:
                return ds.update(result_unstacked)
            else:
                return result_unstacked

        return wrapper_stack_then_unstack

    if _func is None:
        return decorator_stack_then_unstack
    else:
        return decorator_stack_then_unstack(_func)
