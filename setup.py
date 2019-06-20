from setuptools import setup

from scripts.release import get_version

setup(
    name='sanic-prometheus',
    version=f'{get_version()}',
    description='Exposes various prometheus monitoring metrics of Sanic-based apps.',
    url='http://github.com/dkruchinin/sanic-prometheus',
    author='Dan Kruchinin',
    author_email='dan.kruchinin@gmail.com',
    license='MIT',
    packages=['sanic_prometheus'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'sanic>=0.5.0',
        'prometheus-client~=0.5.0',
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
        'Programming Language :: Python :: 3.7'
    ],
    keywords='sanic prometheus monitoring'
)
