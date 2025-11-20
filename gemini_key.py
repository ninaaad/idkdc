from google import genai

# Replace "YOUR_API_KEY" with your actual Gemini API key
MY_API_KEY = "YOUR_API_KEY"

# Pass the API key directly to the client
client = genai.Client(api_key=MY_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents="Explain how AI works in a few words"
)

print(response.text)
