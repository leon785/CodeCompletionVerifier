from openai import OpenAI


class Chatbot:
    def __init__(self):
        # self.model = "gpt-3.5-turbo-0125"
        self.model = "gpt-4"
        self.api_key = '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'
        self.client = OpenAI(api_key=self.api_key)
        self.history = []
        # self.history = [{"role": 'assistant', "content": 'There is a function called num_adder, returning the addition of two parameters a and b.'}]

    def send_message(self, message):
        # get previous context
        msg = self.history.copy()
        msg.append({"role": "user", "content": message})

        # communicate
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=msg,
        )
        assistant_answer = completion.choices[0].message.content

        # session history update
        self.history_update('user', message)
        self.history_update('assistant', assistant_answer)
        return assistant_answer

    def history_update(self, role, content):
        self.history.append({"role": role, "content": content})


class ReActBot(Chatbot):
    def __init__(self):
        super().__init__()
        self.stop_word = ["Observation", "Task Completed"]
        self.react_instruction()
        self.react_msg = ''

    def send_message(self, message):
        # get previous context
        msg = self.history.copy()
        msg.append({"role": "assistant", "content": message})

        # communicate
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=msg,
            stop=self.stop_word
        )
        assistant_answer = completion.choices[0].message.content

        # session history update
        self.react_msg = self.react_msg + message + assistant_answer
        return completion

    def react_instruction(self):
        self.history_update(
            'system',
            # "Answer the following questions as best as you can."
            # "You have access to the following tools:"
            # "[tree-sitter code extractor, infer syntax verifier]"
            # ""
            # "Use the following format:"
            # "Question: the input question you must answer."
            # "Thought: you should always think about what to do."
            # "Action: the action to take, should be one of the tools."
            # "Action Input: the input to the action"
            # "Observation: the result of the action"
            # ""
            # "this Thought/Action/Action Input/Observation can repeat N times)"
            # ""
            # "Thought: I now know the final answer"
            # "Final Answer: the final answer to the original question"
            # "Task Completed."
            # ""
            # "Begin!"

            "You are the brain of a Code Completion Verifier, your decisions will affect the behavior of this program."
            "The Code Completion Verifier will verify the code syntax. If the syntax is correct, it outputs this code "
            "snippets, but if the syntax is incorrect, it returns the error message it received. "
            "Code Completion Verifier may also receive mixed text, in which case it will need to extract the code "
            "before performing syntax checking. You, as the brain of Code Completion Verifier, will need to help "
            "the application accomplish the above tasks and make the right execution decisions."
            ""

            "You have access to the following tools:"
            "[tree-sitter code extractor, infer syntax verifier]"
            ""
            "You will have the Question at the beginning of the process, in the following format:"
            "\""
            "Question: the input question you must answer."
            "\""
            "The Question will be \"Is the following text a mixed text or a syntax validation report from a verifier?\""
            "If it is a mixed text, you should decide to use tree-sitter code extractor."
            "If it is a syntax validation report, you should decide to use infer syntax verifier."
            ""
            "You will think about the question step by step. Your answer will be in the following format:"
            "\""
            "Thought: you should always think about what to do."
            "Action: the action to take, should be one of the tools."
            "Action Input: the input to the action"
            "Observation: the result of the action"
            "\""
            ""
            "this Thought/Action/Action Input/Observation can repeat N times)"
            ""
            
            "You must decide whether it is an extracted code or if the syntax is correct "
            "as the brain of Code Completion Verifier."
            "If Question is a raw mixed text, then you should extract the code. "
            "Question can also be the validation report of the verifier, then you should understand the meaning of it."
            "If the report says the syntax is correct, then output the code snippet. "
            "If not, then summarize the report and output."
            ""
            # "When you have the Observation of the validation report, your next answer set will be the final one. "
            # "Use following format:"
            # "\""
            # "Thought: I now know the final answer"
            # "Final Answer: code snippet (when syntax is correct), or report summary (when syntax is incorrect)."
            # "Task Completed."
            "\""
            "Begin!"
        )


if __name__ == "__main__":
    # print('=' * 100)
    chatbot = Chatbot()

    prompt = "Generate a piece of code in the language C with the explanation. "
    mixed_text = chatbot.send_message(prompt)
    print(mixed_text)
    print('=' * 100)
    #
    # prompt = "Try to explain this piece of code line by line."
    # answer = chatbot.send_message(prompt)
    # print(answer)
    # print('=' * 100)

    reactor = ReActBot()
    prompt = ("Question: Is the following text an extracted code?"
              + "\"" + mixed_text + "\"\n"
              + "\nThought: "
              )
    answer = reactor.send_message(prompt)
    print(answer.choices[0].message.content)
    print()
    print(reactor.history)
    print(reactor.react_msg)
    print("=" * 100)

    prompt = (reactor.react_msg
              + "\nObservation: " +
              ""
              )



