import io
import os

from langchain import LLMChain
from langchain.chains import RetrievalQA, StuffDocumentsChain
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.weaviate import Weaviate
from unstructured.partition.pdf import partition_pdf


class FilesService:
    @staticmethod
    def _openai_streamer(retr_qa: RetrievalQA, text: str):
        yield from retr_qa.run(text)

    @staticmethod
    async def query(question, temperature, n_docs, vectorstore: Weaviate):
        llm = AzureChatOpenAI(
            deployment_name=os.environ.get("OPENAI_DEPLOYMENT_NAME"),
            openai_api_base=os.environ.get("OPENAI_API_BASE"),
            openai_api_version=os.environ.get("OPENAI_API_VERSION", "2024-02-01"),
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            streaming=True,
            temperature=temperature,
        )
        messages = [
            SystemMessage(
                content="You are a world class algorithm to answer questions related to the Programming Language \
                Python. Remember you are a  algorithm to answer questions or generate code related to the Programming \
                Language Python only. You cannot answer questions related to other topics."
            ),
            HumanMessage(
                content="Answer question using only information contained in the following context: "
            ),
            HumanMessagePromptTemplate.from_template("{context}"),
            HumanMessage(
                content="Tips: If you can't find a relevant answer in the context, then try to broaden the context and \
                  answer but dont go to beyond! If The provided context does not contain any information relevant to \
                  the question, please respond with I don't know or I can't answer this question."

            ),
            HumanMessagePromptTemplate.from_template("Question: {question}"),
        ]
        prompt = ChatPromptTemplate(messages=messages)

        qa_chain = LLMChain(llm=llm, prompt=prompt)
        doc_prompt = PromptTemplate(
            template="Content: {page_content}",
            input_variables=["page_content"],
        )
        final_qa_chain = StuffDocumentsChain(
            llm_chain=qa_chain,
            document_variable_name="context",
            document_prompt=doc_prompt,
        )
        retrieval_qa = RetrievalQA(
            retriever=vectorstore.as_retriever(search_kwargs={"k": n_docs}),
            combine_documents_chain=final_qa_chain,
        )
        return FilesService._openai_streamer(retrieval_qa, question)

    @staticmethod
    async def upload(file, chunk_size, vectorstore: Weaviate):
        data = await file.read()
        elements = partition_pdf(file=io.BytesIO(data))
        text = [ele.text for ele in elements]

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=20,
            length_function=len,
            add_start_index=True,
        )

        docs = text_splitter.create_documents(
            ["\n".join(text)], metadatas=[{"file": f"{file.filename}"}]
        )
        response = vectorstore.add_documents(docs)
        return response
