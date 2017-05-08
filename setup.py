from setuptools import setup

setup(
    name='sanic-prometheus',
    version='0.1.3',
    description='Exposes various prometheus monitoring metrics of Sanic-based apps.',
    url='http://github.com/dkruchinin/sanic-prometheus',
    author='Dan Kruchinin',
    author_email='dkruchinin@acm.org',
    license='MIT',
    packages=['sanic_prometheus'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'sanic>=0.5.0',
        'prometheus-client>=0.0.19',
        'psutil>=5.2.0'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Topic :: System :: Monitoring',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='sanic prometheus monitoring'
)
