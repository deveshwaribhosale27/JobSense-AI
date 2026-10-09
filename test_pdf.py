from utils.pdf_reader import extract_text_from_pdf

text = extract_text_from_pdf("resume.pdf")

print("----- RESUME TEXT -----")
print(text)
print("-----------------------")