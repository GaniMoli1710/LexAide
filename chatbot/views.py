# import spacy
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# # Load the SpaCy English model
# nlp = spacy.load("en_core_web_sm")



# # Example legal data (You can replace this with real legal data or train a chatbot)
# legal_data = {
#     "contract": "A contract is a legally binding agreement between two or more parties.",
#     "intellectual property": "Intellectual property refers to creations of the mind, such as inventions, designs, and literary works.",
#     # Add more key phrases and responses as needed
# }

# @csrf_exempt
# # Chatbot view
# def chatbot_view(request):
#     if request.method == "POST":
#         user_input = request.POST.get('user_input', '')
        
#         # Process the user input with SpaCy to extract key phrases
#         doc = nlp(user_input.lower())
        
#         # Try to find a matching response based on key phrases
#         response = "Sorry, I do not have information on that."
#         for token in doc:
#             if token.lemma_ in legal_data:  # Use the lemma to match with keys in legal_data
#                 response = legal_data[token.lemma_]
#                 break  # Stop after finding the first matching response
        
#         return JsonResponse({"response": response})
    
#     return render(request, 'chatbot/chat_interface.html')

from django.shortcuts import render
from django.http import JsonResponse
from transformers import pipeline
from django.views.decorators.csrf import csrf_exempt

# Initialize the Hugging Face question answering model
qa_pipeline = pipeline("question-answering")

# Define the legal context (This can be expanded to include more data)
legal_context = """
    A contract is an agreement between two or more parties that is enforceable by law.
    Intellectual property includes patents, trademarks, copyrights, and trade secrets.
    Criminal law pertains to acts that are offenses against the state or public.
    Civil law deals with rights and obligations between individuals, such as family law or tort cases.
"""

@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        # Get the user input (question)
        user_input = request.POST.get('user_input', '')

        if user_input:
            # Get the answer from the model using the context
            result = qa_pipeline({
                'context': legal_context,
                'question': user_input
            })

            # Return the answer from the model
            response = result['answer']
        else:
            response = "Please ask a legal question."

        # Send back the response as JSON
        return JsonResponse({"response": response})

    # If it's a GET request, render the chatbot interface
    return render(request, 'chatbot/chat_interface.html')
