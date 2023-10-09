"""
This module is used to fetch answers for the questions asked by user.
It takes the question as input and processes it over the vector database to figure out the answer.
"""

import os
import logging
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.callbacks import get_openai_callback
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

logger = logging.getLogger(__name__)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]

class Chatbot:
    """
    Class is used to define functions that will help in question answering for the chatbot.
    """

    def __init__(self) -> None:
        # Initialize the constants and env variables

        self._db_name = "ops-bot"
        self._embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self._llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        # TODO: to implement memory for the bot
        # memory = ConversationBufferMemory(
        #     memory_key="chat_history",
        #     return_messages=True,
        # )

        # Initialize pinecone
        pinecone.init(
            api_key=PINECONE_API_KEY,
            environment="us-central1-gcp",
        )

        # Setup the retrieval model that will be used to find answers
        _vector_store = Pinecone.from_existing_index(self._db_name, self._embeddings)
        _retriever = _vector_store.as_retriever(search_type="similarity")


        _qa_chain = load_qa_with_sources_chain(
            llm=self._llm,
            chain_type="map_rerank",
            verbose=False,
        )

        self._qa_model = RetrievalQAWithSourcesChain(
            combine_documents_chain=_qa_chain, 
            retriever=_retriever,
            return_source_documents=False
        )

    def find_answer_for_question(self, question: str, hide_token_details: bool = True):
        """
        This function is used to find the answer from the vector database.
        Args:
            - `question` (str): Query asked by the user
            - `hide_token_details` (boolean) : flag to show additional details about the process
        """
        if hide_token_details:
            answer = "I don't know the answer based on the provided information."
            try:
                result = self._qa_model({"question": question})
                split_result = result.get("answer").split("\n", 1)

                if split_result[0] != '':
                    answer = split_result[0]
                if len(split_result)>1:
                    source = split_result[1]
                    print(source)
            except Exception as e:
                if isinstance(e) == ValueError and e.args[0] == "Could not parse output: I don't know.":
                    logger.exception(e, "Unable to find out answer")

            return answer

        with get_openai_callback() as cb:
            result = self._qa_model({"question": question})
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")
            print(result)
            return result.get("answer")



class UploadDocuments:
    """
    Class is used to upload the documents. It first converts the file into vector firmat and 
    then uploads the vector to the Pincone Index. 
    This vector is later used to figure out answers for questions asked by users.
    """

    def __init__(self) -> None:
        self._db_name = "ops-bot"
        self._embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)


    def add_documents_to_existing_index(self, path):
        """
        This function is used t add additional documents to the existing vector database
        It converts the documents into vectors and uploads it to the pinecone database

        Args:
         - `path` : Location of the documents in local (Currently, it does not support urls)
        """

        # Combine multiple documents into one and Split based on character
        loader = DirectoryLoader(path)
        docs = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=50)
        texts = text_splitter.split_documents(docs)
        index = pinecone.Index(self._db_name)
        vectorstore = Pinecone(
            index=index,
            text_key="text",
            embedding=self._embeddings.embed_query
        )

        # Add additional texts to the vector database
        response = vectorstore.add_texts(texts)

        print(response)
