from distutils.core import setup

setup(
    name='ofxReaderBR',
    packages=['ofxReaderBR',
              'ofxReaderBR.model',
              'ofxReaderBR.reader'],
    version='0.16.13',
    license='MIT',
    description='Convert ofx - pt_BR',
    author='Fintask',
    author_email='admin@fintask.com.br',
    url='https://github.com/Fintask/ofxReaderBR/',
    download_url='https://github.com/Fintask/ofxReaderBR/archive/v0.16.0.tar.gz',
    keywords=['ofx', 'xlsx'],
    install_requires=[
        'lxml==4.5.1',
        'ofxtools==0.8.22',
        'openpyxl==3.0.5',
        'pandas==1.3.5',
        'pypdf2==1.28.4',
        'xlrd==2.0.1',
        'unidecode'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
