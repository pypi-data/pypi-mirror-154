from distutils.core import setup
setup(
  name = 'azuretls',
  packages = ['azuretls'],  
  version = '0.2',     
  license='MIT',       
  description = 'TYPE YOUR DESCRIPTION HERE',  
  author = 'Noste',                  
  author_email = 'nooooste@gmail.com',     
  url = 'https://github.com/Noooste/azuretls', 
  download_url = 'https://github.com/Noooste/azuretls/archive/refs/tags/0.2.tar.gz',    # I explain this later on
  keywords = ['TLS', 'API', 'AZURE'],  
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)