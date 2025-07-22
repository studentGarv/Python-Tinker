#!/usr/bin/env python3
"""
Python Thinker App Launcher
Choose between command-line and GUI versions
"""

import sys
import os

def main():
    """Main launcher function"""
    print("🧠 Welcome to Python Thinker App!")
    print("=" * 40)
    print("Choose your interface:")
    print("1. 🖥️  Command Line Interface (CLI)")
    print("2. 🖼️  Graphical User Interface (GUI)")
    print("3. ❓ Help")
    print("4. 🚪 Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                print("\n🚀 Launching CLI version...")
                from thinker_app import main as cli_main
                cli_main()
                break
            elif choice == '2':
                print("\n🚀 Launching GUI version...")
                try:
                    from thinker_gui import main as gui_main
                    gui_main()
                except ImportError as e:
                    print(f"❌ GUI version requires tkinter. Error: {e}")
                    print("💡 Try installing tkinter or use the CLI version (option 1)")
                break
            elif choice == '3':
                show_help()
            elif choice == '4':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")

def show_help():
    """Display help information"""
    help_text = """
🧠 Python Thinker App - Help
============================

WHAT IS IT?
Python Thinker is a tool to help you organize your thoughts, brainstorm ideas,
and structure your thinking process. It supports both command-line and 
graphical interfaces.

FEATURES:
• 📚 Create multiple thinking sessions for different topics
• 💭 Add thoughts with categories, priorities, and tags
• 🧠 Interactive brainstorming mode for rapid idea capture
• ✅ Mark thoughts as completed when acted upon
• 📄 Export sessions to text or markdown files
• 💾 Automatic data persistence

VERSIONS:
1. CLI Version (thinker_app.py):
   • Text-based interface
   • Keyboard-driven commands
   • Works on any system with Python
   • Great for quick note-taking

2. GUI Version (thinker_gui.py):
   • Visual interface with buttons and menus
   • Mouse-driven interaction
   • Requires tkinter (usually included with Python)
   • Better for extended brainstorming sessions

GETTING STARTED:
1. Choose your preferred interface (CLI or GUI)
2. Create a new thinking session with a descriptive title
3. Start adding thoughts with categories and priorities
4. Use brainstorm mode for rapid idea capture
5. Export your sessions when ready to share or review

TIPS:
• Use descriptive session titles (e.g., "Project Ideas", "Daily Goals")
• Set priorities: 1=low importance, 5=high importance
• Use categories to group related thoughts
• Tag thoughts for easy searching and organization
• Regular brainstorming sessions boost creativity

DATA STORAGE:
Your thoughts are automatically saved to 'thoughts.json' in the app directory.
You can backup this file or load different data files as needed.
    """
    print(help_text)

if __name__ == "__main__":
    main()
