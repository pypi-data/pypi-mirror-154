from setuptools import setup

setup(name='avocadopml',
      packages=['avocadopml'],
      version='1.0.0',
      install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'sklearn',
        'xgboost',
        'pytest'
      ],
      package_dir={'avocadopml': 'avocadopml'},
      package_data={'': ['data/*']}
)