import os
import requests
import openai

class TransactionHistory:
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        self.endpoint = endpoint
        self.transactions = self._load_transactions()

    def _load_transactions(self):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(self.endpoint, headers=headers)
            if response.status_code == 200:
                return response.json().get("transactions", [])
            else:
                raise Exception(f"Failed to retrieve transactions: {response.text}")
        except requests.RequestException as e:
            raise Exception(f"API error: {str(e)}")

    def search(self, criteria):
        # In a real-world application, you'd use a more sophisticated method to filter transactions
        # based on the criteria. This is a basic mock method.
        return [transaction for transaction in self.transactions if criteria in transaction["description"].lower()]

class OpenAIInterface:
    def __init__(self, transaction_history):
        self.transaction_history = transaction_history

    def answer_question(self, user_input):
        # Use OpenAI to interpret the user_input
        interpretation = self._interpret_with_openai(user_input)

        # Use the interpretation to probe the transaction history
        relevant_transactions = self.transaction_history.search(interpretation)

        # Generate a relevant response based on the retrieved transactions
        # For simplicity, we return the first matching transaction description.
        # In a real-world scenario, you'd formulate a more comprehensive answer.
        if relevant_transactions:
            return f"I found a transaction: {relevant_transactions[0]['description']}."
        else:
            return "I couldn't find any relevant transactions."

    def _interpret_with_openai(self, user_input):
        # This is a mock method. In reality, you'd use OpenAI's capabilities to understand user input.
        # For this demonstration, we assume the interpretation is a keyword or key phrase to search
        # within transaction descriptions.
        return user_input.lower()  # Mock interpretation

def main():
    # Load API credentials from environment variables
    mastercard_api_key = os.environ.get("MASTERCARD_API_KEY")
    mastercard_endpoint = os.environ.get("MASTERCARD_API_ENDPOINT")

    # Initialize the TransactionHistory and OpenAIInterface
    transaction_history = TransactionHistory(mastercard_api_key, mastercard_endpoint)
    ai_interface = OpenAIInterface(transaction_history)

    while True:
        user_question = input("User: ")
        if user_question.lower() == "exit":
            break
        response = ai_interface.answer_question(user_question)
        print("AI: " + response)

if __name__ == "__main__":
    main()
