from setuptools import setup, Extension

NAME = 'clickhouse-toolset'
VERSION = '0.20.dev0'

try:
    from conf import *
    chquery = Extension(
        'chtoolset._query',
        sources=['src/query.cpp', 'src/TBQueryParser.cpp'],
        depends=['conf.py',
                 'src/ClickHouseQuery.h',
                 'src/PythonThreadHandler.h',
                 'src/TBQueryParser.h']
    )
    setup(
        name=NAME,
        version=VERSION,
        url='https://gitlab.com/tinybird/clickhouse-toolset',
        author='Tinybird.co',
        author_email='support@tinybird.co',
        packages=['chtoolset'],
        package_dir={'': 'src'},
        python_requires='>=3.7, <3.12',
        install_requires=[],
        extras_require={
            'test': requirements_from_file('requirements-test.txt')
        },
        cmdclass={
            'clickhouse': ClickHouseBuildExt,
            'build_ext': CustomBuildWithFromCH,
        },
        ext_modules=[chquery]
    )

except ModuleNotFoundError:
    setup(
        name=NAME,
        version=VERSION,
        url='https://gitlab.com/tinybird/clickhouse-toolset',
        author='Tinybird.co',
        author_email='support@tinybird.co',
        packages=['chtoolset'],
        package_dir={'': 'src'},
        python_requires='>=3.7, <3.12',
        install_requires=[],
    )
