__author__ = "Jianfeng Sun"
__version__ = "v1.0"
__copyright__ = "Copyright 2022"
__license__ = "MIT"
__email__ = "jianfeng.sunmt@gmail.com"
__maintainer__ = "Jianfeng Sun"

import urllib.request
import click


@click.group()
def main():
    pass

@click.command()
@click.option('-u', '--url', default='https://github.com/2003100127/deepsmirud/releases/download/model/model.zip', help='URL of deepsmirud models')
@click.option('-o', '--output_path', default='./model.zip', help='output path of deepsmirud models')
def download(url, fpn):
    print('downloading...')
    urllib.request.urlretrieve(
        url=url,
        filename=fpn
    )
    print('downloaded!')
    return

#
# if __name__ == '__main__':
#     main()