from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(gds.`Date`) as year
                    from go_daily_sales gds """
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getAllColors():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct gp.Product_color 
                        from go_products gp
                        order by gp.Product_color desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Product_color"])
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getAllNodes(color):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct gp.* 
                    from go_products gp
                    where gp.Product_color = %s """
            cursor.execute(query, (color,))

            for row in cursor:
                result.append(Product(**row))
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getAllEdges(color, year, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select gp1.Product_number as p1, gp2.Product_number as p2, count(distinct gds1.`Date`) as peso
                    from go_products gp1
                    join go_daily_sales gds1 on gds1.Product_number = gp1.Product_number 
                    join go_daily_sales gds2 on gds1.Retailer_code = gds2.Retailer_code and gds1.`Date` = gds2.`Date`
                    join go_products gp2 on gp2.Product_number = gds2.Product_number 
                    where gp1.Product_color = %s and gp2.Product_color = %s and year(gds1.`Date`) = %s and
                          year(gds2.`Date`) = %s and gp1.Product_number < gp2.Product_number 
                    group by gp1.Product_number, gp2.Product_number """
            cursor.execute(query, (color, color, year, year))

            for row in cursor:
                result.append((
                    idMap[row["p1"]],
                    idMap[row["p2"]],
                    row["peso"]
                ))
            cursor.close()
            cnx.close()
        return result
