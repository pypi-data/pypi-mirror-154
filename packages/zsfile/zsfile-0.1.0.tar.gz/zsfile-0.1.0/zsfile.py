
import os

import click
import zstandard

default_ext_name = ".zst"

def get_output_from_input(input, decompress_flag):
    if decompress_flag:
        return os.path.splitext(input)[0]
    else:
        return input + default_ext_name

def do_decompress(input_path, output_path):
    dctx = zstandard.ZstdDecompressor()
    with open(input_path, 'rb') as ifh, open(output_path, 'wb') as ofh:
        dctx.copy_stream(ifh, ofh)

def do_compress(input_path, output_path):
    dctx = zstandard.ZstdCompressor()
    with open(input_path, 'rb') as ifh, open(output_path, 'wb') as ofh:
        dctx.copy_stream(ifh, ofh)


@click.command()
@click.option("-d", "--decompress", is_flag=True, help="force decompression. default to false.")
@click.option("-o", "--output", help="Output filename.")
@click.argument("input", nargs=1, required=True)
def main(decompress, input, output):
    """Zstandard compress and decompress tool.
    """
    if not output:
        output = get_output_from_input(input, decompress)
    if decompress:
        print("decompressing file {input} to {output}...".format(input=input, output=output))
        do_decompress(input, output)
    else:
        if os.path.splitext(input)[1].lower() == default_ext_name:
            print("input file {input} already has .zst suffix.".format(input=input))
            os.sys.exit(1)
        else:
            print("compressing file {input} to {output}...".format(input=input, output=output))
            do_compress(input, output)
