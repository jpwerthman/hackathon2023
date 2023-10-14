import openai
import json
import os

openai.api_key = "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"

class Bot:
    def __init__(self):
        self.available_functions = {
            "get_transaction_info": self.get_transaction_info,
        }
        self.transaction_data = {
            "12345": {
                "balance": "$1000",
                "recent_transactions": {
                    "deposit": ["$200 on 12-Oct", "$50 on 10-Oct"],
                    "withdrawal": ["$50 on 09-Oct"],
                    "all": ["$200 deposit on 12-Oct", "$50 deposit on 10-Oct", "$50 withdrawal on 09-Oct"]
                }
            }
        }

    def get_transaction_info(self, account_number, transaction_type="all"):
        account_data = self.transaction_data.get(account_number)
        if not account_data:
            return json.dumps({"error": "Account not found."})

        return json.dumps({
            "balance": account_data["balance"],
            "recent_transactions": account_data["recent_transactions"][transaction_type]
        })

    def run_conversation(self, initial_message):
        messages = [{"role": "user", "content": initial_message}]
        functions = [
            {
                "name": "get_transaction_info",
                "description": "Get the transaction data for a given account number",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_number": {
                            "type": "string",
                            "description": "The account number to fetch transactions for"
                        },
                        "transaction_type": {
                            "type": "string",
                            "enum": ["deposit", "withdrawal", "all"]
                        },
                    },
                    "required": ["account_number"],
                },
            }
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto",
        )

        response_message = response["choices"][0]["message"]
        if response_message.get("function_call"):
            function_name = response_message["function_call"]["name"]
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = self.available_functions[function_name](
                **function_args
            )

            messages.extend([
                response_message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            ])
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
            )
            return second_response["choices"][0]["message"]["content"]
        else:
            return response_message["content"]
