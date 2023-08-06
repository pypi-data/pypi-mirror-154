from distutils.core import setup

packages=["everywhereml", "everywhereml.plot", "everywhereml.sklearn", "everywhereml.sklearn.tree", "everywhereml.sklearn.tree.templates", "everywhereml.sklearn.ensemble", "everywhereml.sklearn.ensemble.templates", "everywhereml.get_started", "everywhereml.code_generators", "everywhereml.code_generators.jinja", "everywhereml.code_generators.jinja.filters", "everywhereml.templates", "everywhereml.templates.cpp", "everywhereml.preprocessing", "everywhereml.preprocessing.templates", "everywhereml.data", "everywhereml.data.collect"]
data=["sklearn/tree/templates/tree.cpp.jinja", "sklearn/tree/templates/DecisionTreeClassifier.cpp.jinja", "sklearn/ensemble/templates/tree.cpp.jinja", "sklearn/ensemble/templates/RandomForestClassifier.cpp.jinja", "templates/latency.cpp.jinja", "templates/vote.cpp.jinja", "templates/class_map.cpp.jinja", "templates/BaseClassifier.cpp.jinja", "preprocessing/templates/Step.cpp.jinja", "preprocessing/templates/Pipeline.cpp.jinja", "preprocessing/templates/SpectralFeatures.cpp.jinja", "preprocessing/templates/Window.cpp.jinja", "preprocessing/templates/MinMaxScaler.cpp.jinja"]

setup(
  name='everywhereml',
  packages=packages,
  version='0.0.3',
  license='MIT',
  description='Train ML in Python, run everywhere',
  author='Simone Salerno',
  author_email='support@eloquentarduino.com',
  url='https://github.com/eloquentarduino/everywhereml',
  download_url='https://github.com/eloquentarduino/everywhereml/blob/master/dist/everywhereml-0.0.3.tar.gz?raw=true',
  keywords=[
    'ML',
    'machine learning'
  ],
  install_requires=[
    'numpy',
    'pandas',
    'seaborn',
    'scikit-learn',
    'Jinja2',
    'cached-property',
  ],
  package_data={
    'everywhereml': data
  },
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Code Generators',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
