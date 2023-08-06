#Disable
Disable is a context manager that disables output and specified errors. `with Disable(Exception) as (write, flush):` has the following effect: print statements do nothing and all subclasses of Exception do not propagate to the caller if raised. "Write" and "flush" are used for writing and flushing.

#Parallel
Parallel is basically zip and map combined. It can take an iterable of iterables or multiple iterables and zips them. If the func argument is used then it works like map. There is also a strict option.