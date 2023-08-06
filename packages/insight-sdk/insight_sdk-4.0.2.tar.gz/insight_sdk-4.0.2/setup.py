from setuptools import find_packages
from setuptools import setup

setup(
    name="insight_sdk",
    author="htsc",
    version="4.0.2",
    author_email="insight@htsc.com",
    description="insight_sdk",
    long_description="insight_sdk",
    license='insightpythonsdk',
    project_urls={
        'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/pypa/sampleproject/',
        'Tracker': 'https://github.com/pypa/sampleproject/issues',
    },


    packages= ['insight_sdk',
               'insight_sdk/com',
               'insight_sdk/com/interface',
               'insight_sdk/com/libs/python37/x64',
               'insight_sdk/com/libs/python36/x64',
               'insight_sdk/com/libs/python39/x64',
               'insight_sdk/com/cert',
               'insight_sdk/com/insight'
               ],
    package_dir={'insight_sdk/com/cert': 'insight_sdk/com/cert',
                 'insight_sdk/com/libs/python37/x64':
                     'insight_sdk/com/libs/python37/x64',
                  'insight_sdk/com/libs/python36/x64':
                     'insight_sdk/com/libs/python36/x64'},
    package_data={'insight_sdk/com/cert': ['HTInsightCA.crt', 'InsightClientCert.pem', 'HTISCA.crt', 'InsightClientKeyPkcs8.pem'],
                  'insight_sdk/com/libs/python37/x64': ['_mdc_gateway_client.pyd', 'ACE.dll', 'ACE_SSL.dll', 'libeay32.dll', "ssleay32.dll"],
                  'insight_sdk/com/libs/python36/x64': ['_mdc_gateway_client.pyd', 'ACE.dll', 'ACE_SSL.dll', 'libeay32.dll', "ssleay32.dll"]},
    install_requires=[],

    python_requires='>=3.6.*',
)