from setuptools import setup, find_packages

setup(
    name='micro_config',
    version='0.1',
    license='MIT',
    author="Charlie Snell",
    author_email='csnell22@berkeley.edu',
    description='A deep learning config framework based on hierarchical dataclasses.',
    py_modules=["micro_config"],
    url='https://github.com/Sea-Snell/micro_config',
    keywords='configs configuration dataclasses deeplearning hierarchy hierarchical',
    install_requires=[
          'torch',
      ],
    python_requires='>=3',
    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ], 
)