from tree_sitter import Language, Parser


class CodeExtractor:
    def __init__(self, library_path='build/c_parse.so', language_name='c'):
        # 构建语言解析库
        Language.build_library(
            library_path,
            ['tree-sitter-c']
        )
        self.language = Language(library_path, language_name)
        self.parser = Parser()
        self.parser.set_language(self.language)

    def extract_code_from_text(self, text):
        """从提供的文本中提取所有 C 代码表达式和函数定义"""
        tree = self.parser.parse(bytes(text, "utf8"))
        root_node = tree.root_node
        code_blocks = []

        def extract_code(node):
            """递归地从每个节点提取代码"""
            if node.type in ['expression_statement', 'function_definition']:
                start = node.start_byte
                end = node.end_byte
                code_blocks.append(text[start:end].strip())
            for child in node.children:
                extract_code(child)

        extract_code(root_node)
        return code_blocks


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

    extracted_code = extractor.extract_code_from_text(mixed_text)
    print(extracted_code)


