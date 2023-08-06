from setuptools import setup
    
requirements = ["biopython>=1.79", "argparse>=1.4.0"]

setup(
    name='convertFQ',
    version='0.1.0',
    description='convertFQ is used to convert either DNA2RNA or RNA2DNA in a fastq file',
    url='https://github.com/NuruddinKhoiry/convertFQ.git',
    author='Ahmad Nuruddin Khoiri',
    author_email='nuruddinkhoiri34@gmail.com',
    license='GNU GENERAL PUBLIC LICENSE V3',
    packages=['convertFQ'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'convertFQ = convertFQ.convertFQ:main'
        ]
    },
)
