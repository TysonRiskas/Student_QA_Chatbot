"""
Student Q&A Chatbot - CLI Prototype
A command-line chatbot that answers student questions using course materials and AI assistance.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from mistralai import Mistral
import PyPDF2
import docx
import json
from datetime import datetime

# Load environment variables
load_dotenv()

class ChatbotCorpus:
    """Manages the corpus of course materials (PDFs, DOCX, MP4)."""
    
    def __init__(self, corpus_dir="corpus"):
        self.corpus_dir = Path(corpus_dir)
        self.corpus_text = ""
        
    def load_corpus(self):
        """Load all documents from the corpus directory."""
        if not self.corpus_dir.exists():
            print(f"Creating corpus directory: {self.corpus_dir}")
            self.corpus_dir.mkdir(parents=True, exist_ok=True)
            print("Please add your course materials (PDF, DOCX, TXT, MP4) to the 'corpus' folder.")
            return
        
        corpus_parts = []
        
        # Load TXT files first (ensure text content not truncated later)
        for txt_file in self.corpus_dir.glob("*.txt"):
            print(f"Loading TXT: {txt_file.name}")
            corpus_parts.append(self._read_txt(txt_file))
        
        # Load PDFs
        for pdf_file in self.corpus_dir.glob("*.pdf"):
            print(f"Loading PDF: {pdf_file.name}")
            corpus_parts.append(self._read_pdf(pdf_file))
        
        # Load DOCX files
        for docx_file in self.corpus_dir.glob("*.docx"):
            print(f"Loading DOCX: {docx_file.name}")
            corpus_parts.append(self._read_docx(docx_file))
        
        # Load MP4 files (extract metadata/info)
        for mp4_file in self.corpus_dir.glob("*.mp4"):
            print(f"Loading MP4 metadata: {mp4_file.name}")
            corpus_parts.append(self._read_mp4_info(mp4_file))
        
        self.corpus_text = "\n\n".join(corpus_parts)
        
        if self.corpus_text.strip():
            print(f"\nCorpus loaded successfully! ({len(corpus_parts)} files)\n")
        else:
            print("\nNo corpus files found. Add PDF, DOCX, TXT, or MP4 files to the 'corpus' folder.\n")
    
    def _read_pdf(self, filepath):
        """Extract text from PDF file."""
        try:
            text_parts = []
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text_parts.append(page.extract_text())
            return f"[PDF: {filepath.name}]\n" + "\n".join(text_parts)
        except Exception as e:
            print(f"Error reading {filepath.name}: {e}")
            return ""
    
    def _read_docx(self, filepath):
        """Extract text from DOCX file."""
        try:
            doc = docx.Document(filepath)
            text = "\n".join([para.text for para in doc.paragraphs])
            return f"[DOCX: {filepath.name}]\n" + text
        except Exception as e:
            print(f"Error reading {filepath.name}: {e}")
            return ""
    
    def _read_txt(self, filepath):
        """Read plain text from TXT file."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            return f"[TXT: {filepath.name}]\n" + text
        except Exception as e:
            print(f"Error reading {filepath.name}: {e}")
            return ""
    
    def _read_mp4_info(self, filepath):
        """Extract basic info from MP4 file."""
        try:
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(str(filepath))
            duration = clip.duration
            clip.close()
            return f"[VIDEO: {filepath.name}]\nDuration: {duration:.2f} seconds\nNote: This is a video lecture file."
        except Exception as e:
            print(f"Error reading {filepath.name}: {e}")
            return f"[VIDEO: {filepath.name}]\nNote: Video file present but metadata unavailable."


