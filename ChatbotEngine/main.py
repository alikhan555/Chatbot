from chat_pipline import Chat


def main():
    chat = Chat()
    response = chat.send_message("Hi my name is ali, what is my name?", "101")
    print(response["messages"][-1].content)


if __name__ == "__main__":
    main()
