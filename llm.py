import ollama

stream = ollama.chat(
    model='llama3',
    messages=[{'role': 'user', 'content': 'answer in the same language as the question: एसी गैस रिकवरी के लिए मैनिफोल्ड गेज का उपयोग कैसे करें'}],
    stream=True,
    options = {
             "num_predict": 2048
         }
    
)



for chunk in stream:
  if len(chunk['message']['content']) > 204:
    print(chunk['message']['content'])
