from anthropic import AI_PROMPT, HUMAN_PROMPT, AsyncAnthropic

from config import claude_api


class Claude:
    def __init__(self):
        self.model = "claude-2.1"
        self.temperature = 0.5
        self.cutoff = 75
        self.client = AsyncAnthropic(api_key=claude_api)
        self.prompt = "你需要在回答中清晰地列出逻辑推理过程和结论。分析流程应包括：明确目标、解剖问题、给出答案;在回答的最后不要总结。"

    def reset(self):
        self.prompt = "你需要在回答中清晰地列出逻辑推理过程和结论。分析流程应包括：明确目标、解剖问题、给出答案;在回答的最后不要总结。"

    def revert(self):
        self.prompt = self.prompt[: self.prompt.rfind(HUMAN_PROMPT)]

    def change_model(self, model):
        valid_models = {"claude-2.1", "claude-instant-1"}
        if model in valid_models:
            self.model = model
            return True
        return False

    def change_temperature(self, temperature):
        try:
            temperature = float(temperature)
        except ValueError:
            return False
        if 0 <= temperature <= 1:
            self.temperature = temperature
            return True
        return False

    def change_cutoff(self, cutoff):
        try:
            cutoff = int(cutoff)
        except ValueError:
            return False
        if cutoff > 0:
            self.cutoff = cutoff
            return True
        return False

    async def send_message_stream(self, message):
        self.prompt = f"{self.prompt}{HUMAN_PROMPT} {message}{AI_PROMPT}"
        response = await self.client.completions.create(
            prompt=self.prompt,
            model=self.model,
            temperature=self.temperature,
            stream=True,
            max_tokens_to_sample=100000,
        )
        answer = ""
        async for data in response:
            answer = f"{answer}{data.completion}"
            yield answer
        self.prompt = f"{self.prompt}{answer}"
