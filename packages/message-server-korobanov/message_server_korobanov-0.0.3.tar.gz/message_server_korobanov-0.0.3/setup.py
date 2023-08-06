from setuptools import setup, find_packages

setup(name="message_server_korobanov",
      version="0.0.3",
      description="message_server_korobanov_project",
      author="George Korobanov",
      author_email="georgekorob@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome',
                        'pycryptodomex'],
      long_description_content_type='text/markdown'
      )
