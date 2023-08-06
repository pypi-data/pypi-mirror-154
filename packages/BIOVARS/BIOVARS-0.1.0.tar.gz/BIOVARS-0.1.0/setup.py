from distutils.core import setup
setup(
  name = 'BIOVARS',         
  packages = ['biovars'],  
  version = '0.1.0',
  license='GNU General Public License v3.0',
  description = "Tool for joining all the bioinfo-hcpa's variant information retrieval APIs.",   
  author = 'Felipe Colombelli, Paola Carneiro',                   
  author_email = 'bioinfo@hcpa.edu.br',
  url = 'https://github.com/bioinfo-hcpa/biovars',
  keywords = ['gnomad', 'api', 'variants', 'genes'],
  install_requires=[
          'pandas>=1.0.5',
          'numpy>=1.19.0',
          'requests>=2.24.0',
          'seaborn',
          'rpy2',
          'pynoma',
          'pyabraom'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.6',
  ],
)
