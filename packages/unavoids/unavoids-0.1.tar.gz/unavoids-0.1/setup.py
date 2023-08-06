from setuptools import setup, find_packages


setup(
    name='unavoids',
    version='0.1',
    license='GNU',
    author="Yousef, Waleed A. and Traoré, Issa and Briguglio, William",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/isotlaboratory/UNAVOIDS-Code',
    keywords='unavoids',
    install_requires=[
          'numpy',
		  'sklearn',
		  'functools',
		  'multiprocessing',
		  'os', 
		  'decimal',
		  'warnings',
		  'sys',
		  'time',
		  'pyod.models'
      ],

)
