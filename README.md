## Coding Challenge-3: Natural Language Queries Against a Structural Database
### Kristy Hollingshead submission

This repo is forked from Weave.bio's coding challenge repo: https://github.com/weavebio/coding-challenge-3, which in turn was forked from Onuralp Soylemez's (@cx0) repo: https://github.com/cx0/chatGPT-for-genetics

This repo takes a natural language instruction or a question, and returns an appropriate response using using Open Targets API endpoints [Open Targets Platform GraphQL](https://platform-docs.opentargets.org/data-access/graphql-api).

### Types of Queries:
**1. Single-step queries**
e.g.: "What are the targets of Vorinostat?", "Find drugs that are used for treating ulcerative colitis.", etc.

**2. Two-step queries**
e.g.: "Which diseases are associated with the genes targeted by Fasudil?", "Show all the diseases that have at least 5 pathways associated with Alzheimer's.", etc.

### To run it:
- You will need an OpenAI account for OpenAI API access; export your API key into the environment variable OPENAI_API_KEY.
- This repo provides a CLI functionality; run `python3 ask_opentargets.py`.
- You will be asked to enter a natural language instruction or question, related to the Open Targets platform.
- The response should list the queried entities, with no extra paragraphs or text.
