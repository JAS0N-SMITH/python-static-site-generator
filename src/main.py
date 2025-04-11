from textnode import TextNode  # Import TextNode from the appropriate module

def main():
	obj = TextNode("This is some anchor text", "link", "https://www.boot.dev")
	print(obj.__repr__())

if __name__ == "__main__":
	main()