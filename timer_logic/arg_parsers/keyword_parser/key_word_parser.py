
# {'flag':'a_note=', 'value':None},

class UpdateKeywordParser:

    def __init__(self, args, kwarg_flags):
        self.kwarg_flags = kwarg_flags
        self.args = args
        self.arg_slices = list()

    # TODO: st= et= need to limit to two inputs
    def keyword_parser(self):
        start = None
        for index, arg in enumerate(self.args):
            if '=' in arg and start is None:
                start = index
            elif index + 1 == len(self.args):
                self.handle_end_slice(start, index, arg)
            elif '=' in arg and start is not None:
                self.arg_slices.append(self.args[start: index])
                start = index

    def handle_end_slice(self, start, index, arg):
        if "=" in arg:
            self.arg_slices.append(self.args[start: index])
            self.arg_slices.append(self.args[index:])
        else:
            self.arg_slices.append(self.args[start:])

    def iter_through_flags(self):
        for flags in self.kwarg_flags:
            flag = flags['flag']
            flags['value'] = self.process_slices(flag)

    def process_slices(self, flag):
        for index, array in enumerate(self.arg_slices):
            if flag in array[0]:
                value_array = self.arg_slices.pop(index)
                # Todo: a better way to handle del=note dynamically instead of hard coding it?
                if value_array[0] == 'del=note':
                    return 'Null'
                if len(value_array) > 1:
                    value = value_array[0].split('=')[1] + " " + " ".join(value_array[1:])
                    return value
                else:
                    value = value_array[0].split('=')[1]
                    return value

# ToDo: Need a keyword factory
