from chat import Chatbot, ReActBot, YesNoBot
from code_extraction import CodeExtractor
import helper


MAX_LOOP = 3
PATH_TO_SNIPPETS = "./data/extracted_snippet.c"


def main():
    # initialization
    chatbot, reactor = Chatbot(), ReActBot()
    extractor = CodeExtractor()
    payload_sofar = ''
    extracted_code = ''
    final_output = '-1'
    react_counter = 0

    # Mixed text generation
    prompt = "Generate a piece of mixed text include a piece of code in the language C."
    mixed_text = chatbot.send_message(prompt)
    print("-- Mixed Text --")
    print(mixed_text)
    print('=' * 100)

    # Think: initial question
    loop_counter = 0
    while True and loop_counter < MAX_LOOP:
        # React
        prompt = (
                payload_sofar
                + "Question: Act as the Code Completion Verifier, what should you do now?"
                + "\"" + mixed_text + "\"\n"
                + "\nThought: "
        )
        answer = reactor.send_message(prompt)
        status = helper.get_status(answer)
        react_counter += 1
        print(f"-- React {react_counter} --")
        print("Thought: " + answer)
        print("=" * 100)
        # go to extract code
        if status == "tree-sitter":
            break
        loop_counter += 1
    payload_sofar = reactor.react_msg

    # Think: if the code is extracted
    loop_counter = 0
    while True and loop_counter < MAX_LOOP:
        # Code extraction
        extracted_code = extractor.extract_code(mixed_text)
        extracted_code = helper.list_to_str(extracted_code)
        helper.str_to_file(extracted_code, PATH_TO_SNIPPETS)
        print("-- Code Extraction --")
        print("* * " * 10)
        print(extracted_code)
        print("* * " * 10 + '\n')

        # React
        prompt = (
                payload_sofar
                + "\nObservation: "
                + extracted_code + "\n"
                + "\nThought: "
        )
        answer = reactor.send_message(prompt)
        status = helper.get_status(answer)
        react_counter += 1
        print(f"-- React {react_counter} --")
        print("Thought: " + answer)
        print("=" * 100)
        if status == "clang":
            break
        loop_counter += 1
    payload_sofar = reactor.react_msg

    # Think: if the extracted code is valid
    loop_counter = 0
    while True and loop_counter < MAX_LOOP:
        # Analyze
        analyzer_result = helper.analyze_syntax()
        print("-- Analysis --")
        print(analyzer_result)

        # React
        prompt = (
                payload_sofar
                + "\nObservation: "
                + analyzer_result + "\n"
                + "\nThought: "
        )
        answer = reactor.send_message(prompt)
        status = helper.get_status(answer)
        react_counter += 1
        print(f"-- React {react_counter} --")
        print("Thought: " + answer)
        print("=" * 100)
        if status not in ["tree-sitter", "clang", "invalid"]:
            sentiment = YesNoBot()
            decision = sentiment.send_message(status)
            if decision == "positive":
                final_output = extracted_code
            else:
                final_output = status
            break
        loop_counter += 1
    payload_sofar = reactor.react_msg

    # Task Completed
    print('The final output of the Code Completion Verifier is: \n' + final_output)


main()

