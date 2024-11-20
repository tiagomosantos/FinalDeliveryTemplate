from typing import Type
from pydantic import BaseModel
from langchain.tools import BaseTool
import sqlite3
from langchain_openai import ChatOpenAI
from company_name.chatbot.chains.chain1 import Chain1
from company_name.data.loader import get_sqlite_database_path


class CreateOrderInput(BaseModel):
    customer_id: int
    customer_input: str


class Tool1(BaseTool):
    name: str = "CreateOrderTool"  # This should only contain letters
    description: str = "Create a new order in the e-commerce database"
    args_schema: Type[BaseModel] = CreateOrderInput
    return_direct: bool = True

    def _run(
        self,
        customer_id: int,
        customer_input: str,
    ) -> str:
        llm = ChatOpenAI(model="gpt-4o-mini")
        db_path = get_sqlite_database_path()
        order_info = Chain1(llm, db_path).invoke(
            {"customer_input": customer_input}
        )

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT product_id, price FROM products WHERE name = ?",
                (order_info.product_name,),
            )
            product_id, price = cursor.fetchone()

            total_amount = price * order_info.quantity
            order_date = "2023-05-01"
            quantity = order_info.quantity

            cursor.execute(
                "INSERT INTO orders (customer_id, product_id, quantity, total_amount, order_date) VALUES (?, ?, ?, ?, ?)",
                (customer_id, product_id, quantity, total_amount, order_date),
            )
            connection.commit()

            id = cursor.lastrowid
        except sqlite3.OperationalError as e:
            print(f"Error: {e}")
            return "An error occurred while creating the order."
        finally:
            cursor.close()
            connection.close()

        return f"Order created with ID: {id}"
