import setuptools

with open("README.md","r", encoding="utf-8") as fh:
	long_description = fh.read()
	
setuptools.setup(
  name = "contentassistant",
  version = "0.0.1",
  author = "Caio Souza",
  author_email = "caios@take.net",
  description = "Manipulação do assistente de conteúdo",
  long_description = long_description,
  long_description_content_type="text/markdown",
  keywords = [],
  install_requires=[
  'pandas',
  'ujson',
  'requests',
  'uuid'
  ],
  classifiers=[  
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
	"Operating System :: OS Independent",
    "Programming Language :: Python :: 3"
  ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)