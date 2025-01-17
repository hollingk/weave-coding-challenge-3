import os
import re
import json
import requests
import openai
from datetime import datetime
from utils import extract_values

def inform_user(msg:str, quit:bool) -> None:
    print(msg)
    if quit:
        exit(0)

def chatbot_graphql(user_input:str) -> str:

    message_list = [{"role": "system", "content": "You are a helpful, low-level GraphQL programming assistant."},
            {"role": "user", "content": "Help me translate the following natural language sentences into GraphQL queries."},
            {"role": "assistant", "content": "Sure, I'd be happy to!"}]
    with open("chat-assistant-graphql.jsonl", 'r') as fp:
        for chatline in fp:
            message_list.append(json.loads(chatline.strip()))
    message_list.append({"role": "user", "content": user_input})

    # or model="gpt-3.5-turbo-instruct"
    response_msg = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=message_list,
        temperature=0,
    )

    query_string=''
    try:
        query_chatbuilt = response_msg["choices"][0].message.content
    except:
        inform_user("ChatBot failed to return a response. Exiting.", quit=True)
    else:
        if '{' not in query_chatbuilt:
            inform_user(query_chatbuilt, quit=True)
        query_string = query_chatbuilt.strip()
    return query_string

def prompt_graphql(filename:str, user_input:str) -> str:

    # read graphQL schema example for prompt
    # e.g., graphql_schema.txt
    with open(filename, "r") as f:
        prompt_template = f.read()

    # Prime the target query for completion
    prime_prompt = "query treatment_drugs {\n  search(queryString:"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_template + "### " + user_input + "\n" + prime_prompt,
        temperature=0,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###"],
    )

    query_string=''
    try:
        response_text = response["choices"][0].text
    except:
        inform_user("Prompted chat failed to return a response. Exiting.", quit=True)
    else:
        query_string = prime_prompt + response_text
    return query_string

def output_query_file(query_string:str) -> None:
    # filename with current date and time
    query_file = "query_" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + ".txt"

    # write query to file with current date and time
    with open(query_file, "w") as f:
        f.write(f"# User input: {user_input}\n")
        f.write(query_string)
        inform_user(f"\nCustom graphQL query was written to file: {query_file}", quit=False)

def query_opentargets(query_string:str) -> dict:
    # Set base URL of GraphQL API endpoint
    base_url = "https://api.platform.opentargets.org/api/v4/graphql"

    # Perform POST request and check status code of response
    # This handles the cases where the Open Targets API is down or our query is invalid
    print("\n\nQuerying Open Targets genetics database...\n\n")
    try:
        response = requests.post(base_url, json={"query": query_string})
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        # inform_user(err, quit=False)
        inform_user("Open Targets query failed; try a different question.", quit=True)

    # Transform API response from JSON into Python dictionary and return
    api_response = json.loads(response.text)
    try:
        hits_list = api_response["data"]["search"]["hits"]
    except IndexError:
        inform_user("None found.", quit=True)
    else:
        if not hits_list:
            inform_user("None found.", quit=True)
        return hits_list[0]

def print_hits(hits_list:dict) -> None:
    # try to be clever about "guessing" correct output
    returned_rows = extract_values(hits_list, "rows")
    if not returned_rows:
        extracted_name_things = extract_values(hits_list, "id")
    else:
        extracted_name_things = extract_values(returned_rows, "name", fuzzy_match=True)
        if not extracted_name_things:
            extracted_name_things = extract_values(returned_rows, "id")
    if not extracted_name_things:
        print("None found, or incorrect format returned.")
        return
    for i, j in enumerate(list(dict.fromkeys(extracted_name_things))):
        # list(dict.fromkeys(<list>)) gets unique set while preserving order
        print(f"{i+1}. {j}")


if __name__ == "__main__":

    # read Open AI API key from environment variable
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        inform_user("Must populate environment variable OPENAI_API_KEY with secret key, e.g.:\
                    \nexport OPENAI_API_KEY=<your-secret-key>", quit=True)

    # Prompt user for input to query.
    # user_input = "Find the top 2 diseases associated with BRCA1"
    user_input = input("Hello, and welcome to Ask Open Targets. How can I help you today?\
                    \nE.g., ask me to:\
                    \nFind the top 2 diseases associated with BRCA1.\nor\
                    \nWhat are the targets of Trastuzumab?\nor\
                    \nFind drugs that are used for treating osteoporosis.\n_\n")

    # Uncomment to use file-based prompts to request GraphQL query from OpenAI
    # -- maybe less expensive but may ultimately require more API calls
    # prompt_filename="graphql_schema_treatments.txt"
    # query_string = prompt_graphql(prompt_filename, user_input)

    # Build a chatbot to request GraphQL query from OpenAI
    # -- maybe more expensive but potentially more flexible
    query_string = chatbot_graphql(user_input)

    # Uncomment to output query to file for later analysis
    # output_query_file(query_string)

    # Query Open Targets
    hits_list = query_opentargets(query_string)

    # try to be super clever about extracting print-out-able results
    print_hits(hits_list)
