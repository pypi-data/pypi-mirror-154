[metadata]
name = $pkgname
version = $version
author = $author
author_email = $author_email
description = $description
long_description = file: README.md
long_description_content_type = text/markdown
license_files = LICENSE
url = # add a URL here
classifiers =
    Programming Language :: Python :: 3
    Operating System :: Unix
    # add more classifiers from https://pypi.org/classifiers/

[options]
zip_safe = False
package_dir=
    =src
packages=find:
python_requires = >=$python_requires
install_requires = $dependencies
    # add package dependencies here

[options.packages.find]
where = src

[options.entry_points]
console_scripts =
    $pkgname = ${pkgname}.scripts.${pkgname}:main

[options.extras_require]
${use_sphinx}docs =
${use_sphinx}    sphinx>=4.5.0
${use_sphinx}    sphinx-rtd-theme>=1.0.0
${use_sphinx}    sphinxcontrib-napoleon>=0.7

${use_tf}tf = tensorflow
${use_tf}tf-gpu = tensorflow-gpu
${use_tf}tf-cpu = tensorflow-cpu
${use_tf}tf-amd = tensorflow-rocm
