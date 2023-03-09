from setuptools import setup

from scripts.release import get_version

setup(
    name='sanic-prometheus',
    version=f'{get_version()}',
    description='Exposes Prometheus monitoring metrics of Sanic apps.',
    url='http://github.com/AltanAlpay/sanic-prometheus',
    author='Dan Kruchinin, Altan Alpay',
    author_email='dan.kruchinin@gmail.com, altan.alpay@gmail.com',
    license='MIT',
    packages=['sanic_prometheus'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'sanic>=22.12.0',
        'prometheus-client~=0.16.0',
        'psutil>=5.6.6',
        'ujson>=5.4.0'
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

        'Programming Language :: Python :: 3.11'
    ],
    keywords='sanic prometheus monitoring'
)
