createhook
===================================

Create hooks for function calls using decorators


Installation
==================================

pip install createhook


Usage
==================================

Add a hook to a function

```python
        from createhook impory hooks
        @hooks.before
        def action():
                print('called action')
```


Then access that hook

::

```python
        @action.before
        def before_action():
                print('called before_action')


        @action.before
        def before_action():
                print('called before_action')
```

`before_action()` will be executed before `action()`

```python
        action()
```


Output
```python
        called action
        called before_action
```

