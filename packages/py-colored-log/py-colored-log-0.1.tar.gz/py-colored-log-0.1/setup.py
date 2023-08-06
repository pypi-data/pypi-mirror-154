from distutils.core import setup

setup(
  name = 'py-colored-log',
  packages = ['py-colored-log'],
  version = '0.1',
  license='MIT',
  description = 'Lib to color application console logs',
  author = 'Felipe Gomes Machado',
  author_email = 'fgmachado0@gmail.com',
  url = 'https://github.com/fgmachado/py-colored-log',
  download_url = 'https://github.com/fgmachado/py-colored-log/archive/v_01.tar.gz',
  keywords = ['log', 'logger', 'logging', 'color'],
  install_requires = [
          'logging',
          'datetime',
    ],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)