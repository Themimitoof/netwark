import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pypugjs',
    'alembic',
    'psycopg2-binary',
    'SQLAlchemy',
    'pyramid_tm',
    'transaction',
    'pyramid_retry',
    'zope.sqlalchemy',
    'celery',
    'geoip2',
    'idna',
    'pyyaml'
]

dev_require = [
    'plaster_pastedeploy',
    'waitress',
    'pyramid_debugtoolbar',
    'pycodestyle',
    'sphinx',
    'sphinc-rtd-theme',
    'cornice_swagger',
    'sphinxcontrib-openapi',
    'black',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest >= 3.7.4',
    'pytest-cov',
]

setup(
    name='netwark',
    version='1.0.0',
    description='netwark',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Michael Vieira',
    author_email='contact+dev[âT]mvieira[d¤T]fr',
    url='https://github.com/themimitoof/netwark',
    keywords='network tools ping mtr traceroute geoip lookup as pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={'testing': tests_require, 'dev': dev_require},
    install_requires=requires,
    entry_points={
        'paste.app_factory': ['main = netwark:main'],
        'console_scripts': [
            'initialize_netwark_db=netwark.bin.initialize_db:main'
        ],
    },
)
