import setuptools

from version import __version__
# CalVer: https://calver.org/
# Ubuntu is using CalVer format: YY.0M.MICRO

''' 
    Entry point schema:
        mypyliex_printer - command_name
        mypyliex_printer = library_folder.submodule_folder.submodule_folder_name.module_name:function_name
        mypyliex_printer = mypyliex      .tools           .printer              .printer    :main
'''


setuptools.setup(
    name='mypyliex',
    version=__version__,
    author='Tadeusz Miszczyk',
    author_email='tadeusz.miszczyk@email.com',
    description='Short project description - this is example of simple library',
    url='https://github.com/8tm/mypyliex',
    package_dir={'': 'src'},
    packages=setuptools.find_namespace_packages(where='src'),
    include_package_data=True,
    install_requires=[],
    extras_require={
        'test': [
            'flake8==3.8.3',
            'flake8-commas==2.0.0',
            'flake8-import-order==0.18.1',
            'flake8-quotes==3.2.0',

            'pytest==6.0.1',
            'pytest-cov==2.10.0',
            'pytest-mock==3.2.0',
            'pytest-random-order==1.0.4',
            'pytest-xdist==1.29.0',
            'pytest-parallel',

            'mypy==0.812',
        ],
        'tools': [
            'pip-search==0.0.7',
        ],
    },
    python_requires='>=3.7.0',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: Unix',
    ],
    entry_points={
        'console_scripts': [
            'mypyliex_printer = mypyliex.tools.printer.printer:main',
            'mypyliex_next_tool_name = mypyliex.tools.next_tool_name.next_tool_name:main',
            'mypyliex_other_tool_name = mypyliex.tools.other_tool_name.other_tool_name:main',
        ],
    },
)
