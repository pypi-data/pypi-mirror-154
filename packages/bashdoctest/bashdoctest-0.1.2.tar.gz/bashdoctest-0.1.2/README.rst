===========================================
Bashdoctest Command Line Application Tester
===========================================

Bashdoctest is a fork of the original "clatter" repo, which is a doctest-style testing tool for command-line applications. It wraps other testing suites and allows them to be tested in docstrings.

* Free software: MIT license
* Original Documentation: https://clatter.readthedocs.io.


Features
--------

* Bring testing best practices to your command line apps
* Extensible - subclassing CommandValidator is trivial using any cli testing suite
* Easily test your documentation. This README is a valid doctest!


Usage
-----

.. code-block:: python

    >>> from bashdoctest import Runner
    >>> from bashdoctest.validators import SubprocessValidator

Test command line utilities and applications by whitelisting them with app-specific testing engines:

.. code-block:: python

    >>> test_str = r'''
    ... 
    ... .. code-block:: bash
    ... 
    ...     $ echo 'Pining for the fjords'
    ...     Pining for the fjords
    ... '''
    >>>
    >>> tester = Runner()
    >>> tester.call_engines['echo'] = SubprocessValidator()
    >>> tester.teststring(test_str)
    # echo 'Pining for the fjords'

Click applications
~~~~~~~~~~~~~~~~~~

Integrate your command line app:

.. code-block:: python
    
    >>> import click
    >>> @click.command()
    ... @click.argument('name')
    ... def hello(name):
    ...     click.echo('Hello %s!' % name)

This can now be tested in docstrings:

.. code-block:: python

    >>> test_str = '''
    ... 
    ... .. code-block:: bash
    ... 
    ...     $ hello Polly
    ...     Hello Polly!
    ... 
    ...     $ hello Polly Parrot
    ...     Usage: hello [OPTIONS] NAME
    ...     Try "hello --help" for help.
    ...     <BLANKLINE>
    ...     Error: Got unexpected extra argument (Parrot)
    ... 
    ...     $ hello 'Polly Parrot'
    ...     Hello Polly Parrot!
    ... 
    ... '''

Click applications can be tested with a ``ClickValidator`` engine:

.. code-block:: python

    >>> from bashdoctest.validators import ClickValidator
    >>> tester = Runner()
    >>> tester.call_engines['hello'] = ClickValidator(hello)

    >>> tester.teststring(test_str)
    # hello Polly
    # hello Polly Parrot
    # hello 'Polly Parrot'


Mixed applications
~~~~~~~~~~~~~~~~~~

Your app can be combined with other command-line utilities by adding multiple engines:

.. code-block:: python

    >>> test_str = r'''
    ... 
    ... .. code-block:: bash
    ... 
    ...     $ hello Polly
    ...     Hello Polly!
    ... 
    ...     $ echo 'Pining for the fjords'
    ...     Pining for the fjords
    ... 
    ... Pipes/redirects don't work, so we can't redirect this value into a file.
    ... But we can write a file with python:
    ... 
    ... .. code-block:: bash
    ... 
    ...     $ python -c \
    ...     >     "with open('tmp.txt', 'w+') as f: f.write('Pushing up daisies')"
    ... 
    ...     $ cat tmp.txt
    ...     Pushing up daisies
    ...
    ... '''

    >>> tester.call_engines['echo'] = SubprocessValidator()
    >>> tester.call_engines['python'] = SubprocessValidator()
    >>> tester.call_engines['cat'] = SubprocessValidator()

    >>> tester.teststring(test_str)
    # hello Polly
    # echo 'Pining for the fjords'
    # python -c "with open('tmp.txt', 'w+') as f: f.write('Pushing up daisies')"
    # cat tmp.txt

Suppressing commands
~~~~~~~~~~~~~~~~~~~~

Commands can be skipped altogether with a ``SkipValidator``:

.. code-block:: python

    >>> test_str = '''
    ... .. code-block:: bash
    ... 
    ...     $ aws storage buckets list --password $MY_PASSWORD
    ... 
    ... '''

    >>> from bashdoctest.validators import SkipValidator
    >>> tester.call_engines['aws'] = SkipValidator()

    >>> tester.teststring(test_str)
    # aws storage ...


Illegal commands
~~~~~~~~~~~~~~~~

Errors are raised when using an application you haven't whitelisted:

.. code-block:: python

    >>> test_str = '''
    ...
    ... The following block of code should cause an error:
    ...
    ... .. code-block:: bash
    ...
    ...     $ rm tmp.txt
    ...
    ... '''

    >>> tester.teststring(test_str) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Command "rm" not allowed. Add command caller to call_engines to whitelist.

Unrecognized commands will not raise an error if +SKIP is specified

.. doctest's skip here will be interpreted by doctest, not bashdoctest. So we mock the code here.

    >>> test_str = r'''
    ...
    ... .. code-block:: bash
    ...
    ...     $ nmake all # doctest
    ...     $ echo 'I made it!'
    ...     I made it!
    ...
    ... '''
    >>> test_str = test_str.replace('ctest', 'ctest: +SKIP')

.. code-block:: python

    >>> test_str = r'''
    ...
    ... .. code-block:: bash
    ...
    ...     $ nmake all # doctest: +SKIP
    ...     $ echo 'I made it!'
    ...     I made it!
    ...
    ... '''
    >>> tester.teststring(test_str)
    # nmake all

Error handling
~~~~~~~~~~~~~~

Lines failing to match the command's output will raise an error

.. code-block:: python

    >>> test_str = r'''
    ... .. code-block:: bash
    ... 
    ...     $ echo "There, it moved!"
    ...     "No it didn't!"
    ... 
    ... '''
    
    >>> tester = Runner()
    >>> tester.call_engines['echo'] = SubprocessValidator()
    
    >>> tester.teststring(test_str) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Differences (ndiff with -expected +actual):
        - "No it didn't!"
        + There, it moved!

Known issues
------------

We have issues on our `issues <https://github.com/juledwar/bashdoctest/issues>`_ page. But we want to be very up-front about these.

Security
~~~~~~~~

Similar to ``doctest``, executing arbitrary commands from within your tests is dangerous, and we make no attempt to protect you. We won't run commands you don't whitelist, but we cant't prevent against malicious cases. Don't run anything you don't understand, and use at your own risk.

Syntactic completeness
~~~~~~~~~~~~~~~~~~~~~~

Bashhdoctest is not a syntactically complete bash emulator and has no intention of being so.

All arguments to commands are passed as arguments to the first command. Therefore, loops, pipes, redirects, and other control-flow and IO commands will not work as expected.

.. code-block:: python
    
    >>> test_str = '''
    ...    $ echo hello > test.txt
    ...    $ cat test.txt    
    ...    hello
    ...
    ... '''
    >>> tester.teststring(test_str) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Differences (ndiff with -expected +actual):
        + hello > test.txt
    <BLANKLINE>



Installation
------------

``pip install bashhdoctest``


Requirements
------------

* pytest


Todo
----

See `issues <https://github.com/juledwar/bashdoctest/issues>`_ to see and add to our todos.


