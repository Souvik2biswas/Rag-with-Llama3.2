from app import upload_pdf
import os

with open("dummy.pdf", "w") as f:
    f.write("test")

# Simulate Gradio passing a string path
print("String path test:")
print(upload_pdf("dummy.pdf"))

class MockGradioFile:
    def __init__(self, name):
        self.name = name
        self.orig_name = "mock.pdf"

# Simulate Gradio passing an object
print("\nObject test:")
print(upload_pdf(MockGradioFile("dummy.pdf")))
