from distutils.core import setup

setup(
    name='nfms4redd-cli',
    packages=['nfms4redd'],
    version='0.0.1',
    description='NFMS4REDD CLI',
    author='geomati.co',
    author_email='info@geomati.co',
    url='https://github.com/nfms4redd/admin-tools',
    download_url='https://github.com/nfms4redd/admin-tools/archive/0.1.0.tar.gz',
    keywords=['nfms4redd', 'fao', 'unredd',
              'nfms', 'snmb', 'cli', 'geoladris'],
    classifiers=[],
    scripts=['nfms4redd/portal', 'nfms4redd/monit-config'],
    install_requires=['requests']
)
