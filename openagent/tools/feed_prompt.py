FEED_PROMPT = """
Here are the raw activities:

{activities_data}

- Before answering, please first summarize how many actions the above activities have been carried out.
- Display the key information in each operation, such as time, author, specific content, etc., and display this information in a markdown list format.
- Finally, give a specific answer to the question.
"""
