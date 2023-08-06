from setuptools import setup, find_packages

VERSION = '0.8'
DESCRIPTION = 'Necro Authenticator'
LONG_DESCRIPTION = 'An authenticator to get real-time verification codes in 2 steps'

setup(
    name="necroauth",
    version=VERSION,
    author="sk4yx",
    author_email="<sk4yx@nikkistealer.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyotp'],
    keywords=['python', 'authenticator', 'necroauth'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)