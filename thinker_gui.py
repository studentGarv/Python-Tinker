#!/usr/bin/env python3
"""
Python Thinker App - GUI Version with tkinter
A visual interface for organizing thoughts and brainstorming
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import os
import datetime
from typing import List, Dict
import uuid
from dataclasses import dataclass, asdict

# Import the core classes from the main app
from thinker_app import Thought, ThinkingSession, ThinkerApp

class ThinkerGUI:
    """GUI wrapper for the ThinkerApp"""
    
    def __init__(self):
        self.app = ThinkerApp()
        self.root = tk.Tk()
        self.root.title("🧠 Python Thinker App")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        
        self.create_widgets()
        self.refresh_displays()
    
    def create_widgets(self):
        """Create and layout GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🧠 Python Thinker App", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Left panel - Sessions
        self.create_session_panel(main_frame)
        
        # Right panel - Thoughts
        self.create_thoughts_panel(main_frame)
        
        # Bottom panel - Controls
        self.create_control_panel(main_frame)
    
    def create_session_panel(self, parent):
        """Create the session management panel"""
        session_frame = ttk.LabelFrame(parent, text="📚 Thinking Sessions", padding="10")
        session_frame.grid(row=1, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        session_frame.columnconfigure(0, weight=1)
        session_frame.rowconfigure(1, weight=1)
        
        # Session creation
        create_frame = ttk.Frame(session_frame)
        create_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        create_frame.columnconfigure(1, weight=1)
        
        ttk.Label(create_frame, text="New Session:").grid(row=0, column=0, sticky=tk.W)
        self.session_title_var = tk.StringVar()
        session_entry = ttk.Entry(create_frame, textvariable=self.session_title_var)
        session_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        session_entry.bind('<Return>', lambda e: self.create_session())
        
        create_btn = ttk.Button(create_frame, text="Create", command=self.create_session)
        create_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Session list
        self.session_listbox = tk.Listbox(session_frame, height=10)
        self.session_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.session_listbox.bind('<<ListboxSelect>>', self.on_session_select)
        
        # Session scrollbar
        session_scrollbar = ttk.Scrollbar(session_frame, orient=tk.VERTICAL, command=self.session_listbox.yview)
        session_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.session_listbox.configure(yscrollcommand=session_scrollbar.set)
        
        # Session buttons
        session_btn_frame = ttk.Frame(session_frame)
        session_btn_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(session_btn_frame, text="Export TXT", command=lambda: self.export_session('txt')).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(session_btn_frame, text="Export MD", command=lambda: self.export_session('md')).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(session_btn_frame, text="Delete", command=self.delete_session).pack(side=tk.LEFT)
    
    def create_thoughts_panel(self, parent):
        """Create the thoughts management panel"""
        thoughts_frame = ttk.LabelFrame(parent, text="💭 Thoughts", padding="10")
        thoughts_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        thoughts_frame.columnconfigure(0, weight=1)
        thoughts_frame.rowconfigure(1, weight=1)
        
        # Thought input
        input_frame = ttk.Frame(thoughts_frame)
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # Thought text area
        self.thought_text = scrolledtext.ScrolledText(input_frame, height=3, wrap=tk.WORD)
        self.thought_text.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Thought metadata
        meta_frame = ttk.Frame(input_frame)
        meta_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E))
        
        ttk.Label(meta_frame, text="Category:").pack(side=tk.LEFT)
        self.category_var = tk.StringVar(value="general")
        category_entry = ttk.Entry(meta_frame, textvariable=self.category_var, width=15)
        category_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(meta_frame, text="Priority:").pack(side=tk.LEFT)
        self.priority_var = tk.IntVar(value=3)
        priority_spin = ttk.Spinbox(meta_frame, from_=1, to=5, textvariable=self.priority_var, width=5)
        priority_spin.pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(meta_frame, text="Tags (comma-separated):").pack(side=tk.LEFT)
        self.tags_var = tk.StringVar()
        tags_entry = ttk.Entry(meta_frame, textvariable=self.tags_var, width=20)
        tags_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        add_btn = ttk.Button(meta_frame, text="Add Thought", command=self.add_thought)
        add_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Thoughts display
        thoughts_display_frame = ttk.Frame(thoughts_frame)
        thoughts_display_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        thoughts_display_frame.columnconfigure(0, weight=1)
        thoughts_display_frame.rowconfigure(0, weight=1)
        
        # Thoughts treeview
        columns = ('Status', 'Content', 'Category', 'Priority', 'Tags', 'Created')
        self.thoughts_tree = ttk.Treeview(thoughts_display_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.thoughts_tree.heading('Status', text='✓')
        self.thoughts_tree.heading('Content', text='Content')
        self.thoughts_tree.heading('Category', text='Category')
        self.thoughts_tree.heading('Priority', text='Priority')
        self.thoughts_tree.heading('Tags', text='Tags')
        self.thoughts_tree.heading('Created', text='Created')
        
        self.thoughts_tree.column('Status', width=50, minwidth=50)
        self.thoughts_tree.column('Content', width=300, minwidth=200)
        self.thoughts_tree.column('Category', width=100, minwidth=80)
        self.thoughts_tree.column('Priority', width=80, minwidth=60)
        self.thoughts_tree.column('Tags', width=120, minwidth=100)
        self.thoughts_tree.column('Created', width=150, minwidth=120)
        
        self.thoughts_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Thoughts scrollbar
        thoughts_scrollbar = ttk.Scrollbar(thoughts_display_frame, orient=tk.VERTICAL, command=self.thoughts_tree.yview)
        thoughts_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.thoughts_tree.configure(yscrollcommand=thoughts_scrollbar.set)
        
        # Thoughts context menu
        self.create_thoughts_context_menu()
    
    def create_control_panel(self, parent):
        """Create the control panel"""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=3, column=0, columnspan=3, pady=(20, 0))
        
        ttk.Button(control_frame, text="🧠 Brainstorm Mode", command=self.brainstorm_mode).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="💾 Save Data", command=self.save_data).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="📁 Load Data", command=self.load_data).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="❓ Help", command=self.show_help).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="🚪 Exit", command=self.exit_app).pack(side=tk.RIGHT)
    
    def create_thoughts_context_menu(self):
        """Create context menu for thoughts"""
        self.thoughts_menu = tk.Menu(self.root, tearoff=0)
        self.thoughts_menu.add_command(label="Complete", command=self.complete_thought)
        self.thoughts_menu.add_command(label="Edit", command=self.edit_thought)
        self.thoughts_menu.add_command(label="Delete", command=self.delete_thought)
        
        self.thoughts_tree.bind("<Button-3>", self.show_thoughts_context_menu)
    
    def show_thoughts_context_menu(self, event):
        """Show context menu for thoughts"""
        item = self.thoughts_tree.selection()[0] if self.thoughts_tree.selection() else None
        if item:
            try:
                self.thoughts_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.thoughts_menu.grab_release()
    
    def create_session(self):
        """Create a new thinking session"""
        title = self.session_title_var.get().strip()
        if not title:
            messagebox.showwarning("Warning", "Please enter a session title")
            return
        
        self.app.create_session(title)
        self.session_title_var.set("")
        self.refresh_displays()
    
    def on_session_select(self, event):
        """Handle session selection"""
        selection = self.session_listbox.curselection()
        if selection:
            session_info = self.session_listbox.get(selection[0])
            session_id = session_info.split('(')[1].split(')')[0]  # Extract ID from display text
            self.app.select_session(session_id)
            self.refresh_thoughts_display()
    
    def add_thought(self):
        """Add a new thought"""
        content = self.thought_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Please enter thought content")
            return
        
        category = self.category_var.get().strip() or "general"
        priority = self.priority_var.get()
        tags = [tag.strip() for tag in self.tags_var.get().split(',') if tag.strip()]
        
        self.app.add_thought(content, category, priority, tags)
        
        # Clear input fields
        self.thought_text.delete(1.0, tk.END)
        self.tags_var.set("")
        
        self.refresh_thoughts_display()
    
    def complete_thought(self):
        """Mark selected thought as completed"""
        selection = self.thoughts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a thought")
            return
        
        item = selection[0]
        thought_id = self.thoughts_tree.item(item)['tags'][0]  # Store ID in tags
        self.app.complete_thought(thought_id)
        self.refresh_thoughts_display()
    
    def edit_thought(self):
        """Edit selected thought"""
        selection = self.thoughts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a thought")
            return
        
        item = selection[0]
        values = self.thoughts_tree.item(item)['values']
        thought_id = self.thoughts_tree.item(item)['tags'][0]
        
        # Find the thought
        thought = None
        if self.app.current_session:
            for t in self.app.current_session.thoughts:
                if t.id == thought_id:
                    thought = t
                    break
        
        if not thought:
            return
        
        # Create edit dialog
        self.create_edit_dialog(thought)
    
    def create_edit_dialog(self, thought):
        """Create dialog for editing a thought"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Thought")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Content
        ttk.Label(dialog, text="Content:").pack(anchor=tk.W, padx=10, pady=(10, 5))
        content_text = scrolledtext.ScrolledText(dialog, height=8, wrap=tk.WORD)
        content_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        content_text.insert(1.0, thought.content)
        
        # Metadata frame
        meta_frame = ttk.Frame(dialog)
        meta_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(meta_frame, text="Category:").grid(row=0, column=0, sticky=tk.W)
        category_var = tk.StringVar(value=thought.category)
        ttk.Entry(meta_frame, textvariable=category_var).grid(row=0, column=1, padx=(5, 20))
        
        ttk.Label(meta_frame, text="Priority:").grid(row=0, column=2, sticky=tk.W)
        priority_var = tk.IntVar(value=thought.priority)
        ttk.Spinbox(meta_frame, from_=1, to=5, textvariable=priority_var, width=5).grid(row=0, column=3, padx=(5, 0))
        
        ttk.Label(meta_frame, text="Tags:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        tags_var = tk.StringVar(value=', '.join(thought.tags))
        ttk.Entry(meta_frame, textvariable=tags_var, width=40).grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), padx=(5, 0), pady=(5, 0))
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        def save_changes():
            thought.content = content_text.get(1.0, tk.END).strip()
            thought.category = category_var.get().strip() or "general"
            thought.priority = priority_var.get()
            thought.tags = [tag.strip() for tag in tags_var.get().split(',') if tag.strip()]
            thought.updated_at = datetime.datetime.now().isoformat()
            
            if self.app.current_session:
                self.app.current_session.updated_at = thought.updated_at
            
            self.refresh_thoughts_display()
            dialog.destroy()
        
        ttk.Button(btn_frame, text="Save", command=save_changes).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)
    
    def delete_thought(self):
        """Delete selected thought"""
        selection = self.thoughts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a thought")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this thought?"):
            item = selection[0]
            thought_id = self.thoughts_tree.item(item)['tags'][0]
            self.app.delete_thought(thought_id)
            self.refresh_thoughts_display()
    
    def delete_session(self):
        """Delete selected session"""
        selection = self.session_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a session")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this session?"):
            session_info = self.session_listbox.get(selection[0])
            session_id = session_info.split('(')[1].split(')')[0]
            
            # Find and remove session
            self.app.sessions = [s for s in self.app.sessions if s.id != session_id]
            if self.app.current_session and self.app.current_session.id == session_id:
                self.app.current_session = None
            
            self.refresh_displays()
    
    def export_session(self, format_type):
        """Export current session"""
        if not self.app.current_session:
            messagebox.showwarning("Warning", "No session selected")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=f".{format_type}",
            filetypes=[(f"{format_type.upper()} files", f"*.{format_type}"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if format_type == "txt":
                    self.app._export_to_txt(self.app.current_session, filename)
                else:
                    self.app._export_to_markdown(self.app.current_session, filename)
                messagebox.showinfo("Success", f"Session exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export session: {e}")
    
    def brainstorm_mode(self):
        """Open brainstorming mode window"""
        if not self.app.current_session:
            messagebox.showwarning("Warning", "Please create or select a session first")
            return
        
        BrainstormWindow(self.root, self.app, self.refresh_thoughts_display)
    
    def save_data(self):
        """Save data to file"""
        self.app.save_data()
        messagebox.showinfo("Success", "Data saved successfully!")
    
    def load_data(self):
        """Load data from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            self.app.data_file = filename
            self.app.load_data()
            self.refresh_displays()
            messagebox.showinfo("Success", "Data loaded successfully!")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
