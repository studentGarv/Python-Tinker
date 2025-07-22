#!/usr/bin/env python3
"""
Python Thinker App - Demo Script
Demonstrates the core functionality with sample data
"""

from thinker_app import ThinkerApp
import time

def run_demo():
    """Run a demonstration of the Python Thinker App"""
    print("🧠 Python Thinker App - Demo")
    print("=" * 40)
    print("This demo will show you how to use the Thinker App programmatically")
    print("and create sample thinking sessions.\n")
    
    # Create app instance
    app = ThinkerApp("demo_thoughts.json")
    
    # Demo 1: Project Planning Session
    print("📚 Demo 1: Creating a Project Planning Session")
    print("-" * 50)
    
    session1 = app.create_session(
        "Website Redesign Project", 
        "Planning and ideas for the company website redesign"
    )
    
    # Add various thoughts
    thoughts_data = [
        ("Research competitor websites", "research", 4, ["competitive-analysis", "inspiration"]),
        ("Create user persona profiles", "planning", 5, ["ux", "research"]),
        ("Design new color scheme", "design", 3, ["visual", "branding"]),
        ("Implement responsive layout", "development", 4, ["technical", "mobile"]),
        ("Set up Google Analytics", "analytics", 3, ["tracking", "metrics"]),
        ("Write new homepage copy", "content", 4, ["copywriting", "marketing"]),
        ("Test on multiple browsers", "testing", 3, ["qa", "compatibility"]),
        ("Plan launch strategy", "marketing", 5, ["promotion", "launch"])
    ]
    
    for content, category, priority, tags in thoughts_data:
        app.add_thought(content, category, priority, tags)
        time.sleep(0.1)  # Small delay for demonstration
    
    print(f"✅ Added {len(thoughts_data)} thoughts to the project session")
    
    # Demo 2: Daily Goals Session
    print("\n📚 Demo 2: Creating a Daily Goals Session")
    print("-" * 50)
    
    session2 = app.create_session(
        "Today's Goals", 
        "Daily tasks and objectives to accomplish"
    )
    
    daily_thoughts = [
        ("Review and respond to emails", "communication", 4, ["email", "admin"]),
        ("Complete project proposal", "work", 5, ["deadline", "important"]),
        ("Schedule team meeting", "planning", 3, ["coordination", "team"]),
        ("Read industry news", "learning", 2, ["research", "knowledge"]),
        ("Exercise for 30 minutes", "health", 4, ["fitness", "wellness"]),
        ("Call mom", "personal", 3, ["family", "relationships"]),
        ("Plan weekend activities", "personal", 1, ["leisure", "planning"])
    ]
    
    for content, category, priority, tags in daily_thoughts:
        app.add_thought(content, category, priority, tags)
        time.sleep(0.1)
    
    print(f"✅ Added {len(daily_thoughts)} thoughts to the daily goals session")
    
    # Demo 3: Creative Brainstorming Session
    print("\n📚 Demo 3: Creating a Creative Brainstorming Session")
    print("-" * 50)
    
    session3 = app.create_session(
        "Mobile App Ideas", 
        "Brainstorming session for potential mobile application concepts"
    )
    
    creative_thoughts = [
        ("Habit tracking app with gamification", "apps", 4, ["habits", "gamification", "health"]),
        ("Local event discovery platform", "apps", 3, ["social", "location", "events"]),
        ("AI-powered recipe suggestions", "apps", 5, ["ai", "food", "personalization"]),
        ("Collaborative playlist maker", "apps", 2, ["music", "social", "collaboration"]),
        ("Virtual plant care assistant", "apps", 3, ["plants", "ar", "education"]),
        ("Micro-learning language app", "apps", 4, ["education", "language", "learning"]),
        ("Sustainable living tracker", "apps", 3, ["environment", "sustainability", "tracking"])
    ]
    
    for content, category, priority, tags in creative_thoughts:
        app.add_thought(content, category, priority, tags)
        time.sleep(0.1)
    
    print(f"✅ Added {len(creative_thoughts)} thoughts to the brainstorming session")
    
    # Demonstrate completion of some thoughts
    print("\n✅ Demo 4: Marking Some Thoughts as Completed")
    print("-" * 50)
    
    # Complete some thoughts from the daily goals
    app.select_session(session2.id)
    for thought in app.current_session.thoughts[:3]:  # Complete first 3 thoughts
        app.complete_thought(thought.id)
        print(f"✅ Completed: {thought.content}")
        time.sleep(0.1)
    
    # Demo 5: Display session summaries
    print("\n📊 Demo 5: Session Summaries")
    print("-" * 50)
    
    app.list_sessions()
    
    # Demo 6: Export a session
    print("\n📄 Demo 6: Exporting Session")
    print("-" * 50)
    
    app.select_session(session1.id)
    app.export_session(format="md")
    print("📄 Exported 'Website Redesign Project' to markdown file")
    
    # Save all data
    app.save_data()
    
    print("\n🎉 Demo Complete!")
    print("=" * 40)
    print("Sample data has been created and saved to 'demo_thoughts.json'")
    print("You can now:")
    print("1. Run 'python thinker_app.py' and load demo_thoughts.json")
    print("2. Run 'python thinker_gui.py' and load the demo file")
    print("3. Explore the sessions and thoughts created")
    print("4. Try adding your own thoughts and sessions")
    
    print("\n💡 Next Steps:")
    print("• Try the brainstorm mode for rapid idea capture")
    print("• Experiment with different categories and priorities")
    print("• Export sessions to share with others")
    print("• Create your own thinking sessions for real projects")

