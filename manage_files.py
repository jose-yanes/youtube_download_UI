
def add_to_file(data):
    with open("./files/pending_urls.txt.", "a") as file:
        file.write(f"{data}")
def read_from_file(file):
    with open(f"./files/{file}", "r") as file:
        lines = file.readlines()
    return lines