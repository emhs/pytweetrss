from setuptools import setup

setup(
    name='pytweetrss',
    version='0.5',
    py_modules=['pytweetrss'],
    install_requires=[
        'click',
        'python-twitter',
        'bitly-api',
        'feedparser',
        'requests-oauthlib'],
    entry_points="""
    [console_scripts]
    pytweetrss=pytweetrss:main
""")
