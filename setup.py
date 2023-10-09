"""
This file contain information about your package, specifically the name of the package, 
its version, platform-dependencies and a whole lot more.
"""
from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Plug-n-Play AI Chatbot'
LONG_DESCRIPTION = 'AI Chatbot which can answer questions from any given set of documents \
    uploaded using this library. Just integrate the library to your code and you are good to go!'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pnp-chatbot",
        version=VERSION,
        author="Saswat Sahoo",
        author_email="<ss.saswatsahoo@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=['python', 'ai', 'chatbot'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
        ],
        install_requires=["pinecone-client", "openai", "langchain"],
)
