import uuid
from dataclasses import dataclass

from langchain.retrievers import MultiQueryRetriever
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import VectorStore
from app.ai.dto.ai_schema import LLMResponse
from app.file.service.file_service import FileService

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        ("system", "{data}"),
        ("human", "{text}"),
    ]
)

query_prompt = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant and an expert extraction algorithm. Your task is to generate five
        different versions of the given user question to retrieve and extract relevant documents and information from
        a vector database. By generating multiple perspectives on the user question, your
        goal is to help the user overcome some of the limitations of the distance-based
        similarity search. Provide these alternative questions separated by newlines.
        Original question: {question}""",
)

template = """Answer the question should be short, only to the point, without any additional information and only based ONLY on the following context:
    {context}
    Question: {question}
    """

@dataclass
class AIService:
    def __init__(self, llm: BaseChatModel, vector_store: VectorStore, file_service: FileService):
        self.llm_original = llm
        self.llm = llm.with_structured_output(schema=LLMResponse)
        self.db = vector_store
        self.file_service = file_service

    async def query_alternative(self, query: str, chat_id: uuid.UUID) -> str | None:
        documents = await self.file_service.search_documents(query=query, chat_id=chat_id)
        data = "\n\n".join(doc.page_content for doc in documents)
        prompt = prompt_template.invoke({"text": query, "data": data})
        llm_result = await self.llm.ainvoke(prompt)

        return LLMResponse.model_validate(llm_result).answer if llm_result else None

    async def query(self, query: str, chat_id: uuid.UUID) -> str | None:
        prompt =  ChatPromptTemplate.from_template(template)
        file_ids = await self.file_service.find_files_ids(chat_id=chat_id)
        base_retriever = self.db.as_retriever(
            search_kwargs={
                "filter": {"file_id": {"$in": file_ids}},
                "k": 10
            }
        )
        retriever = MultiQueryRetriever.from_llm(
            base_retriever,
            self.llm_original,
            prompt=query_prompt,
        )

        chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | self.llm_original
                | StrOutputParser()
        )

        response = await chain.ainvoke(query)

        return response

