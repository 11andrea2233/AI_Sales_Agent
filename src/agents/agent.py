from colorama import Fore, init
from litellm import completion
import time
from litellm.exceptions import RateLimitError

# Initialize colorama for colored terminal output
init(autoreset=True)

class Agent:
    """
    @title AI Agent Class
    @notice This class defines an AI agent that can uses function calling to interact with tools and generate responses.
    """

    def __init__(self, name, model, tools=None, system_prompt=""):
        """
        @notice Initializes the Agent class.
        @param model The AI model to be used for generating responses.
        @param tools A list of tools that the agent can use.
        @param available_tools A dictionary of available tools and their corresponding functions.
        @param system_prompt system prompt for agent behaviour.
        """
        self.name = name
        self.model = model
        self.messages = []
        self.tools = tools if tools is not None else []
        self.tools_schemas = self.get_openai_tools_schema() if self.tools else None
        self.system_prompt = system_prompt
        if self.system_prompt and not self.messages:
            self.handle_messages_history("system", self.system_prompt)

    def invoke(self, message):
        print(Fore.GREEN + f"\nCalling Agent: {self.name}")
        self.handle_messages_history("user", message)
        result = self.execute()
        return result

    def execute(self):
        """
        @notice Use LLM to generate a response and handle tool calls if needed.
        @return The final response.
        """
        # First, call the AI to get a response
        response_message = self.call_llm()

        # Check if there are tool calls in the response
        tool_calls = response_message.tool_calls

        # If there are tool calls, invoke them
        if tool_calls:
            response_message = self.run_tools(tool_calls)
            
        return response_message.content

    def run_tools(self, tool_calls):
        """
        @notice Runs the necessary tools based on the tool calls from the LLM response.
        @param tool_calls The list of tool calls from the LLM response.
        @return The final response from the LLM after processing tool calls.
        """
        # For each tool the AI wanted to call, call it and add the tool result to the list of messages
        for tool_call in tool_calls:
            self.execute_tool(tool_call)

        # Call the AI again so it can produce a response with the result of calling the tool(s)
        response_message = self.call_llm()
        tool_calls = response_message.tool_calls

        # If the AI decided to invoke a tool again, invoke it
        if tool_calls:
            response_message = self.run_tools(tool_calls)

        return response_message

    def execute_tool(self, tool_call):
        """
        @notice Executes a tool based on the tool call from the LLM response.
        @param tool_call The tool call from the LLM response.
        @return The final response from the LLM after executing the tool.
        """
        function_name = tool_call.function.name
        func = next(
            iter([func for func in self.tools if func.__name__ == function_name])
        )

        if not func:
            return f"Error: Function {function_name} not found. Available functions: {[func.__name__ for func in self.tools]}"

        try:
            print(Fore.GREEN + f"\nCalling Tool: {function_name}")
            
            # Get arguments from the tool call
            try:
                args = eval(tool_call.function.arguments) if tool_call.function.arguments else {}
            except:
                args = {}
            
            # Define default arguments for each tool
            default_args = {
                "GetProductRecommendation": {
                    "product_category": "Laptops",
                    "user_query": "Show me all gaming laptops"
                },
                "GetStoreInfo": {
                    "search_query": "Show me available products"
                },
                "GenerateCalendlyInvitationLink": {
                    "query": "Consultation"
                }
            }
            
            # Get default args for the current function
            default = default_args.get(function_name, {})
            
            # Create final arguments by combining defaults with provided args
            if function_name == "GetProductRecommendation":
                final_args = {
                    "product_category": args.get("category", default["product_category"]),
                    "user_query": args.get("description", default["user_query"])
                }
            elif function_name == "GetStoreInfo":
                final_args = {
                    "search_query": args.get("query", default["search_query"])
                }
            elif function_name == "GenerateCalendlyInvitationLink":
                final_args = {
                    "query": args.get("description", default["query"])
                }
            elif function_name == "GenerateStripePaymentLink":
                final_args = args
            else:
                final_args = args
            
            print(Fore.GREEN + f"Arguments: {final_args}\n")
            
            # Create a new instance of the tool with the final arguments
            tool_instance = func(**final_args)
            
            # Execute the tool
            output = tool_instance.run()
            
            # Create tool message without empty function_call
            tool_message = {
                "name": function_name,
                "tool_call_id": tool_call.id,
                "content": output
            }
            
            self.handle_messages_history("tool", output, tool_output=tool_message)
            
            return output
        except Exception as e:
            print("Error: ", str(e))
            return "Error: " + str(e)

    def call_llm(self):
        max_retries = 5
        initial_retry_delay = 30
        
        # Convert tools to the correct format
        formatted_tools = []
        for tool in self.tools:
            if hasattr(tool, 'to_dict'):
                formatted_tools.append(tool.to_dict())
            else:
                tool_dict = {
                    "type": "function",
                    "function": {
                        "name": tool.__name__,
                        "description": tool.__doc__ or "",
                        "parameters": getattr(tool, "parameters", {})
                    }
                }
                formatted_tools.append(tool_dict)

        for attempt in range(max_retries):
            try:
                response = completion(
                    model="gpt-3.5-turbo",
                    messages=[
                        # Only include essential fields in messages
                        {
                            "role": msg["role"],
                            "content": msg["content"],
                            **({"tool_calls": msg["tool_calls"]} if msg.get("tool_calls") else {}),
                            **({"name": msg["name"]} if msg.get("name") else {}),
                            **({"tool_call_id": msg["tool_call_id"]} if msg.get("tool_call_id") else {})
                        }
                        for msg in self.messages
                    ],
                    tools=formatted_tools,
                    temperature=0.1
                )
                message = response.choices[0].message
                self.handle_messages_history(
                    "assistant",
                    message.content,
                    tool_calls=message.tool_calls if hasattr(message, "tool_calls") else None
                )
                return message
            except RateLimitError as e:
                retry_delay = initial_retry_delay * (2 ** attempt)
                if attempt < max_retries - 1:
                    print(f"\nRate limit reached. Waiting {retry_delay} seconds before retry {attempt + 1} of {max_retries}...")
                    time.sleep(retry_delay)
                else:
                    print("\nMax retries reached. Please try again later.")
                    raise

    def reset(self):
        self.messages = []
        if self.system_prompt:
            self.messages.append({"role": "system", "content": self.system_prompt})
            
    def get_openai_tools_schema(self):
        return [
            {"type": "function", "function": tool.openai_schema} for tool in self.tools
        ]
            
    def handle_messages_history(self, role, content, tool_calls=None, tool_output=None):
        """
        @notice Handles the message history for the agent.
        @param role The role of the message.
        @param content The content of the message.
        @param tool_calls The tool calls from the LLM response.
        @param tool_output The output from the tool.
        """
        message = {"role": role, "content": content}
        
        if role == "tool" and tool_output:
            message.update({
                "tool_call_id": tool_output.get("tool_call_id"),
                "name": tool_output.get("name")
            })
        elif role == "assistant" and tool_calls:
            message["tool_calls"] = tool_calls
        
        self.messages.append(message)

    def parse_tool_calls(self, calls):
        parsed_calls = []
        for call in calls:
            parsed_call = {
                "function": {
                    "name": call.function.name,
                    "arguments": call.function.arguments,
                },
                "id": call.id,
                "type": call.type,
            }
            parsed_calls.append(parsed_call)
        return parsed_calls