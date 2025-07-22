#!/usr/bin/env python3
"""
Python Thinker App - A tool to help organize thoughts, brainstorm ideas, and structure thinking
"""

import json
import os
import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
import uuid

@dataclass
class Thought:
    """Represents a single thought or idea"""
    id: str
    content: str
    category: str
    priority: int  # 1-5 scale
    tags: List[str]
    created_at: str
    updated_at: str
    is_completed: bool = False

@dataclass
class ThinkingSession:
    """Represents a thinking session with multiple thoughts"""
    id: str
    title: str
    description: str
    thoughts: List[Thought]
    created_at: str
    updated_at: str

class ThinkerApp:
    """Main application class for the Python Thinker"""
    
    def __init__(self, data_file: str = "thoughts.json"):
        self.data_file = data_file
        self.sessions: List[ThinkingSession] = []
        self.current_session: ThinkingSession = None
        self.load_data()
    
    def load_data(self):
        """Load existing thinking sessions from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.sessions = []
                    for session_data in data:
                        thoughts = [Thought(**thought) for thought in session_data['thoughts']]
                        session = ThinkingSession(
                            id=session_data['id'],
                            title=session_data['title'],
                            description=session_data['description'],
                            thoughts=thoughts,
                            created_at=session_data['created_at'],
                            updated_at=session_data['updated_at']
                        )
                        self.sessions.append(session)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading data: {e}")
                self.sessions = []
    
    def save_data(self):
        """Save thinking sessions to file"""
        try:
            data = []
            for session in self.sessions:
                session_dict = asdict(session)
                data.append(session_dict)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("✅ Data saved successfully!")
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def create_session(self, title: str, description: str = ""):
        """Create a new thinking session"""
        session_id = str(uuid.uuid4())[:8]
        timestamp = datetime.datetime.now().isoformat()
        
        session = ThinkingSession(
            id=session_id,
            title=title,
            description=description,
            thoughts=[],
            created_at=timestamp,
            updated_at=timestamp
        )
        
        self.sessions.append(session)
        self.current_session = session
        print(f"🧠 Created new thinking session: '{title}' (ID: {session_id})")
        return session
    
    def list_sessions(self):
        """List all thinking sessions"""
        if not self.sessions:
            print("📝 No thinking sessions found. Create one to get started!")
            return
        
        print("\n📚 Your Thinking Sessions:")
        print("-" * 50)
        for i, session in enumerate(self.sessions, 1):
            status = "🟢 Active" if session == self.current_session else "⚪ Inactive"
            thought_count = len(session.thoughts)
            completed_thoughts = len([t for t in session.thoughts if t.is_completed])
            
            print(f"{i}. {session.title} ({session.id})")
            print(f"   {status} | {thought_count} thoughts ({completed_thoughts} completed)")
            print(f"   Created: {session.created_at[:19]}")
            if session.description:
                print(f"   Description: {session.description}")
            print()
    
    def select_session(self, session_id: str):
        """Select a session to work with"""
        for session in self.sessions:
            if session.id == session_id:
                self.current_session = session
                print(f"🎯 Selected session: '{session.title}'")
                return session
        print(f"❌ Session with ID '{session_id}' not found")
        return None
    
    def add_thought(self, content: str, category: str = "general", priority: int = 3, tags: List[str] = None):
        """Add a new thought to the current session"""
        if not self.current_session:
            print("❌ No active session. Create or select a session first.")
            return
        
        if tags is None:
            tags = []
        
        thought_id = str(uuid.uuid4())[:8]
        timestamp = datetime.datetime.now().isoformat()
        
        thought = Thought(
            id=thought_id,
            content=content,
            category=category,
            priority=priority,
            tags=tags,
            created_at=timestamp,
            updated_at=timestamp
        )
        
        self.current_session.thoughts.append(thought)
        self.current_session.updated_at = timestamp
        print(f"💡 Added thought: '{content[:50]}...' (ID: {thought_id})")
    
    def list_thoughts(self, category: str = None, completed: bool = None):
        """List thoughts in the current session"""
        if not self.current_session:
            print("❌ No active session selected")
            return
        
        thoughts = self.current_session.thoughts
        
        # Filter by category
        if category:
            thoughts = [t for t in thoughts if t.category.lower() == category.lower()]
        
        # Filter by completion status
        if completed is not None:
            thoughts = [t for t in thoughts if t.is_completed == completed]
        
        if not thoughts:
            print("🤔 No thoughts found with the specified criteria")
            return
        
        print(f"\n💭 Thoughts in '{self.current_session.title}':")
        print("-" * 60)
        
        # Sort by priority (high to low)
        thoughts.sort(key=lambda x: x.priority, reverse=True)
        
        for thought in thoughts:
            status = "✅" if thought.is_completed else "⭕"
            priority_stars = "⭐" * thought.priority
            
            print(f"{status} {thought.content}")
            print(f"   ID: {thought.id} | Category: {thought.category} | Priority: {priority_stars}")
            if thought.tags:
                print(f"   Tags: {', '.join(thought.tags)}")
            print(f"   Created: {thought.created_at[:19]}")
            print()
    
    def complete_thought(self, thought_id: str):
        """Mark a thought as completed"""
        if not self.current_session:
            print("❌ No active session selected")
            return
        
        for thought in self.current_session.thoughts:
            if thought.id == thought_id:
                thought.is_completed = True
                thought.updated_at = datetime.datetime.now().isoformat()
                self.current_session.updated_at = thought.updated_at
                print(f"✅ Marked thought as completed: '{thought.content[:50]}...'")
                return
        
        print(f"❌ Thought with ID '{thought_id}' not found")
    
    def delete_thought(self, thought_id: str):
        """Delete a thought from the current session"""
        if not self.current_session:
            print("❌ No active session selected")
            return
        
        for i, thought in enumerate(self.current_session.thoughts):
            if thought.id == thought_id:
                deleted_thought = self.current_session.thoughts.pop(i)
                self.current_session.updated_at = datetime.datetime.now().isoformat()
                print(f"🗑️ Deleted thought: '{deleted_thought.content[:50]}...'")
                return
        
        print(f"❌ Thought with ID '{thought_id}' not found")
    
    def brainstorm_session(self):
        """Interactive brainstorming session"""
        if not self.current_session:
            print("❌ No active session. Create or select a session first.")
            return
        
        print(f"\n🧠 Starting brainstorming session for: '{self.current_session.title}'")
        print("💡 Enter your thoughts (type 'done' to finish, 'help' for commands)")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n💭 Your thought: ").strip()
                
                if user_input.lower() == 'done':
                    break
                elif user_input.lower() == 'help':
                    self.show_brainstorm_help()
                    continue
                elif user_input.lower().startswith('priority:'):
                    # Handle priority setting: "priority:5 This is important"
                    parts = user_input.split(' ', 1)
                    if len(parts) == 2:
                        try:
                            priority = int(parts[0].split(':')[1])
                            content = parts[1]
                            self.add_thought(content, priority=min(max(priority, 1), 5))
                        except ValueError:
                            print("❌ Invalid priority format. Use: priority:1-5 your thought")
                    continue
                elif user_input.lower().startswith('category:'):
                    # Handle category setting: "category:ideas This is an idea"
                    parts = user_input.split(' ', 1)
                    if len(parts) == 2:
                        category = parts[0].split(':')[1]
                        content = parts[1]
                        self.add_thought(content, category=category)
                    continue
                elif not user_input:
                    continue
                
                # Regular thought
                self.add_thought(user_input)
                
            except KeyboardInterrupt:
                print("\n\n🛑 Brainstorming session interrupted")
                break
        
        print(f"\n🎉 Brainstorming session completed! Added thoughts to '{self.current_session.title}'")
    
    def show_brainstorm_help(self):
        """Show help for brainstorming session"""
        print("\n📖 Brainstorming Commands:")
        print("  • Just type your thought and press Enter")
        print("  • 'priority:1-5 your thought' - Set priority (1=low, 5=high)")
        print("  • 'category:name your thought' - Set category")
        print("  • 'help' - Show this help")
        print("  • 'done' - Finish brainstorming session")
    
    def export_session(self, session_id: str = None, format: str = "txt"):
        """Export a session to a file"""
        session = self.current_session
        if session_id:
            session = next((s for s in self.sessions if s.id == session_id), None)
        
        if not session:
            print("❌ No session to export")
            return
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"thinking_session_{session.id}_{timestamp}.{format}"
        
        try:
            if format == "txt":
                self._export_to_txt(session, filename)
            elif format == "md":
                self._export_to_markdown(session, filename)
            else:
                print("❌ Unsupported format. Use 'txt' or 'md'")
                return
            
            print(f"📄 Session exported to: {filename}")
        except Exception as e:
            print(f"❌ Error exporting session: {e}")
    
    def _export_to_txt(self, session: ThinkingSession, filename: str):
        """Export session to plain text"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Thinking Session: {session.title}\n")
            f.write("=" * 50 + "\n\n")
            
            if session.description:
                f.write(f"Description: {session.description}\n\n")
            
            f.write(f"Created: {session.created_at[:19]}\n")
            f.write(f"Updated: {session.updated_at[:19]}\n")
            f.write(f"Total Thoughts: {len(session.thoughts)}\n\n")
            
            # Group thoughts by category
            categories = {}
            for thought in session.thoughts:
                if thought.category not in categories:
                    categories[thought.category] = []
                categories[thought.category].append(thought)
            
            for category, thoughts in categories.items():
                f.write(f"\n{category.upper()}\n")
                f.write("-" * len(category) + "\n\n")
                
                # Sort by priority
                thoughts.sort(key=lambda x: x.priority, reverse=True)
                
                for thought in thoughts:
                    status = "[✓]" if thought.is_completed else "[ ]"
                    priority = "★" * thought.priority
                    f.write(f"{status} {thought.content}\n")
                    f.write(f"    Priority: {priority} | Tags: {', '.join(thought.tags)}\n")
                    f.write(f"    Created: {thought.created_at[:19]}\n\n")
    
    def _export_to_markdown(self, session: ThinkingSession, filename: str):
        """Export session to markdown"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {session.title}\n\n")
            
            if session.description:
                f.write(f"**Description:** {session.description}\n\n")
            
            f.write(f"- **Created:** {session.created_at[:19]}\n")
            f.write(f"- **Updated:** {session.updated_at[:19]}\n")
            f.write(f"- **Total Thoughts:** {len(session.thoughts)}\n\n")
            
            # Group thoughts by category
            categories = {}
            for thought in session.thoughts:
                if thought.category not in categories:
                    categories[thought.category] = []
                categories[thought.category].append(thought)
            
            for category, thoughts in categories.items():
                f.write(f"\n## {category.title()}\n\n")
                
                # Sort by priority
                thoughts.sort(key=lambda x: x.priority, reverse=True)
                
                for thought in thoughts:
                    checkbox = "- [x]" if thought.is_completed else "- [ ]"
                    priority = "⭐" * thought.priority
                    f.write(f"{checkbox} **{thought.content}**\n")
                    f.write(f"  - Priority: {priority}\n")
                    if thought.tags:
                        f.write(f"  - Tags: {', '.join(thought.tags)}\n")
                    f.write(f"  - Created: {thought.created_at[:19]}\n\n")

def main():
    """Main function to run the Thinker App"""
    app = ThinkerApp()
    
    print("🧠 Welcome to the Python Thinker App!")
    print("💭 Organize your thoughts, brainstorm ideas, and structure your thinking")
    print("Type 'help' for available commands\n")
    
    while True:
        try:
            command = input("🤔 thinker> ").strip().lower()
            
            if command == 'help':
                show_help()
            elif command == 'quit' or command == 'exit':
                app.save_data()
                print("👋 Thanks for using Python Thinker! Your thoughts have been saved.")
                break
            elif command == 'sessions':
                app.list_sessions()
            elif command.startswith('create '):
                title = command[7:].strip()
                if title:
                    app.create_session(title)
                else:
                    print("❌ Please provide a session title")
            elif command.startswith('select '):
                session_id = command[7:].strip()
                app.select_session(session_id)
            elif command.startswith('add '):
                content = command[4:].strip()
                if content:
                    app.add_thought(content)
                else:
                    print("❌ Please provide thought content")
            elif command == 'thoughts':
                app.list_thoughts()
            elif command.startswith('complete '):
                thought_id = command[9:].strip()
                app.complete_thought(thought_id)
            elif command.startswith('delete '):
                thought_id = command[7:].strip()
                app.delete_thought(thought_id)
            elif command == 'brainstorm':
                app.brainstorm_session()
            elif command.startswith('export'):
                parts = command.split()
                format_type = parts[1] if len(parts) > 1 else "txt"
                app.export_session(format=format_type)
            elif command == 'save':
                app.save_data()
            elif command == '':
                continue
            else:
                print("❌ Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n\n🛑 Use 'quit' to exit properly and save your data.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")

def show_help():
    """Display help information"""
    print("\n📖 Python Thinker App Commands:")
    print("─" * 50)
    print("🗂️  Session Management:")
    print("  sessions                 - List all thinking sessions")
    print("  create <title>          - Create a new thinking session")
    print("  select <session_id>     - Select a session to work with")
    print()
    print("💭 Thought Management:")
    print("  add <thought>           - Add a thought to current session")
    print("  thoughts                - List thoughts in current session")
    print("  complete <thought_id>   - Mark a thought as completed")
    print("  delete <thought_id>     - Delete a thought")
    print()
    print("🧠 Thinking Tools:")
    print("  brainstorm              - Start interactive brainstorming")
    print("  export [txt|md]         - Export current session to file")
    print()
    print("💾 Data Management:")
    print("  save                    - Save all data to file")
    print("  quit/exit               - Save and exit the application")
    print()
    print("💡 Tips:")
    print("  • Use descriptive session titles")
    print("  • Set priorities (1-5) during brainstorming: 'priority:5 important idea'")
    print("  • Categorize thoughts: 'category:goals finish the project'")
    print("  • Use tags to organize related thoughts")

if __name__ == "__main__":
    main()
