LLM_PROMPTS = {
    "tool_call_prompt": lambda message: f"""
        There is a function that can be called to get more information, and it takes a string as input. The function returns a list of sentences that are relevant to the input string.
        The data saved in database is from transcripts of conversations with users. Keep this in mind while generating the queries.
        The function can be called 2 times. From the user's message, return 2 queries that you would like to send to the function to get most relevant context. Try to make the queries such that you get as much relevant context as possible.
        Output should strictly be an array of 2 strings, each string being a query.

        Example: User Message: "How does the user feel about our product?"
        Queries:
        ["User experience and testimonials about the product", "User feedback on product features"]

        Example: User Message: "What are the common issues faced by users?"
        Queries:
        ["Common problems reported by users", "User complaints and suggestions"]

        Example: User Message: {message}
        Queries:
        """,
    "enhancement_prompt": lambda context, message: f"""
        You are a helpful assistant. Use the following information to answer the user's question. You can respond in a conversational manner, but do not include any unnecessary information.
        Context is a subset of transcript of conversations between two people.
        Please answer the question based on the context provided. You can say "Sorry, I don't know" if the context does not provide enough information, but try your best to answer even if the context is not complete.
        ######
        Context: {context}
        ######

        User's Question: {message}
        """
}