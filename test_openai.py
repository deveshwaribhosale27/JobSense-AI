from app.services.openai_client import ask_ai


result = ask_ai("Say hello to JobSense AI in one short sentence.")

print("AI RESPONSE:")
print(result)