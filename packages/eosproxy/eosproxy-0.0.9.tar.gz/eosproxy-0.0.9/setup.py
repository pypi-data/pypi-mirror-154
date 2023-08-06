from setuptools import setup, find_packages

setup(name='eosproxy',
      version='0.0.9',
      description='Python eos API with proxy',
      long_description='Python library for the eos.io REST API with proxy',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='eos wax',
      url='',
      author='',
      author_email='',
      license='',
      packages=find_packages(),
      install_requires=[
          'base58', 'colander', 'ecdsa', 'pytz', 'pyyaml', 'requests', 'six'
      ],
      include_package_data=True,
      zip_safe=False)
