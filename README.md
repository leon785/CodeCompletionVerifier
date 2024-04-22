# Code Completion Verifier

## 1. Overview
The Code Completion Verifier is a tool that verifies the C code syntax in a mixed text.
Openai API are used for the decision-making of the entire working process based on a specific prompt engineering approach.
Several tools are integrated for mixed text generation, code extraction and code analysis. 



## 2. Project Structure
### Decision Maker
Openai API are used to act as the "brain" of the application, It is instructed to perform [ReAct](https://arxiv.org/abs/2210.03629) thinking and output in a standardized format. 
Unlike the linear flow of traditional programs, this tool demonstrates the possibility of automated circular validation.

### Mixed Text Generation
Application generate a piece of text mixed text and code.

### Code Extraction
When the "brain" receive the mixed text, it will decide if it is a mixed text and need to extract the code.

### Code Analysis
After the "brain" determine that the code has been fully extracted, it will drive verification tools to analyze C syntax.

### Final Output
The final output based on the analysis result. If no error exists then output will be the extracted code, otherwise, output the error message.



## 3. Getting Started
### Prerequisites
Docker must be installed on your machine. Go to [docker documentation](https://docs.docker.com/get-docker/) for installation.

### Build a Docker Image
Navigate to the project root directory and execute the following command:
```bash
docker build -t code-completion-verifier .
```

### Run the Container
Once the docker image is built successfully, you can execute the following command to run this container.
```bash
docker run --rm -v "${PWD}:/project" code-completion-verifier
```



## 4. Integrated Tools
[tree-sitter-c](https://github.com/tree-sitter/tree-sitter-c) implemented as a submodule.<br/>
[llvm clang](https://clang.llvm.org/) is installed into the docker environment for C code syntax analysis.<br/>

