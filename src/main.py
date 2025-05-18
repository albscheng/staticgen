from textnode import TextType, TextNode


def main():
    # make a dummy TextNode
    dummy = TextNode("This is some text", TextType.LINK, "https://www.google.com")
    print(dummy)

if __name__ == "__main__":
    main()

