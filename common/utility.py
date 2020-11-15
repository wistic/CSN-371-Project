import py


def pretty_print(key, value):
    tw = py.io.TerminalWriter()
    tw.write(str(key)+":", yellow=True, bold=True)
    tw.write(str(value)+'\n', bold=True)
