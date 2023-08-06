from setuptools import setup, find_packages

setup(name="message_client_korobanov",
      version="0.0.2",
      description="message_client_korobanov_project",
      author="George Korobanov",
      author_email="georgekorob@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
