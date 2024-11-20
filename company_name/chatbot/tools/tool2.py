from typing import Type
from pydantic import BaseModel
from langchain.tools import BaseTool
import sqlite3
from langchain_openai import ChatOpenAI
from company_name.chatbot.chains.chain2 import Chain2
from company_name.data.loader import get_sqlite_database_path


class GetOrderInput(BaseModel):
    customer_id: int
    customer_input: str


class Tool2(BaseTool):
    name: str = "GetOrderTool"
    description: str = "Retrieve details of an existing order based on the order ID"
    args_schema: Type[BaseModel] = GetOrderInput
    return_direct: bool = True

    def _run(
        self,
        customer_id: int,
        customer_input: str,
    ) -> str:
        llm = ChatOpenAI(model="gpt-4o-mini")

        order_info = Chain2(llm).invoke(
            {"customer_input": customer_input}
        )
        order_id = order_info.order_id

        db_path = get_sqlite_database_path()

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        try:
            # Get the column names of the orders table
            cursor.execute("PRAGMA table_info(orders)")
            columns = cursor.fetchall()

            cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
            order_ = cursor.fetchone()

            # Map the order to the column names
            order = dict(zip([column[1] for column in columns], order_))
        except sqlite3.OperationalError as e:
            print(f"Error: {e}")
            return "An error occurred while retrieving the order."
        finally:
            cursor.close()
            connection.close()

        if customer_id != order["customer_id"]:
            return "You are not authorized to view this order."
        else:
            return order
