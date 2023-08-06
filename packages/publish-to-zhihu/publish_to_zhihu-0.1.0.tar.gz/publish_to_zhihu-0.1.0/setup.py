# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['publish_to_zhihu']

package_data = \
{'': ['*']}

install_requires = \
['azure-storage-blob>=12.12.0,<13.0.0', 'click>=8.0.4,<9.0.0']

entry_points = \
{'console_scripts': ['zhihu_convert_latex = '
                     'publish_to_zhihu.convert_latex:main',
                     'zhihu_prepare_md = publish_to_zhihu.prepare_md:main',
                     'zhihu_upload_images = '
                     'publish_to_zhihu.upload_images:main']}

setup_kwargs = {
    'name': 'publish-to-zhihu',
    'version': '0.1.0',
    'description': 'Publish markdown to Zhihu',
    'long_description': '# Usage\n\n```bash\npipx install publish_to_zhihu\n\n# convert latex math formula to zhihu format\nzhihu_convert_latex to_be_convert.md\n\n# upload a list of images to azure storage container\nzhihu_upload_images azure_storage_container_name azure_storage_account_connection_string file_root file_rel_path_0 file_rel_path_1\n\n# Convert standard Markdown file to Zhihu Format and upload all local images\nzhihu_prepare_md --container container_name image_link_root output_folder md_file0 md_file1\n\n\n```\n\n# Setup Dev Environment\n\nFirst clone this repo then change to the repo directory.\n\nThen run following command:\n```sh\npip install poetry\npoetry install   # Create virtual environement, install all dependencies for the project\npoetry shell     # activate the virtual environment\npre-commit install    # to ensure automatically formatting, linting, type checking and testing before every commit\n```\n\nIf you want to run unit test manually, just activate virtual environment and run:\n```sh\npytest\n```\n\n# Acknowledgement\n\n- [搭建图床与自动上传 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/258230175)\n- [markdown公式转为知乎格式 - 知乎](https://zhuanlan.zhihu.com/p/87153002)\n',
    'author': 'Anselm Wang',
    'author_email': 'anselmwang@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/anselmwang/publish_to_zhihu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
