from setuptools import setup, find_packages


setup(
    name='necroauth',
    version='0.6',
    license='MIT',
    author="sk4yx",
    author_email='sk4yx@nikkistealer.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='authenticator',
    install_requires=[
          'pyotp',
      ],

)