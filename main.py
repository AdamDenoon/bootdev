import os
import argparse
import sys
from dotenv import load_dotenv
import openai
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
	raise RuntimeError("Please add OPENROUTER_API_KEY to .env.")
	
client = openai.OpenAI(
	base_url="https://openrouter.ai/api/v1",
	api_key=api_key,
)

def generate_content(client, messages, verbose: bool = False):
	try:
		user_prompt = next(
			(message["content"] for message in messages if message["role"] == "user"),
			None,
		)
			
		response = client.chat.completions.create(
			model="openrouter/free",
			messages=messages,
			tools=available_functions,
		)
		if response.usage is None:
			raise RuntimeError("Could not generate a response. Wait a few minutes and try again, or explicitly set a different model.")

		if verbose:
			print(f"User prompt: {user_prompt}")
			print(f"Prompt tokens: {response.usage.prompt_tokens}")
			print(f"Response tokens: {response.usage.completion_tokens}")

		return response
	except openai.RateLimitError:
		print("Daily free-model request limit reached. Try again later or add credits.")
		return
		

def main():
	parser = argparse.ArgumentParser(description="Chatbot")
	parser.add_argument("user_prompt", type=str, help="User prompt")
	parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
	args = parser.parse_args()

	messages=[
		{ "role": "system", "content": system_prompt },
		{ "role": "user", "content": args.user_prompt },
	]

	hasFinal: bool = False;
	for _ in range(20):
		response = generate_content(client, messages, args.verbose)

		if response is None or not response.choices:
			print("Response is empty")
			continue

		message = response.choices[0].message
			
		messages.append(message.model_dump(exclude_none=True))

		if not message:
			raise ProcessLookupError("Response is empty")

		if message.tool_calls:
			for tool_call in message.tool_calls or []:
				tool_message = call_function(tool_call, verbose=args.verbose)
				messages.append(tool_message)
		else:
			print(f"Final message: {message}")
			hasFinal = True
			break

	if not hasFinal:
		print(f"Max iterations have been reached without a final answer")
		sys.exit(1)
		

if __name__ == "__main__":
    main()
