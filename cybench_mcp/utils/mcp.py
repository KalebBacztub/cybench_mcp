from typing import List, Dict

class MCPConversation:
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt.strip()
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def add_user_message(self, user_text: str, metadata: Dict = None):
        content = user_text
        if metadata:
            meta_str = " | Metadata: " + ", ".join(f"{k}={v}" for k, v in metadata.items())
            content += meta_str
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, assistant_text: str):
        self.messages.append({"role": "assistant", "content": assistant_text})

    def get_context(self) -> List[Dict]:
        return self.messages

    def reset(self):
        self.messages = [{"role": "system", "content": self.system_prompt}]
