from pathlib import Path  #3.6+
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()  #leemos el contenido del archivo readme.md y los añadimos a la configuración del paquete

VERSION = '1.0.11'
DESCRIPTION = 'Contiene clases, funciones, constantes comunes para proyectos aws' #breve descripción del paquete
PACKAGE_NAME = 'lambdautility' #nombre del paquete
AUTHOR = '@jfsanz' #nuestro nombre
EMAIL = 'dolgasanz@gmail.com' #nuestro correo
GITHUB_URL = 'https://github.com/juanfcosanz/python_package.git' #dirección de nuestro repositorio en github

setup(
    name = 'aws-lambda-utility',
    packages = [PACKAGE_NAME],
    entry_points={  # le decimos a python que cuando se ejecute el comando pylambdautility, llame la función main del archivo __main__.py del paquete pylambdautility
        'console_scripts': [  
            ["pylambdautility=lambdautility.__main__:main"],
        ]
    },
    version = VERSION,
    description = DESCRIPTION,
    long_description_content_type="text/markdown",  #tipo de maquetado
    long_description=long_description,
    author = AUTHOR,
    author_email = EMAIL,
    url = GITHUB_URL,
    license="GPLv3+", #revisar que licencia necesitamos
    #python_requires="==3.6",
    #packages=find_packages('.', exclude=['tests', 'docs']),
    #package_dir = {'utilities':'lambdautility'},
    keywords = ['aws', 'utilities'], #palabras claves para que los usuarios puedan encontrar nuestro paquete 
    install_requires=[ 
        'boto3',
        'cx-Oracle',
        'PyMySQL',
        'pytz',
        'requests',  #librerías que utilizamos/instalamos en nuestro paquete
        'SQLAlchemy'
    ],
    classifiers=[ #
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent",
    ],
)