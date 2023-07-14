import os
import re
import json
import requests
import openai
from datetime import datetime
from utils import extract_values

# read Open AI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    print("Must populate environment variable OPENAI_API_KEY with secret key, e.g.:\nexport OPENAI_API_KEY=<your-secret-key>")
    exit()

# Open Targets graphQL schema example
# read from file
with open("graphql_schema_search_diseases.txt", "r") as f:
    prompt_template = f.read()

# Prime the target query for completion
# -- as read from the schema file??
prime_prompt = "query top_n_associated_diseases {\n  search(queryString:"

# Custom input by the user
# user_input = "Find the top 2 diseases associated with BRCA1"
user_input = input("How can I help you today?\nE.g., ask me to:\nFind the top 2 diseases associated with BRCA1.\nor\nWhat are the targets of Adderall?\nor\nFind drugs that are used for treating arthritis.\n")

# response_msg = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo-0613",
#     messages=[
#         {"role": "system", "content": "You are a helpful, low-level GraphQL programming assistant."},
#         {"role": "user", "content": "Help me translate the following natural language sentences into GraphQL queries."},
#         {"role": "assistant", "content": "Sure, I'd be happy to!"},
#         {"role": "user", "content": "What are the top 5 diseases associated with gene APOE?"},
#         {"role": "assistant", "content": "query top_n_associated_diseases {search(queryString: \"APOE\", entityNames: \"target\") { \
#          hits { id, name, entity, object { \
#          ... on Target { associatedDiseases(page: {index: 0, size: 5}) { \
#          rows { score, disease {name} } } } } } } }"},
#         {"role": "user", "content": "What are the targets of vorinostat?"},
#         {"role": "assistant", "content": "query targeted_genes { search(queryString: \"vorinostat\", entityNames: \"drug\") { \
#          hits { id, name, entity, object { \
#          ... on Drug { linkedTargets { \
#          rows { id, approvedSymbol, approvedName } } } } } } }"},
#         {"role": "user", "content": "Find 3 drugs that are used for treating ulcerative colitis."},
#         {"role": "assistant", "content": "query treatment_drugs { search(queryString: \"ulcerative colitis\", entityNames: \"disease\") { \
#          hits { id, name, entity, object { \
#          ... on Disease { knownDrugs(page: {index: 0, size: 3}) { \
#          rows { approvedSymbol, approvedName } } } } } } }"},
#         {"role": "user", "content": user_input},
#     ],
#     temperature=0,
# )

# print(response_msg)
# query_chatbuilt = response_msg["choices"][0].message.content
# query_string = query_chatbuilt.strip()

# response = openai.Completion.create(
#     model="text-davinci-003",
#     prompt=prompt_template + "### " + user_input + "\n" + prime_prompt,
#     temperature=0,
#     max_tokens=250,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0,
#     stop=["###"],
# )

# response_text = response["choices"][0].text

# query_string = prime_prompt + response_text

# filename with current date and time
# query_file = "query_" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + ".txt"

# # write query to file with current date and time
# with open(query_file, "w") as f:
#     f.write(f"# User input: {user_input}\n")
#     f.write(query_string)
#     print(f"\nCustom graphQL query was written to file: {query_file}")

# Set base URL of GraphQL API endpoint
# base_url = "https://api.platform.opentargets.org/api/v4/graphql"


# print(f"with query_string:\n{query_string}\n...")

# Perform POST request and check status code of response
# This handles the cases where the Open Targets API is down or our query is invalid
# print("\n\nQuerying Open Targets genetics database...\n\n")
# try:
#     response = requests.post(base_url, json={"query": query_string})
#     response.raise_for_status()
# except requests.exceptions.HTTPError as err:
#     print(err)

