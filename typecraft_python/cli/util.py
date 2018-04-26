import click
import six
import codecs


def write_to_stdout_or_file(
    content_to_write,
    path_or_file,
    encoding="utf-8"
):
    if not path_or_file or path_or_file == '-':
        click.echo(content_to_write)
    elif hasattr(path_or_file, 'write'):
        if isinstance(content_to_write, str):
            path_or_file.write(content_to_write)
        else:
            path_or_file.write(content_to_write.decode("utf-8"))
    elif isinstance(path_or_file, six.string_types):
        # Try to open file given by path
        with codecs.open(path_or_file, 'w+', encoding=encoding) as _file:
            if isinstance(content_to_write, str):
                _file.write(content_to_write)
            else:
                _file.write(content_to_write.decode("utf-8"))
    else:
        raise ValueError("Argument `path_or_file` is not a path or a file.")
