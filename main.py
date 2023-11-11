from tkinter import *
from tkinter import filedialog
import subprocess
import os
import tempfile

class SimpleCompiler:
    def __init__(self, master):
        self.master = master
        master.title("Simple Compiler")

        self.file_path = ''

        self.editor = Text(master)
        self.editor.pack()

        self.code_output = Text(master)
        self.code_output.pack()

        menu_bar = Menu(master)
        master.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Open', command=self.open_file)
        file_menu.add_command(label='Save', command=self.save)
        file_menu.add_command(label='Save As', command=self.save_as)
        file_menu.add_command(label='Exit', command=exit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        run_bar = Menu(menu_bar, tearoff=0)
        run_bar.add_command(label='Run', command=self.run)
        menu_bar.add_cascade(label="Run", menu=run_bar)

        # Bind Ctrl+S to the save method
        master.bind('<Control-s>', lambda event: self.save())

    def set_file_path(self, path):
        self.file_path = path

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[('C Files', '*.c')])
        if path:
            with open(path, 'r') as file:
                code = file.read()
                self.editor.delete('1.0', END)
                self.editor.insert('1.0', code)
                self.set_file_path(path)

    def save(self):
        if self.file_path:
            with open(self.file_path, 'w') as file:
                code = self.editor.get('1.0', END)
                file.write(code)
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename(filetypes=[('C Files', '*.c')])
        if path:
            with open(path, 'w') as file:
                code = self.editor.get('1.0', END)
                file.write(code)
                self.set_file_path(path)

    def run(self):
        # Save the file before running
        self.save()

        if not self.file_path:
            return  # If no file has been selected or saved, return without running

        # Compile and run the C code
        self.compile_and_run()

    def compile_and_run(self):
        try:
            # Compile the C code using gcc
            executable_path = os.path.splitext(self.file_path)[0]
            result = subprocess.run(['gcc', self.file_path, '-o', executable_path], capture_output=True, text=True, check=False)

            if result.returncode == 0:
                # Run the compiled executable
                process = subprocess.run([executable_path], capture_output=True, text=True)
                output, error = process.stdout, process.stderr
                self.code_output.delete('1.0', END)
                self.code_output.insert('1.0', output)
                self.code_output.insert('2.0', error)
            else:
                # Print the compilation error to the console for debugging
                self.code_output.delete('1.0', END)
                self.code_output.insert('1.0', f'Error during compilation:\n{result.stderr}')
                print(f'Error during compilation:\n{result.stderr}')

        except Exception as e:
            # Print any other error to the console for debugging
            self.code_output.delete('1.0', END)
            self.code_output.insert('1.0', f'Error: {str(e)}')
            print(f'Error: {str(e)}')

if __name__ == "__main__":
    root = Tk()
    app = SimpleCompiler(root)
    root.mainloop()
