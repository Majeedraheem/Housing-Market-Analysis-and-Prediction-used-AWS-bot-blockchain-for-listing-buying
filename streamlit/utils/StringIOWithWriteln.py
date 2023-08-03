from io import StringIO

class StringIOWithWriteln(StringIO):
    def writeln(self, arg=None):
        if arg:
            self.write(arg)
        self.write('\n')