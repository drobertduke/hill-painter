from argparse import ArgumentParser

from painter.painter import invoke


def main():
    parser = ArgumentParser(description="Hill Painter")
    parser.add_argument(
        "--image-path", type=str, default=None, help="Path to the source image")
    parser.add_argument(
        "--iterations", "-i", type=int, default=50000, help="Iterations to run")
    args = parser.parse_args()
    invoke(args)

if __name__ == "__main__":
    main()
