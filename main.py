from chat import Chatbot, ReActBot
from code_extraction import CodeExtractor
import helper


def main():
    # initialization
    chatbot = Chatbot()
    reactor = ReActBot()
    extractor = CodeExtractor()

    # Mixed text generation
#     prompt = ("Generate a piece of code in the language C with a brief explanation. "
#               "The explanation cannot have code snippet.")
    prompt = ("Generate a piece of mixted text include a piece of code in the language C")
    mixed_text = chatbot.send_message(prompt)
    print("-- Mixed Text --")
    print(mixed_text)
    print('=' * 100)

    # React 1
    prompt = (
            reactor.react_msg
            + "Question: Is the following text an extracted code?"
            + "\"" + mixed_text + "\"\n"
            + "\nThought: "
    )
    answer = reactor.send_message(prompt)
    # print(reactor.react_msg)
    # print(answer.choices[0].message.content)
    print("-- React 1 --")
    print("Thought: " + answer.choices[0].message.content)
    print("=" * 100)

    # Code extraction
    extracted_code = extractor.extract_code_from_text(mixed_text)
    extracted_code = helper.list_to_str(extracted_code)
    print("-- Code Extraction --")
    print(extracted_code)
    print('=' * 100)

    # React 2
    prompt = (
            reactor.react_msg
            + "\nObservation: "
            + extracted_code
    )
    answer = reactor.send_message(prompt)
    print("-- React 2 --")
    print(answer.choices[0].message.content)
    print("=" * 100)
    print()


main()

