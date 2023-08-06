# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mmodel']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.16', 'h5py>=3.6.0', 'networkx>=2.8.3']

extras_require = \
{'docs': ['sphinx>=4.5.0,<5.0.0',
          'sphinx-book-theme>=0.3.2,<0.4.0',
          'nbsphinx>=0.8.8,<0.9.0'],
 'test': ['pytest>=7.1.1', 'pytest-cov>=3.0.0']}

setup_kwargs = {
    'name': 'mmodel',
    'version': '0.3.0',
    'description': 'Modular modeling framework for nonlinear scientific models',
    'long_description': 'MModel\n======\n\nMModel is a lightweight and modular model building framework\nfor small-scale and nonlinear models. The package aims to solve\nscientific program prototyping and distribution difficulties, making\nit easier to create modular, fast, and user-friendly packages. The package\nis well tested with 100 % coverage.\n\nQuickstart\n----------\n\nTo create a nonlinear model that has the result of\n`(x + y)log(x + y, base)`:\n\n.. code-block:: python\n\n    from mmodel import ModelGraph, Model, MemHandler\n    import math\n\n    def func_a(x, y):\n        return x + y\n\n    def func_b(sum_xy, base):\n        return math.log(sum_xy, base)\n\n    def func_c(sum_xy, log_xy):\n        return sum_xy * log_xy\n\n    # create graph links\n\n    grouped_edges = [\n        ("func a", ["func b", "func c"]),\n        ("func b", "func c"),\n    ]\n\n    node_objects = [\n        ("func a", func_a, ["sum_xy"]),\n        ("func b", func_b, ["log_xy"]),\n        ("func c", func_c, ["result"]),\n    ]\n\n    graph = ModelGraph(name="Example")\n    graph.add_grouped_edges_from(grouped_edges)\n    graph.set_node_objects_from(node_objects)\n\n    example_func = Model(graph, handler=MemHandler)\n\n    >>> print(example_func)\n    Example model\n      signature: base, x, y\n      returns: result\n      handler: MemHandler\n      modifiers: none\n\n    >>> example_func(2, 5, 3) # (5 + 3)log(5 + 3, 2)\n    24.0\n\nThe resulting ``example_func`` is callable.\n\nOne key feature of ``mmodel`` is modifiers, which modify callables post\ndefinition. To loop the "base" parameter.\n\n.. code-block:: python \n\n    from mmodel import subgraph_by_parameters, modify_subgraph, loop_modifier\n\n    subgraph = subgraph_by_parameters(graph, ["base"])\n    loop_node = Model(subgraph, MemHandler, [loop_modifier("base")])\n    looped_graph = modify_subgraph(graph, subgraph, "loop node", loop_node)\n    looped_model = Model(looped_graph, handler=MemHandler)\n\n    >>> print(looped_model)\n    Example model\n      signature: base, x, y\n      returns: result\n      handler: MemHandler\n      modifiers: none\n    \n    >>> looped_model([2, 4], 5, 3) # (5 + 3)log(5 + 3, 2)\n    [24.0, 12.0]\n\n\nModifiers can also be added to the whole model or a single node.\n\nTo draw the graph or the underlying graph of the model:\n\n.. code-block:: python\n    \n    graph.draw()\n    example_func.draw()\n\nInstallation\n------------\n\nGraphviz installation\n^^^^^^^^^^^^^^^^^^^^^\n\nTo view the graph, Graphviz needs to be installed:\n`Graphviz Installation <https://graphviz.org/download/>`_\nFor windows installation, please choose "add Graphviz to the\nsystem PATH for all users/current users" during the setup.\n\n``mmodel`` installation\n^^^^^^^^^^^^^^^^^^^^^^^\n\n.. code-block::\n\n    pip install mmodel\n\nDevelopment installation\n^^^^^^^^^^^^^^^^^^^^^^^^\n``mmodel`` uses `poetry <https://python-poetry.org/docs/>`_ as\nthe build system. The package works with both pip and poetry\ninstallation. \n\nTo install test and docs, despondencies run::\n\n    pip install .[test] .[docs]\n\n(For ``zsh`` shell, run ``pip install ".[test]"``)\n\nTo run the tests, run::\n\n    pytest\n\nTo run the tests in different python environments (py38, py39,\ncoverage and docs)::\n\n    tox\n\nTo create the documentation, run under the "/docs" directory::\n\n    make html\n',
    'author': 'Peter Sun',
    'author_email': 'hs859@cornell.edu',
    'maintainer': 'Peter Sun',
    'maintainer_email': 'hs859@cornell.edu',
    'url': 'https://github.com/peterhs73/MModel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
