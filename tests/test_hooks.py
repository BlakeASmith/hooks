from test import *
import hooks
import sys

class TestBefore(unittest.TestCase):
    def test_before_hook(self):
        print("testing hooks.before")
        text = ''
        @hooks.before
        def action(param, **others):
            print('called_action')
            nonlocal text
            text += param
            #print(before_results)
            #assert(before_results is not None)
            print(others)
            assert(len(others) == 3)


        @action.before
        @hooks.before
        def before_action(param):
            print('called_before')
            nonlocal text
            text += param
            return 'before_result'


        @before_action.before
        def first():
            print('called_first')
            nonlocal text
            text += 'first'


        action("text", another='foo', other='bar')
        print(text)
        assert(text == 'firsttexttext')

    def test_after_hook(self):
        print ('testing hooks.after')
        text = ''

        @hooks.after
        def action(*args, **kwargs):
            print(f'called action: {text}')
            return "result"

        @action.after
        def afteraction(result, *args,  key = 'foo', **kwargs):
            nonlocal text
            text += result
            text += key
            assert('otherkwarg' in kwargs)
            assert('test' in args)
            print(f'called afteraction: {text}')

        action('test', key = 'key', otherkwarg = 'other')

        assert(text == 'resultkey')


if __name__ == '__main__':
    unittest.main()
