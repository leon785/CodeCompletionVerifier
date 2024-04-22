import subprocess
import os


def get_status(answer):
    lst = answer.split('\n')
    for i in lst:
        sent = i.lower()
        if 'final answer:' in sent:
            return i
        elif 'action:' in sent:
            if 'clang' in sent or 'analyze' in sent:
                return 'clang'
            if 'tree-sitter' in sent or 'extract' in sent:
                return 'tree-sitter'
    return 'invalid'


def list_to_str(lst):
    return '\n'.join(lst)


def str_to_file(code, path):
    with open(path, 'w') as f:
        f.write(code)
        f.close()


# CMD ["clang-tidy-10", "./data/extracted_snippet.c", "--", "-I/usr/lib/llvm-10/include"]
def analyze_syntax(path="./data/extracted_snippet.c"):
    command = f"clang-tidy-10 {path} -- -I/usr/lib/llvm-10/include"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result.stderr if result.stderr else result.stdout


if __name__ == '__main__':
    a = ['int main() {\n   printf("Hello World\\n");\n   return 0;\n}',
         'printf("Hello World\\n");',
         'a statement.\n\n6. Curly braces `{}'
    ]
    print(list_to_str(a))

