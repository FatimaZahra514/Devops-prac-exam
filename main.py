import os

def main():
    name = os.getenv("NAME", "student")
    print(f"Hello, {name}! Welcome to DevOps exam practice.")

if __name__ == "__main__":
    main()