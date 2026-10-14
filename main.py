def main():
    name = input("What is your name? ").strip()

    if not name:
        name = "student"

    print(f"Hello, {name}! Welcome to DevOps exam practice.")


if __name__ == "__main__":
    main()