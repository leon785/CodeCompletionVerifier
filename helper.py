def list_to_str(lst):
    return '\n'.join(lst)


if __name__ == '__main__':
    a = ['int main() {\n   printf("Hello World\\n");\n   return 0;\n}',
         'printf("Hello World\\n");',
         'a statement.\n\n6. Curly braces `{}'
    ]
    print(list_to_str(a))

