from sanzan import *
import argparse


def main(args=None):
    parser = argparse.ArgumentParser(description="Encrypt or decrypt video files")

    ifile_group = parser.add_mutually_exclusive_group(required=True)
    ifile_group.add_argument("-e", "--encrypt", help="path of file to encrypt", type=str)
    ifile_group.add_argument("-d", "--decrypt", help="path of file to decrypt", type=str)

    parser.add_argument("-k", "--key", help="path of video keyfile", type=str)
    parser.add_argument("-ka", "--audiokey", help="path of audio keyfile", type=str)
    parser.add_argument("-o", "--output", help="path of output file", type=str)
    parser.add_argument("-pw", "--password", help="password to encrypt or decrypt", type=str)
    parser.add_argument("-c", "--chunksize", help="audio chunksize", type=int)

    parser.add_argument("-p", "--preview", action="store_true", help="show real time preview of output")
    parser.add_argument("-s", "--silent", action="store_true", help="hide progress bar")
    parser.add_argument("-ex", "--export", action="store_true", help="export keyfiles")

    args = parser.parse_args(args)

    if not (args.output or args.preview):
        parser.error("no action specified, add -o or -p")

    if args.encrypt:
        x = Encryptor(args.encrypt)
        x.gen_key(args.key, args.password)
        x.gen_audio_key(args.password, args.chunksize, args.export)

    if args.decrypt:
        if not (args.key or args.password):
            parser.error("keyfile or password not specified, add -k or -pw")

        x = Decryptor(args.decrypt)
        x.set_key(args.key, args.password)
        x.set_audio_key(args.audiokey, args.password, args.chunksize)

    if args.output:
        x.set_output(args.output)

    x.run(preview=args.preview, silent=args.silent)


if __name__ == "__main__":
    main()
