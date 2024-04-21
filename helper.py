import subprocess
import os

def list_to_str(lst):
    return '\n'.join(lst)


def str_to_file(code, path):
    with open(path, 'w') as f:
        f.write(code)
        f.close()


def analyze_syntax():
    cur_dir = os.getcwd()
    command = f'docker run --rm -v "{cur_dir}:/project" llvm-clang'
    # command = 'docker run --rm -v \"${PWD}:/project\" llvm-clang'
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result.stderr if result.stderr else result.stdout


if __name__ == '__main__':
    a = ['int main() {\n   printf("Hello World\\n");\n   return 0;\n}',
         'printf("Hello World\\n");',
         'a statement.\n\n6. Curly braces `{}'
    ]
    print(list_to_str(a))

