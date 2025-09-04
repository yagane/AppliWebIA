from mistralai import Mistral

api_key = "3NBWSQyhw7HQTqOR4lQXUYBknAVkguH2"
model = "mistral-tiny"

client = Mistral(api_key=api_key)


def query(message):
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": message,
            },
        ]
    )
    return chat_response.choices[0].message.content



