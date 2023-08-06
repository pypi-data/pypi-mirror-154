import tempfile

import click
import relation_graph_impl as impl

def run_relation_graph(input_path: str, output_path: str = None) -> None:
    """
    Runs relation-graph

    :param input_path:
    :param output_path:
    :return:
    """
    if output_path is None:
        tf = tempfile.NamedTemporaryFile(mode='r')
        impl.run_relation_graph(input_path, tf.name)
        for line in tf.readlines():
            print(line, end='')
    else:
        impl.run_relation_graph(input_path, output_path)

@click.command()
@click.argument('input')
@click.option('-o', '--output',
              required=False,
              help="Path to entailed edges file")
def main(input, output):
    """
    runs relation graph
    """
    run_relation_graph(input, output)


if __name__ == '__main__':
    main()
