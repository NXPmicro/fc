import asyncio
from functools import wraps


def safe_cache(func):
    @wraps(func)
    def decorator(*args):
        if args[2] not in args[0].__dict__[args[1]]:
            args[0].__dict__[args[1]][args[2]] = []
        return func(*args)

    return decorator


def check_priority_scheduler(*decorator_args):
    def wrapper(func):
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_decorator(*args):
                driver = (
                    args[0].priority_scheduler
                    if len(decorator_args) == 0
                    else decorator_args[0]
                )
                if not driver:
                    return False
                return await func(*args)

            return async_decorator

        @wraps(func)
        def decorator(*args):
            driver = (
                args[0].priority_scheduler
                if len(decorator_args) == 0
                else decorator_args[0]
            )
            if not driver:
                return False
            return func(*args)

        return decorator

    return wrapper