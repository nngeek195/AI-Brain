import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# THE CRITICAL FIX: Properly load the key from the environment
api_key = os.getenv("NVIDIA_API_KEY")

if not api_key or api_key.startswith("$"):
    print("❌ ERROR: API Key failed to load. Check your .env file!")
    exit()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)


class P6AI_Orchestrator:
    def __init__(self):
        self.state_path = "database/project_state.json"
        self.load_state()
        print("--- P6AI: Synthetic Engineering Lab Active (May 2026) ---")

    def load_state(self):
        os.makedirs("database", exist_ok=True)
        if not os.path.exists(self.state_path):
            with open(self.state_path, "w") as f:
                json.dump({"project_name": "New_Project", "history": [], "components": {}, "current_step": "PLANNING"}, f)
        with open(self.state_path, "r") as f:
            self.state = json.load(f)

    def save_state(self):
        with open(self.state_path, "w") as f:
            json.dump(self.state, f, indent=4)

    def get_brain_response(self, prompt, system_instruction):
        print("\n🧠 Brain (Kimi-K2.6) is reasoning...")
        print("-" * 30)
        
        try:
            # Using the latest 2026 model ID
            stream = client.chat.completions.create(
                model="moonshotai/kimi-k2.6", 
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                extra_body={"chat_template_kwargs": {"thinking": True}}, 
                stream=True
            )

            full_response = ""
            for chunk in stream:
                if not chunk.choices:
                    continue
                # Capture reasoning traces
                reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
                if reasoning:
                    print(f"\033[90m{reasoning}\033[0m", end="", flush=True) 
                
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
                    full_response += content
            
            print("\n" + "-" * 30)
            return full_response
        except Exception as e:
            print(f"\n❌ AUTH/CONNECTION ERROR: {e}")
            return None

    def start_project(self):
        user_input = input("\n[USER]: What do you want to build today? ")
        if not user_input: return
        
        plan = self.get_brain_response(user_input, "You are a Lead Systems Architect. Break this request into 3-5 sub-components.")
        if not plan: return

        print("\n[SYSTEM]: Which module shall we design first?")
        selection = input("[USER]: Choose a module: ")
        
        self.state["project_name"] = user_input.replace(" ", "_")
        self.state["history"].append({"action": "planning", "output": plan, "selected": selection})
        self.save_state()
        print(f"✅ Logic locked for: {selection}")

if __name__ == "__main__":
    lab = P6AI_Orchestrator()
    lab.start_project()