# plug-n-play-chatbot
AI Chatbot that you can easily integrate with your applicaiton

This package contains a collection of useful functions that can be used to integrate your application with a AI Chatbot that has been created using langchain.

## Prpject Setup Guidelines

1. Ensure you have Python 3.9 installed on your system. You can download the latest version of Python from the official website: <https://www.python.org/downloads/>

2. Clone the repository or download the ZIP file and extract it to a directory of your choice.

3. Open a terminal or command prompt and navigate to the directory where you extracted the package.


## Usage Guidelines

1. Setup environment variables for `OPENAI_API_KEY` and `PINECONE_API_KEY`
2. Install this package

### Find answers for questions
1. Instantiate the Chatbot class and call the function `find_answer_for_question` to get answer for your query


### To upload documents
1. Instantiate the UploadDocuments class and call the function `add_documents_to_index` to upload your documents. The questions will be answered only based on these documents.

# Flow of the library

![Flow-PnP](https://github.com/reverie-ss/plug-n-play-chatbot/assets/14177137/62c81ca2-93c7-4992-8bef-03cccb1cd7f2)
