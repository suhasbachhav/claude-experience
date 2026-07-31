import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=50,
    messages=[
        {"role": "user", "content": "Say hello in one word."}
    ]
)

print(response.content[0].text)  # Should print: Hello