# # Transform API response from JSON into Python dictionary and print in console
# api_response = json.loads(response.text)
# response_text = "{'data': {'search': {'hits': [{'id': 'ENSG00000012048', 'name': 'BRCA1', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.8340889978861029, 'disease': {'name': 'breast-ovarian cancer, familial, susceptibility to, 1'}}, {'score': 0.8247032876834987, 'disease': {'name': 'Hereditary breast and ovarian cancer syndrome'}}]}}}, {'id': 'ENSG00000267595', 'name': 'BRCA1P1', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.0022174791281082107, 'disease': {'name': 'ovarian serous carcinoma'}}]}}}, {'id': 'ENSG00000136492', 'name': 'BRIP1', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.8394513409791481, 'disease': {'name': 'Fanconi anemia complementation group J'}}, {'score': 0.7433266554411564, 'disease': {'name': 'hereditary breast carcinoma'}}]}}}, {'id': 'ENSG00000163930', 'name': 'BAP1', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.7913893713185206, 'disease': {'name': 'BAP1-related tumor predisposition syndrome'}}, {'score': 0.6578790966068293, 'disease': {'name': 'Pleural Mesothelioma'}}]}}}, {'id': 'ENSG00000138376', 'name': 'BARD1', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.6684557604847824, 'disease': {'name': 'hereditary breast carcinoma'}}, {'score': 0.6092661693716305, 'disease': {'name': 'breast carcinoma'}}]}}}, {'id': 'ENSG00000106009', 'name': 'BRAT1', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.780534242896629, 'disease': {'name': 'Lethal neonatal spasticity-epileptic encephalopathy syndrome'}}, {'score': 0.7504740104398419, 'disease': {'name': 'neurodevelopmental disorder with cerebellar atrophy and with or without seizures'}}]}}}, {'id': 'ENSG00000163322', 'name': 'ABRAXAS1', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.4027713359591208, 'disease': {'name': 'breast carcinoma'}}, {'score': 0.3695798546847018, 'disease': {'name': 'hereditary breast carcinoma'}}]}}}, {'id': 'ENSG00000158019', 'name': 'BABAM2', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.32766016195226877, 'disease': {'name': 'refractive error measurement'}}, {'score': 0.28880053963929403, 'disease': {'name': 'age at menopause'}}]}}}, {'id': 'ENSG00000089234', 'name': 'BRAP', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.43284275508748454, 'disease': {'name': 'platelet count'}}, {'score': 0.3695798546847018, 'disease': {'name': 'platelet crit'}}]}}}, {'id': 'ENSG00000185515', 'name': 'BRCC3', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.2822522100386782, 'disease': {'name': 'ovarian cancer'}}, {'score': 0.2808379956817396, 'disease': {'name': 'breast adenocarcinoma'}}]}}}, {'id': 'ENSG00000105393', 'name': 'BABAM1', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.2822522100386782, 'disease': {'name': 'ovarian cancer'}}, {'score': 0.2808379956817396, 'disease': {'name': 'breast adenocarcinoma'}}]}}}, {'id': 'ENSG00000198496', 'name': 'NBR2', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.06103897153571255, 'disease': {'name': 'cancer'}}, {'score': 0.05709224870377126, 'disease': {'name': 'neoplasm'}}]}}}, {'id': 'ENSG00000189167', 'name': 'ZAR1L', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.3671806654613736, 'disease': {'name': 'Hereditary breast and ovarian cancer syndrome'}}, {'score': 0.3634715209753296, 'disease': {'name': 'hereditary breast ovarian cancer syndrome'}}]}}}, {'id': 'ENSG00000171421', 'name': 'MRPL36', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.5368697208506422, 'disease': {'name': 'neurodegenerative disease'}}, {'score': 0.3109975550394092, 'disease': {'name': 'Alzheimer disease'}}]}}}, {'id': 'ENSG00000188986', 'name': 'NELFB', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.5922100627033303, 'disease': {'name': 'HIV infection'}}, {'score': 0.4831788037858693, 'disease': {'name': 'neurodegenerative disease'}}]}}}, {'id': 'ENSG00000188554', 'name': 'NBR1', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.30353794209448215, 'disease': {'name': 'neurodegenerative disease'}}, {'score': 0.20414840293222045, 'disease': {'name': 'aging'}}]}}}, {'id': 'ENSG00000139618', 'name': 'BRCA2', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.8746440062258756, 'disease': {'name': 'breast carcinoma'}}, {'score': 0.8452702725356971, 'disease': {'name': 'hereditary breast carcinoma'}}]}}}, {'id': 'ENSG00000051180', 'name': 'RAD51', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.5780157064519212, 'disease': {'name': 'familial congenital mirror movements'}}, {'score': 0.5545502110189217, 'disease': {'name': 'cancer'}}]}}}, {'id': 'ENSG00000256683', 'name': 'ZNF350', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.1863860202116849, 'disease': {'name': 'genetic disorder'}}, {'score': 0.07428555079162505, 'disease': {'name': 'kidney neoplasm'}}]}}}, {'id': 'ENSG00000087206', 'name': 'UIMC1', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.2822522100386782, 'disease': {'name': 'ovarian cancer'}}, {'score': 0.2808379956817396, 'disease': {'name': 'breast adenocarcinoma'}}]}}}, {'id': 'ENSG00000136147', 'name': 'PHF11', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.347758768635034, 'disease': {'name': 'platelet count'}}, {'score': 0.2446418178823833, 'disease': {'name': 'eosinophil count'}}]}}}, {'id': 'ENSG00000073598', 'name': 'FNDC8', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.19587205688839007, 'disease': {'name': 'neurodegenerative disease'}}, {'score': 0.18696609478058215, 'disease': {'name': 'genetic disorder'}}]}}}, {'id': 'ENSG00000108384', 'name': 'RAD51C', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.7616381896739217, 'disease': {'name': 'Hereditary breast and ovarian cancer syndrome'}}, {'score': 0.710214873734253, 'disease': {'name': 'Fanconi anemia'}}]}}}, {'id': 'ENSG00000185379', 'name': 'RAD51D', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.7548370676550281, 'disease': {'name': 'Hereditary breast and ovarian cancer syndrome'}}, {'score': 0.6572138094667395, 'disease': {'name': 'ovarian cancer'}}]}}}, {'id': 'ENSG00000113522', 'name': 'RAD50', 'entity': 'target', 'object': {'associatedDiseases': {'rows': [{'score': 0.7278843961464905, 'disease': {'name': 'Nijmegen breakage syndrome-like disorder'}}, {'score': 0.5918224970260421, 'disease': {'name': 'cancer'}}]}}}]}}}"
api_response = json.load(open('response.json'))
print(f"api_response: {api_response}")
try:
    hits_list = api_response["data"]["search"]["hits"][0]
except IndexError:
    print("None found.")
    exit()

print("hits_list:",hits_list)
query_string = "query top_associated_diseases {search(queryString: \"BRCA1\", entityNames: \"target\") {          hits { id, name, entity, object {          ... on Target { associatedDiseases(page: {index: 0, size: 2}) {          rows { score, disease {name} } } } } } } }"
returned_rows = extract_values(hits_list, "rows")
print(f"queried rows: {returned_rows}")
extractable_keys = []
for qr in returned_rows:
    if type(qr) is dict:
        for k in qr.keys():
            extractable_keys.append(k)
print(f"extractable keys: {list(set(extractable_keys))}")
for ek in list(set(extractable_keys)):
    print(f"extract: {ek}")
    results_list = extract_values(hits_list, ek)
    for i, j in enumerate(results_list):
        results_keys = list(j.keys())
        print(f"{i+1}. {j[results_keys[0]]}")