class StudentChatbot:
    """Main chatbot application."""
    
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key or self.api_key == "your_mistral_api_key_here":
            print("ERROR: MISTRAL_API_KEY not found in .env file")
            print("Please create a .env file with your Mistral API key.")
            print("Example: MISTRAL_API_KEY=your_actual_key_here")
            sys.exit(1)
        
        self.client = Mistral(api_key=self.api_key)
        self.model = "mistral-small-latest"
        self.corpus = ChatbotCorpus()
        self.conversation_history = []
        self.saved_qa_pairs = []
        self.storage_file = Path("qa_conversations.json")
        self._load_saved_conversations()
        
    def _load_saved_conversations(self):
        """Load previously saved Q&A pairs from JSON file."""
        if self.storage_file.exists():
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    self.saved_qa_pairs = json.load(f)
                print(f"Loaded {len(self.saved_qa_pairs)} saved Q&A pairs from previous sessions.")
            except Exception as e:
                print(f"Error loading saved conversations: {e}")
                self.saved_qa_pairs = []
        else:
            print("No previous conversations found. Starting fresh.")
    
    def _save_conversations_to_file(self):
        """Save all Q&A pairs to JSON file."""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.saved_qa_pairs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving conversations: {e}")
        
    def initialize(self):
        """Initialize the chatbot and load corpus."""
        print("=" * 60)
        print("Welcome to the INFO 6200 Student Q&A Chatbot!")
        print("=" * 60)
        print("\nHello! I'm your AI teaching assistant for INFO 6200.")
        print("I'm here to help you with Python coding questions and course content.")
        print("\nLoading course materials...")
        self.corpus.load_corpus()
        
    def chat(self):
        """Main chat loop."""
        print("You can ask me questions about the course. Type 'exit' to quit.")
        print("Commands:")
        print("  - 'save': Save the last Q&A pair")
        print("  - 'list': View all saved Q&A pairs")
        print("  - 'exit': End the session")
        print("-" * 60)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'exit':
                self._save_conversations_to_file()
                print("\nConversations saved! Thank you for using the chatbot. Good luck with your studies!")
                break
            
            if user_input.lower() == 'save':
                self._save_last_qa()
                continue
            
            if user_input.lower() == 'list':
                self._list_saved_qa()
                continue
            
            # Get AI response
            response = self._get_ai_response(user_input)
            print(f"\nAssistant: {response}")
            
            # Store in conversation history
            self.conversation_history.append({
                "question": user_input,
                "answer": response,
                "timestamp": datetime.now().isoformat()
            })
    
    def _get_ai_response(self, question):
        """Get response from Mistral AI."""
        try:
            # Build context with corpus
            system_message = (
                "You are a helpful teaching assistant for INFO 6200, a Python coding course. "
                "Answer student questions clearly and concisely based on the course materials provided. "
                "If the answer isn't in the course materials, provide general Python guidance but mention "
                "that students should verify with their professor."
            )
            
            if self.corpus.corpus_text:
                system_message += f"\n\nCourse Materials:\n{self.corpus.corpus_text}"
            
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": question}
            ]
            
            response = self.client.chat.complete(
                model=self.model,
                messages=messages
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}\nPlease try again."
    
    def _save_last_qa(self):
        """Save the last question-answer pair."""
        if not self.conversation_history:
            print("No conversation to save yet!")
            return
        
        last_qa = self.conversation_history[-1].copy()
        last_qa["saved_at"] = datetime.now().isoformat()
        last_qa["id"] = len(self.saved_qa_pairs) + 1
        
        self.saved_qa_pairs.append(last_qa)
        self._save_conversations_to_file()
        print(f"✓ Saved as Q&A #{last_qa['id']}")
    
    def _list_saved_qa(self):
        """List all saved Q&A pairs."""
        if not self.saved_qa_pairs:
            print("No saved Q&A pairs yet!")
            return
        
        print("\n" + "=" * 60)
        print("SAVED Q&A PAIRS")
        print("=" * 60)
        for qa in self.saved_qa_pairs:
            print(f"\n[Q&A #{qa['id']}] - {qa.get('saved_at', 'N/A')}")
            print(f"Q: {qa['question']}")
            print(f"A: {qa['answer']}")
            print("-" * 60)


def main():
    """Main entry point."""
    chatbot = StudentChatbot()
    chatbot.initialize()
    chatbot.chat()


if __name__ == "__main__":
    main()
