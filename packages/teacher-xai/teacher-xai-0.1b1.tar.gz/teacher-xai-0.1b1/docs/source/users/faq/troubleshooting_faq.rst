.. _troubleshooting-faq:

.. redirect-from:: /faq/troubleshooting_faq

***************
Troubleshooting
***************

.. contents::
   :backlinks: none

.. _matplotlib-version:

Obtaining Matplotlib version
============================

To find out your Matplotlib version number, import it and print the
``__version__`` attribute::

    >>> import matplotlib
    >>> matplotlib.__version__
    '0.98.0'


.. _locating-matplotlib-install:

:file:`matplotlib` install location
===================================

You can find what directory Matplotlib is installed in by importing it
and printing the ``__file__`` attribute::

    >>> import matplotlib
    >>> matplotlib.__file__
    '/home/jdhunter/dev/lib64/python2.5/site-packages/matplotlib/__init__.pyc'

.. _reporting-problems:

Getting help
============

There are a number of good resources for getting help with Matplotlib.
There is a good chance your question has already been asked:

- The `mailing list archive <http://matplotlib.1069221.n5.nabble.com/>`_.

- `GitHub issues <https://github.com/matplotlib/matplotlib/issues>`_.

- Stackoverflow questions tagged `matplotlib
  <https://stackoverflow.com/questions/tagged/matplotlib>`_.

If you are unable to find an answer to your question through search, please
provide the following information in your e-mail to the `mailing list
<https://mail.python.org/mailman/listinfo/matplotlib-users>`_:

* Your operating system (Linux/Unix users: post the output of ``uname -a``).

* Matplotlib version::

     python -c "import matplotlib; print(matplotlib.__version__)"

* Where you obtained Matplotlib (e.g., your Linux distribution's packages,
  GitHub, PyPI, or `Anaconda <https://www.anaconda.com/>`_).

* Any customizations to your ``matplotlibrc`` file.

* If the problem is reproducible, please try to provide a *minimal*, standalone
  Python script that demonstrates the problem.  This is *the* critical step.
  If you can't post a piece of code that we can run and reproduce your error,
  the chances of getting help are significantly diminished.  Very often, the
  mere act of trying to minimize your code to the smallest bit that produces
  the error will help you find a bug in *your* code that is causing the
  problem.

* Matplotlib provides debugging information through the `logging` library, and
  a helper function to set the logging level: one can call ::

    plt.set_loglevel("info")  # or "debug" for more info

  to obtain this debugging information.

  Standard functions from the `logging` module are also applicable; e.g. one
  could call ``logging.basicConfig(level="DEBUG")`` even before importing
  Matplotlib (this is in particular necessary to get the logging info emitted
  during Matplotlib's import), or attach a custom handler to the "matplotlib"
  logger.  This may be useful if you use a custom logging configuration.

If you compiled Matplotlib yourself, please also provide:

* any changes you have made to ``setup.py`` or ``setupext.py``.
* the output of::

     rm -rf build
     python setup.py build

  The beginning of the build output contains lots of details about your
  platform that are useful for the Matplotlib developers to diagnose your
  problem.

* your compiler version -- e.g., ``gcc --version``.

Including this information in your first e-mail to the mailing list
will save a lot of time.

You will likely get a faster response writing to the mailing list than
filing a bug in the bug tracker.  Most developers check the bug
tracker only periodically.  If your problem has been determined to be
a bug and can not be quickly solved, you may be asked to file a bug in
the tracker so the issue doesn't get lost.

.. _git-trouble:

Problems with recent git versions
=================================

First make sure you have a clean build and install (see clean-install),
get the latest git update, install it and run a simple test script in debug
mode::

    rm -rf /path/to/site-packages/matplotlib*
    git clean -xdf
    git pull
    python -m pip install -v . > build.out
    python -c "from pylab import *; set_loglevel('debug'); plot(); show()" > run.out

and post :file:`build.out` and :file:`run.out` to the `matplotlib-devel
<https://mail.python.org/mailman/listinfo/matplotlib-devel>`_
mailing list (please do not post git problems to the `users list
<https://mail.python.org/mailman/listinfo/matplotlib-users>`_).

Of course, you will want to clearly describe your problem, what you
are expecting and what you are getting, but often a clean build and
install will help.  See also :ref:`reporting-problems`.
