import requests

def translate_text(text, subscription_key, endpoint, region, to_language="en"):
    """
    Translate a given text into the specified language using Azure Translator.
    """
    # Construct the URL
    path = '/translate?api-version=3.0'
    params = f'&to={to_language}'
    constructed_url = endpoint + path + params

    # Request headers
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json'
    }

    # Request body
    body = [{'text': text}]

    # Call the API
    response = requests.post(constructed_url, headers=headers, json=body)
    result = response.json()

    try:
        # Extract the translated text
        return result[0]['translations'][0]['text']
    except (IndexError, KeyError):
        print("Translation error. Received:", result)
        return None
