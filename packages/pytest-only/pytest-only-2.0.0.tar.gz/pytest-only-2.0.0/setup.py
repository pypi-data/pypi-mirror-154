# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_only', 'pytest_only.ext']

package_data = \
{'': ['*']}

extras_require = \
{':python_version <= "3.6"': ['pytest<7.1'],
 ':python_version >= "3.7" and python_version < "4.0"': ['pytest>=7.1']}

entry_points = \
{'pytest11': ['only = pytest_only.plugin']}

setup_kwargs = {
    'name': 'pytest-only',
    'version': '2.0.0',
    'description': 'Use @pytest.mark.only to run a single test',
    'long_description': 'pytest-only\n===========\n\nOnly run tests marked with ``@pytest.mark.only``. If none are marked, all tests run as usual.\n\nBorrowed from `mocha <https://mochajs.org/>`_.\n\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    pip install pytest-only\n\n\nUsage\n-----\n\nUse it on functions\n\n.. code-block:: python\n\n    import pytest\n\n    def test_that_will_not_run():\n        assert 0\n\n    @pytest.mark.only\n    def test_that_will_run():\n        assert 1\n\n\n.. code-block:: bash\n\n    $ py.test -v test_example.py\n\n    ============================= test session starts ==============================\n    platform linux -- Python 3.6.1, pytest-3.0.7, py-1.4.33, pluggy-0.4.0 -- /tmp/example/bin/python3.6\n    cachedir: .cache\n    rootdir: /tmp/example, inifile:\n    plugins: only-1.0.0\n    collected 2 items\n\n    test_example.py::test_that_will_run PASSED\n\n    =========================== 1 passed in 0.00 seconds ===========================\n\n\nOr use it on classes\n\n.. code-block:: python\n\n    import pytest\n\n    class TestThatWillNotRun:\n        def test_that_will_not_run(self):\n            assert 0\n\n\n    @pytest.mark.only\n    class TestThatWillRun:\n        def test_that_will_run(self):\n            assert 1\n\n\n.. code-block:: bash\n\n    $ py.test -v test_example.py\n\n    ============================= test session starts ==============================\n    platform linux -- Python 3.6.1, pytest-3.0.7, py-1.4.33, pluggy-0.4.0 -- /tmp/example/bin/python3.6\n    cachedir: .cache\n    rootdir: /tmp/example, inifile:\n    plugins: only-1.0.0\n    collected 2 items\n\n    test_example.py::TestThatWillRun::test_that_will_run PASSED\n\n    =========================== 1 passed in 0.00 seconds ===========================\n\n\nOr use it on modules\n\n.. code-block:: python\n\n    # test_example.py\n    import pytest\n\n    pytestmark = pytest.mark.only\n\n    def test_that_will_run():\n        assert 1\n\n\n.. code-block:: python\n\n    # test_example2.py\n    def test_that_will_not_run():\n        assert 0\n\n\n.. code-block:: bash\n\n    $ py.test -v test_example.py test_example2.py\n\n    ============================= test session starts ==============================\n    platform linux -- Python 3.6.1, pytest-3.0.7, py-1.4.33, pluggy-0.4.0 -- /home/they4kman/.virtualenvs/tmp-53d5944c7c78d28/bin/python3.6\n    cachedir: .cache\n    rootdir: /home/they4kman/.virtualenvs/tmp-53d5944c7c78d28, inifile:\n    plugins: only-1.0.0\n    collected 2 items\n\n    test_example.py::test_that_will_run PASSED\n\n    =========================== 1 passed in 0.00 seconds ===========================\n\n\n\nDisable for single test run\n---------------------------\n\nTo run all the tests, regardless of whether ``@pytest.mark.only`` is used, pass\nthe ``--no-only`` flag to pytest:\n\n.. code-block:: bash\n\n    $ py.test --no-only\n\n\nIf ``--no-only`` has already been passed (perhaps by way of ``addopts`` in\n*pytest.ini*), use the ``--only`` flag to re-enable it:\n\n.. code-block:: bash\n\n    $ py.test --no-only --only\n\n\nPylint checker\n--------------\n\nIf you use pylint, you can avoid committing stray `only` marks with the bundled plugin. Just enable the pylint checker in your plugins and enable the `unexpected-focused` rule.\n\n.. code-block:: ini\n\n    [MASTER]\n    load-plugins=pytest_only.ext.pylint\n\n    [MESSAGES CONTROL]\n    enable=unexpected-focused\n\n.. code-block:: console\n\n    $ cat test_ninja.py\n    import pytest\n\n    @pytest.mark.only\n    def test_ninja():\n        pass\n\n    $ pylint test_ninja.py\n    ************* Module mymain\n    test_ninja.py:3:0: W1650: Unexpected focused test(s) using pytest.mark.only: def test_ninja (unexpected-focused)\n\n\nDevelopment\n-----------\n\n1. Install the test/dev requirements using `Poetry <https://python-poetry.org/>`_\n\n    .. code-block:: bash\n\n        poetry install\n\n2. Run the tests\n\n    .. code-block:: bash\n\n        py.test\n\n3. Run the tests on all currently-supported platforms\n\n    .. code-block:: bash\n\n        tox\n',
    'author': 'Zach Kanzler',
    'author_email': 'they4kman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theY4Kman/pytest-only',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
