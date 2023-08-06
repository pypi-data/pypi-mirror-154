from setuptools import setup, find_packages


setup(
    name='timelapse_slicer',
    version='1.0',
    license='MIT',
    author="Xi Zhao",
    author_email='xz3068@columbia.edu',
    packages=find_packages('timelapse_slicer'),
    package_dir={'': 'timelapse_slicer'},
    url='https://github.com/petez-sufe/timelapse_slicer',
    keywords='timelapse slicer',
    install_requires=[
          'PIL',
      ],

)