🧠 Python Thinker App - Help

📚 Sessions:
• Create new thinking sessions to organize your thoughts by topic
• Select a session to view and manage its thoughts
• Export sessions to TXT or Markdown format

💭 Thoughts:
• Add thoughts with categories, priorities (1-5), and tags
• Right-click on thoughts to complete, edit, or delete them
• Use categories to group related thoughts
• Set priorities to focus on important ideas

🧠 Brainstorm Mode:
• Quick thought capture interface
• Add multiple thoughts rapidly
• Perfect for creative sessions

💾 Data Management:
• Your data is automatically saved to thoughts.json
• Use Save/Load to work with different files
• Export individual sessions for sharing

💡 Tips:
• Use descriptive session titles
• Set meaningful categories and priorities
• Regular brainstorming sessions boost creativity
• Export sessions to share ideas with others
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - Python Thinker")
        help_window.geometry("600x500")
        help_window.transient(self.root)
        
        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(1.0, help_text)
        text_widget.configure(state='disabled')
    
    def exit_app(self):
        """Exit the application"""
        if messagebox.askyesno("Exit", "Save data before exiting?"):
            self.app.save_data()
        self.root.destroy()
    
    def refresh_displays(self):
        """Refresh all displays"""
        self.refresh_sessions_display()
        self.refresh_thoughts_display()
    
    def refresh_sessions_display(self):
        """Refresh the sessions listbox"""
        self.session_listbox.delete(0, tk.END)
        for session in self.app.sessions:
            thought_count = len(session.thoughts)
            completed_count = len([t for t in session.thoughts if t.is_completed])
            status = "🟢" if session == self.app.current_session else "⚪"
            display_text = f"{status} {session.title} ({session.id}) - {thought_count} thoughts ({completed_count} done)"
            self.session_listbox.insert(tk.END, display_text)
    
    def refresh_thoughts_display(self):
        """Refresh the thoughts treeview"""
        # Clear existing items
        for item in self.thoughts_tree.get_children():
            self.thoughts_tree.delete(item)
        
        if not self.app.current_session:
            return
        
        # Sort thoughts by priority (high to low)
        thoughts = sorted(self.app.current_session.thoughts, key=lambda x: x.priority, reverse=True)
        
        for thought in thoughts:
            status = "✅" if thought.is_completed else "⭕"
            priority_stars = "⭐" * thought.priority
            tags_str = ", ".join(thought.tags)
            created_str = thought.created_at[:19]
            
            # Truncate long content for display
            content_display = thought.content[:80] + "..." if len(thought.content) > 80 else thought.content
            
            item = self.thoughts_tree.insert('', tk.END, values=(
                status, content_display, thought.category, priority_stars, tags_str, created_str
            ), tags=(thought.id,))  # Store ID in tags for reference
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

