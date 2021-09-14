# open dataset and write ans files for convenience
import string

class OP():
    def __init__(self, f):
        self.file = f
        self.ans = '_ans.'.join(f.split('.'))

    def i(self):
        self.input = open(self.file)
        return self.input
    
    def o(self, out):
        self.input.close()
        self.output = open(self.ans, 'w')
        self.output.write(out + ' ')
        self.output.close()
