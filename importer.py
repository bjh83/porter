import vim

# TODO(brendan): I also need a function to load the table into memory and a way
# to set the file path to the table.
import_table = {}

def attempt_to_add_import(name_to_import):
    if name_to_import in import_table:
        imports = import_table[name_to_import]
        if len(imports) == 1:
            vim.current.buffer = add_import(materialize(imports[0]), vim.current.buffer)
        else:
            user_import = get_import_from_user(imports)
            vim.current.buffer = add_import(materialize(user_import), vim.current.buffer)
        return "success"
    else:
        return "could not find import"

# TODO(brendan): Implement this.
def get_import_from_user(choices):
    return
    # TODO(brendan): Use inputlist in vim to create a dialog.

def materialize(import_path):
    return "import " + import_path

class Importable():
    program_lines = []
    import_lines = []
    import_start = 0

    def __init__(self, program_lines, import_lines, import_start):
        self.program_lines = program_lines
        self.import_lines = import_lines
        self.import_start = import_start

    def insert_import(self, full_import):
        self.import_lines.append(full_import)

    def generate_buffer(self):
        insertion_place = self.import_start
        program_lines = copy(self.program_lines)
        self.import_lines.sort()
        for line in self.import_lines:
            program_lines.insert(insertion_place, line)
            insertion_place += 1
        return program_lines

def add_import(full_import, lines):
    importable = create_importable(lines)
    importable.insert_import(full_import)
    return importable.generate_buffer()

# TODO(brendan): Figure out what to do with non-imports in the import section.
def create_importable(lines):
    program_lines = []
    import_lines = []
    import_start = 0
    in_import_section = False
    done = False
    for line in lines:
        if done:
            # Just move to the buffer for regular code.
            program_lines.append(line)
            continue
        if in_import_section and is_import(line):
            # In import section, add import to import buffer.
            import_lines.append(line)
        elif not in_import_section and is_import(line):
            # Just entered the import section.
            in_import_section = True
            import_start = len(program_lines)
            import_lines.append(line)
        elif in_import_section and not is_import(line):
            # Just left the import section.
            done = True
            program_lines.append(line)
        else:
            # Have not yet entered the import section.
            program_lines.append(line)
    return Importable(program_lines, import_lines, import_start)

# TODO(brendan): Implement this. Shouldn't be too hard...
def is_import(raw_line):
    return
