from inspect import signature
from functools import wraps
import sys

def forward_params(f_from, *args, result = None, **kwargs):
    """call a function passing parameters in *args and **kwargs  iff the function has
    parameters of the same name declared in it's signature.

    Args:
        param1 f_from (function): the function with parameters to be forwarded
        param2 *args: the positial arguments being passed to f_from
        param3 result (optional): the result of f_from to be forwarded as a parameter
        param4 **kwargs: the keyword arguments being passed to f_from

    """
    def run(f_to):
        # apply default arguments
        bound_args = signature(f_from).bind(*args, **kwargs)
        bound_args.apply_defaults()

        passing, passing_kwargs = [], {}
        for name, param in signature(f_to).parameters.items():
            if name == 'result':
                passing += [result]
            elif param.kind == param.VAR_POSITIONAL:
                passing += [arg for arg in bound_args.args if arg not in passing]
            elif param.kind == param.VAR_KEYWORD:
                passing_kwargs.update({k:v for k,v in bound_args.kwargs.items() if k not in passing_kwargs})
            else:
                try:
                    passing.append(bound_args.arguments[name])
                except KeyError: # not present in arguments
                    # must be present in kwargs, else we want to fail
                    passing_kwargs[name] = bound_args.kwargs[name]
        return f_to(*passing, **passing_kwargs)
    return run

def before(func):
    """create decorator functions to provide hooks which
    are attatched to the function object any function
    decorated by func.before will be called before the
    code for func is executed"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        run = forward_params(func, *args ,**kwargs)
        var_keyword_args =  (name for name, p in signature(func).parameters.items() if p.kind == p.VAR_KEYWORD)
        before_results = [run(f) for f in wrapper.pre_exec]
        if next(var_keyword_args, False): # if there is a variable keyword argument
            kwargs['before_results'] = before_results
        return func(*args, **kwargs)
    wrapper.pre_exec = []

    # create a decorator which adds a function to the exec list
    def register(func):
        wrapper.pre_exec.append(func)
        return func

    wrapper.before = register
    return wrapper

def after(func):
    """similar to hooks.before except the decorated functions are
    executed after the hooked function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_result = func(*args, **kwargs)
        run = forward_params(func, *args, **kwargs, result = func_result)
        result = [run(f) for f in wrapper.post_exec]
    wrapper.post_exec = []

    # create a decorator which adds a function to the exec list
    def register(func):
        wrapper.post_exec.append(func)
        return func

    wrapper.after = register
    return wrapper
