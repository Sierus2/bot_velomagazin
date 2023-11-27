from datetime import datetime
import datetime


class Request:
    def __init__(self, conn):
        self.conn = conn

    async def db_get_categories(self):
        query = "SELECT DISTINCT category FROM table_market ORDER BY category ASC"

        rows = await self.conn.execute(query)
        results = await rows.fetchall()
        lst = [result[0] for result in results]
        return lst

    async def db_get_subcategories(self, category):
        query = f"SELECT DISTINCT subcategory FROM table_market WHERE category='{category}' ORDER BY subcategory ASC"

        rows = await self.conn.execute(query)
        results = await rows.fetchall()
        lst = [result[0] for result in results]
        return lst

    async def db_get_items(self, category, subcategory):
        rows = await self.conn.execute(
            f"SELECT product, price FROM table_market WHERE category='{category}' AND subcategory ='{subcategory}'")
        result = await rows.fetchall()
        return result

    async def db_get_description(self, product, category, subcategory):
        sql = f"SELECT product, price FROM table_market WHERE category='{category}' AND subcategory ='{subcategory}' AND product='{product}'"
        rows = await self.conn.execute(
            f"SELECT product, price FROM table_market WHERE category='{category}' AND subcategory ='{subcategory}' AND product='{product}'")

        results = await rows.fetchone()
        return results
