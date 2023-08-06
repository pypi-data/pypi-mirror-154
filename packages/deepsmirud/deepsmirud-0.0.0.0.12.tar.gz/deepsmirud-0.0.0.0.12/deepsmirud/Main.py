__author__ = "Jianfeng Sun"
__version__ = "v1.0"
__copyright__ = "Copyright 2022"
__license__ = "MIT"
__email__ = "jianfeng.sunmt@gmail.com"
__maintainer__ = "Jianfeng Sun"

import urllib.request
import click
from deepsmirud.Run import predict


@click.command()
@click.option('-u', '--url', default='https://github.com/2003100127/deepsmirud/releases/download/model/model.zip', help='URL of deepsmirud models')
@click.option('-o', '--output_path', default='./model.zip', help='output path of deepsmirud models')
def download(url, output_path):
    print('downloading...')
    urllib.request.urlretrieve(
        url=url,
        filename=output_path
    )
    print('downloaded!')
    return


@click.command()
@click.option(
    '-m', '--method', default='LSTMCNN',
    help='''
        deep learning method. It can be any below.
        AlexNet | BiRNN | RNN | Seq2Seq | 
        CNN | ConvMixer64 | DSConv | LSTMCNN |
        MobileNet | ResNet18 | ResNet50 | SEResNet |
    '''
)
@click.option('-sm', '--smile_fpn', default='data/example/5757.txt', help='input file of a SM')
@click.option('-mir', '--fasta_fpn', default='data/example/MIMAT0000066.fasta', help='input fasta file of a miRNA')
@click.option('-mf', '--model_fp', default='model/lstmcnn', help='model path')
@click.option('-o', '--output_path', default='./out.deepsmirud', help='output deepsmirud predictions')
def main(
        method,
        smile_fpn,
        fasta_fpn,
        model_fp,
        output_path,
):
    deepsmirud_p = predict(
        smile_fpn=smile_fpn,
        fasta_fpn=fasta_fpn,
        method=method,
        model_fp=model_fp,
        sv_fpn=output_path,
    )
    s = [
        'AlexNet',
        'BiRNN',
        'RNN',
        'Seq2Seq',
    ]
    if method in s:
        deepsmirud_p.m1()
    else:
        deepsmirud_p.m2()


if __name__ == '__main__':
    main()