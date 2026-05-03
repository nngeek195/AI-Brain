import os
import json
import httpx
from openai import OpenAI
from dotenv import load_dotenv

# 1. Setup Environment
load_dotenv()
# Properly fetching from .env without the literal '$' symbol
api_key = os.getenv("NVIDIA_API_KEY") 

if not api_key:
    print("❌ ERROR: NVIDIA_API_KEY not found in environment.")
    exit()

# 2. Connection Logic: Using a 60s timeout for deep reasoning tasks
http_client = httpx.Client(timeout=60.0)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key,
    http_client=http_client
)

class States:
    INITIAL_INPUT = "INITIAL"
    SUBSYSTEM_REVIEW = "REVIEW"
    DEEP_DIVE = "DEEP_DIVE"
    FINAL_CONFIRMATION = "FINAL_CONFIRM"
    SELECTION = "SELECT_FIRST_PART"

class P6AI_Orchestrator:
    def __init__(self):
        self.state_path = "database/project_state.json"
        self.current_state = States.INITIAL_INPUT
        self.load_state()
        print("\n" + "="*50)
        print("--- P6AI: SYNTHETIC ENGINEERING LAB ACTIVE ---")
        print("Brain: Seed-OSS-36B-Instruct (NVIDIA NIM)")
        print("Protocol: Basement Logic v2.0")
        print("="*50 + "\n")

    def load_state(self):
        os.makedirs("database", exist_ok=True)
        if not os.path.exists(self.state_path):
            initial_data = {
                "project_name": "New_Project",
                "subsystems": "",
                "deep_dive_data": "",
                "history": [],
                "current_step": States.INITIAL_INPUT
            }
            with open(self.state_path, "w") as f:
                json.dump(initial_data, f, indent=4)
        
        with open(self.state_path, "r") as f:
            self.state_data = json.load(f)

    def save_state(self):
        with open(self.state_path, "w") as f:
            json.dump(self.state_data, f, indent=4)

    def get_brain_response(self, prompt, system_instruction):
        print("\n🧠 Seed-OSS is thinking (Budget: Unlimited)...")
        print("-" * 30)
        
        try:
            completion = client.chat.completions.create(
                model="bytedance/seed-oss-36b-instruct",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                temperature=1.1,
                top_p=0.95,
                max_tokens=4096,
                stream=True,
                extra_body={
                    "thinking_budget": -1 # Allowing the model maximum reasoning depth
                }
            )

            full_response = ""
            for chunk in completion:
                # Capture reasoning content (Internal Monologue)
                reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
                if reasoning:
                    # Printed in grey to distinguish from final output
                    print(f"\033[90m{reasoning}\033[0m", end="", flush=True) 
                
                # Capture final output
                content = chunk.choices[0].delta.content
                if content is not None:
                    print(content, end="", flush=True)
                    full_response += content
            
            print("\n" + "-" * 30)
            return full_response
        except Exception as e:
            print(f"\n❌ BRAIN ERROR: {e}")
            return None

    def run_lab(self):
        while True:
            # STEP 1: INITIAL INPUT
            if self.current_state == States.INITIAL_INPUT:
                user_input = input("\n[USER]: What do you want to build today? ")
                if not user_input: continue
                
                self.state_data["project_name"] = user_input.replace(" ", "_")
                sys_msg = "You are a Lead Systems Architect. Break this into 3-5 technical subsystems."
                response = self.get_brain_response(user_input, sys_msg)
                
                if response:
                    self.state_data["subsystems"] = response
                    self.current_state = States.SUBSYSTEM_REVIEW

            # STEP 2 & 3: SUBSYSTEM REVIEW & OPINION
            elif self.current_state == States.SUBSYSTEM_REVIEW:
                print("\n[SYSTEM]: Review the subsystems identified above.")
                opinion = input("[USER]: What is your opinion? (Type 'OK' to proceed or provide feedback): ")
                
                if opinion.upper() == "OK":
                    self.current_state = States.DEEP_DIVE
                else:
                    # CLARIFICATION LOOP
                    sys_msg = "The user has feedback. Re-verify and clarify the subsystem architecture."
                    response = self.get_brain_response(opinion, sys_msg)
                    self.state_data["subsystems"] = response

            # STEP 4: DEEP DIVE (PHYISCS & INTERCONNECTION)
            elif self.current_state == States.DEEP_DIVE:
                print("\n[SYSTEM]: Proceeding to Physics Deep Dive & Interconnection Audit...")
                prompt = (
                    "Describe each subsystem in detail. "
                    "List the primary Laws of Physics ($...$) and formulas governing each. "
                    "Explain the physical and logical interconnections between them."
                )
                sys_msg = "You are a Senior Physics Engineer. Use LaTeX for formulas."
                response = self.get_brain_response(prompt, sys_msg)
                
                if response:
                    self.state_data["deep_dive_data"] = response
                    self.current_state = States.FINAL_CONFIRMATION

            # STEP 5: FINAL CLARIFICATION
            elif self.current_state == States.FINAL_CONFIRMATION:
                print("\n[SYSTEM]: Descriptions, Physics, and Interconnections are ready.")
                final_q = input("[USER]: Any final clarifications? (Type 'NONE' to finalize): ")
                
                if final_q.upper() == "NONE":
                    self.save_state()
                    self.current_state = States.SELECTION
                else:
                    sys_msg = "Clarify the user's specific doubt until they are satisfied."
                    response = self.get_brain_response(final_q, sys_msg)

            # STEP 6: SELECTION
            elif self.current_state == States.SELECTION:
                selection = input("\n[USER]: All systems locked. Which subsystem do we build first? ")
                print(f"🚀 Initializing design phase for: {selection}")
                self.state_data["history"].append({"action": "locked_architecture", "start_node": selection})
                self.save_state()
                break

if __name__ == "__main__":
    lab = P6AI_Orchestrator()
    lab.run_lab()