def create_sample_workflow():
    """Create a sample workflow demonstration"""
    print("\n🔄 Bonus: Sample Workflow Demonstration")
    print("-" * 50)
    
    app = ThinkerApp("workflow_demo.json")
    
    # Workflow: Planning a vacation
    vacation_session = app.create_session(
        "Summer Vacation Planning",
        "Planning our family summer vacation to Europe"
    )
    
    # Phase 1: Initial brainstorming
    brainstorm_thoughts = [
        ("Research destinations in Europe", "research", 5, ["travel", "destinations"]),
        ("Check passport expiration dates", "admin", 5, ["documents", "travel"]),
        ("Set vacation budget", "planning", 5, ["budget", "finances"]),
        ("Book flights early for better prices", "booking", 4, ["flights", "savings"]),
        ("Research local customs and etiquette", "research", 2, ["culture", "preparation"]),
        ("Learn basic phrases in local language", "preparation", 3, ["language", "communication"]),
        ("Find family-friendly accommodations", "booking", 4, ["hotels", "family"]),
        ("Plan daily itineraries", "planning", 3, ["activities", "scheduling"]),
        ("Pack appropriate clothing", "preparation", 2, ["packing", "weather"]),
        ("Arrange pet care while away", "logistics", 4, ["pets", "arrangements"])
    ]
    
    for content, category, priority, tags in brainstorm_thoughts:
        app.add_thought(content, category, priority, tags)
    
    print(f"📝 Added {len(brainstorm_thoughts)} vacation planning thoughts")
    
    # Phase 2: Mark some as completed (simulating progress)
    completed_tasks = ["Check passport expiration dates", "Set vacation budget", "Research destinations in Europe"]
    for thought in app.current_session.thoughts:
        if thought.content in completed_tasks:
            app.complete_thought(thought.id)
            print(f"✅ Completed: {thought.content}")
    
    # Export the vacation plan
    app.export_session(format="txt")
    app.save_data()
    
    print("📄 Vacation planning session exported and saved!")
    print("🌴 Ready for an amazing European adventure!")

if __name__ == "__main__":
    try:
        run_demo()
        
        # Ask if user wants to see the workflow demo too
        print("\n❓ Would you like to see a bonus workflow demonstration?")
        response = input("Enter 'y' for yes, any other key to exit: ").lower().strip()
        
        if response == 'y':
            create_sample_workflow()
            
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for checking out Python Thinker!")
    except Exception as e:
        print(f"\n❌ An error occurred during the demo: {e}")
        print("This is just a demonstration - the actual app is very stable!")
