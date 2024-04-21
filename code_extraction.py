from tree_sitter import Language, Parser
from graphviz import Digraph
import helper


class CodeExtractor:
    def __init__(self):
        Language.build_library(
            'build/c_parse.so',
            ['tree-sitter-c']
        )
        self.language = Language('build/c_parse.so', 'c')
        self.parser = Parser()
        self.parser.set_language(self.language)

    def extract_code(self, text):
        tree = self.parser.parse(bytes(text, "utf8"))
        # print('>'*100)
        # self.print_tree(tree.root_node, bytes(text, "utf8"))
        # print('<'*100)
        root_node = tree.root_node
        code_blocks = []

        def inner_loop(node, level=0):
            capture_types = [
                "preproc_include",
                "function_definition",
                "expression_statement",
                "compound_statement",
            ]
            if node.type in capture_types and level <= 1:
                start = node.start_byte
                end = node.end_byte
                code_blocks.append(text[start:end].strip())
            for child in node.children:
                inner_loop(child, level+1)

        inner_loop(root_node)
        return code_blocks

    def print_tree(self, node, source_code, level=0):
        indent = '  ' * level
        node_text = source_code[node.start_byte:node.end_byte].decode('utf8')
        if level == 1:
            print(f"{indent}TYPE={node.type}: TEXT={node_text}")
        for child in node.children:
            self.print_tree(child, source_code, level+1)


if __name__ == '__main__':
    extractor = CodeExtractor()
    mixed_text = """\
    "Sure, Here's an example of a basic \\"Hello World!\\" program written in the C programming language. This program, when run, will print out the text \\"Hello, World!\\" to the console.
    
    Here's the code:
    
    ```c
    #include <stdio.h>
    
    int main() {
       // printf() displays the string inside the quotation
       printf(\\"Hello, World!\\");
       return 0;
    }
    And here's a step-by-step explanation of the code:
    
    #include <stdio.h>: This is a preprocessor command that tells the compiler to include the contents of the stdio.h (standard input-output header file) in the program. The stdio.h file contains functions such as scanf() and printf() to take input and display output respectively.
    int main(): The main function is the point where our program starts execution. The int at the beginning of this line signifies that the function must return an integer value. When the program completes successfully, the function will return 0 as specified at the end of the function body.
    printf(\\"Hello, World!\\");: The printf function is used to print the specified string on the screen. In this case, the string “Hello, World!” is printed.
    return 0;: This statement signifies that the main function will return by \"0\". Any non-zero value meaning the program has ended unsuccessfully. As a good practice, programmers generally use the return 0 statement in the main function.
    Remember to compile this source code with a C compiler before running the program."
    """

    extracted_code = extractor.extract_code(mixed_text)
    extracted_code = helper.list_to_str(extracted_code)
    helper.str_to_file(extracted_code, "./data/extracted_snippet.c")
    print(extracted_code)