class BrainstormWindow:
    """Dedicated brainstorming window"""
    
    def __init__(self, parent, app, refresh_callback):
        self.app = app
        self.refresh_callback = refresh_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"🧠 Brainstorming: {app.current_session.title}")
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_widgets()
        self.thought_entry.focus()
    
    def create_widgets(self):
        """Create brainstorming window widgets"""
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        instructions = ttk.Label(main_frame, 
            text="💡 Quick Brainstorming Mode - Type thoughts and press Enter to add them",
            font=('Arial', 12, 'bold'))
        instructions.pack(pady=(0, 20))
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        ttk.Label(input_frame, text="Your thought:").grid(row=0, column=0, sticky=tk.W)
        
        self.thought_entry = tk.Text(input_frame, height=3, wrap=tk.WORD)
        self.thought_entry.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 10))
        self.thought_entry.bind('<Control-Return>', self.add_thought)
        
        # Quick options
        options_frame = ttk.Frame(input_frame)
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        ttk.Label(options_frame, text="Category:").pack(side=tk.LEFT)
        self.category_var = tk.StringVar(value="brainstorm")
        ttk.Entry(options_frame, textvariable=self.category_var, width=15).pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(options_frame, text="Priority:").pack(side=tk.LEFT)
        self.priority_var = tk.IntVar(value=3)
        ttk.Spinbox(options_frame, from_=1, to=5, textvariable=self.priority_var, width=5).pack(side=tk.LEFT, padx=(5, 15))
        
        add_btn = ttk.Button(options_frame, text="Add Thought (Ctrl+Enter)", command=self.add_thought)
        add_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Recent thoughts display
        ttk.Label(main_frame, text="Recent thoughts added:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(20, 5))
        
        self.recent_listbox = tk.Listbox(main_frame, height=10)
        self.recent_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="Done Brainstorming", command=self.finish_brainstorming).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(control_frame, text="Clear Input", command=self.clear_input).pack(side=tk.RIGHT)
    
    def add_thought(self, event=None):
        """Add a thought from the brainstorming window"""
        content = self.thought_entry.get(1.0, tk.END).strip()
        if not content:
            return
        
        category = self.category_var.get().strip() or "brainstorm"
        priority = self.priority_var.get()
        
        self.app.add_thought(content, category, priority, ["brainstorm"])
        
        # Add to recent list
        display_text = f"[{priority}⭐] {content[:60]}{'...' if len(content) > 60 else ''}"
        self.recent_listbox.insert(0, display_text)
        
        # Clear input
        self.clear_input()
        
        # Keep focus on entry
        self.thought_entry.focus()
    
    def clear_input(self):
        """Clear the thought input"""
        self.thought_entry.delete(1.0, tk.END)
    
    def finish_brainstorming(self):
        """Finish brainstorming session"""
        count = self.recent_listbox.size()
        self.refresh_callback()
        messagebox.showinfo("Brainstorming Complete", f"Added {count} thoughts to your session!")
        self.window.destroy()

def main():
    """Main function to run the GUI version"""
    app = ThinkerGUI()
    app.run()

if __name__ == "__main__":
    main()
