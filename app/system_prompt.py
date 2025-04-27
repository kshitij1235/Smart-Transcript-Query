
def system_prompt(query:str, results:str):
    return f"""{query}, you do have to behave like a chat bot that answers 
    questions based on the youtube videos take this transcribes : {results}"""