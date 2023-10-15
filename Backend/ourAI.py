import openai
import json
import os
import dotenv

dotenv.load_dotenv()

key = os.getenv("OPENAI_API_KEY");
print(key);

openai.api_key = 'our_api_key'

class Bot:
    def __init__(self):
        self.transaction_data = '''
amount,description,postedDate,transactionDate,createdDate,categorization.normalizedPayeeName,categorization.category,categorization.bestRepresentation,categorization.country
...''' # The rest of your transaction data here

    def get_transaction_info(self):
        return self.transaction_data

    def _format_system_message(self, user_message):
        template = f'''
            You are an expert financial manager. You will help users with questions about their transactional data, based on a given CSV string. 
            User's question:
            {user_message}

            Data:
            {self.transaction_data} 

            You will respond like you are talking to them. For example: if they ask, "tell me about my transfers", you will respond with details about the transfers.
            '''
        return template

    def run_conversation(self, initial_message):
        system_message = self._format_system_message(initial_message)
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": initial_message}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )

        response_content = response.choices[0].message["content"]

        if "get_transaction_info" in response_content:
            messages.extend([
                {"role": "assistant", "content": response_content},
                {
                    "role": "function",
                    "name": "get_transaction_info",
                    "content": self.get_transaction_info()
                }
            ])
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
            )
            return second_response.choices[0].message["content"]

        return response_content