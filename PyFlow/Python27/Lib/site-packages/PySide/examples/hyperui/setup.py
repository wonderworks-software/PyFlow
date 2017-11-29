
from distutils.core import setup

setup(name='HyperUI Demo',
      version='1.0',
      description='HyperUI Demo',
      author='Renato Filho',
      author_email='renato.filho@openbossa.org',
      packages=['hyperuilib', 'hyperuilib.shared', 'hyperuilib.resource'],
      scripts=['hyperui']
      )

