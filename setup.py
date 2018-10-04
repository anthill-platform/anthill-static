
from setuptools import setup, find_packages

DEPENDENCIES = [
    "anthill-common"
]

setup(
    name='anthill-static',
    package_data={
      "anthill.static": ["anthill/static/sql", "anthill/static/static"]
    },
    setup_requires=["pypigit-version"],
    git_version="0.1.0",
    description='Simple static files hosting service (for players to upload)',
    author='desertkun',
    license='MIT',
    author_email='desertkun@gmail.com',
    url='https://github.com/anthill-platform/anthill-static',
    namespace_packages=["anthill"],
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=DEPENDENCIES
)
