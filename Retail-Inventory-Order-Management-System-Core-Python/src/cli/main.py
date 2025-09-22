# # src/cli/main.py
# import argparse
# import json
# from src.services import product_service
# #order_service
# from src.dao import product_dao
# #customer_dao
 
# def cmd_product_add(args):
#     try:
#         p = product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
#         print("Created product:")
#         print(json.dumps(p, indent=2, default=str))
#     except Exception as e:
#         print("Error:", e)
 
# def cmd_product_list(args):
#     ps = product_dao.list_products(limit=100)
#     print(json.dumps(ps, indent=2, default=str))
 
# # def cmd_customer_add(args):
# #     try:
# #         c = customer_dao.create_customer(args.name, args.email, args.phone, args.city)
# #         print("Created customer:")
# #         print(json.dumps(c, indent=2, default=str))
# #     except Exception as e:
# #         print("Error:", e)
 
# # def cmd_order_create(args):
# #     # items provided as prod_id:qty strings
# #     items = []
# #     for item in args.item:
# #         try:
# #             pid, qty = item.split(":")
# #             items.append({"prod_id": int(pid), "quantity": int(qty)})
# #         except Exception:
# #             print("Invalid item format:", item)
# #             return
# #     try:
# #         ord = order_service.create_order(args.customer, items)
# #         print("Order created:")
# #         print(json.dumps(ord, indent=2, default=str))
# #     except Exception as e:
# #         print("Error:", e)
 
# # def cmd_order_show(args):
# #     try:
# #         o = order_service.get_order_details(args.order)
# #         print(json.dumps(o, indent=2, default=str))
# #     except Exception as e:
# #         print("Error:", e)
 
# # def cmd_order_cancel(args):
# #     try:
# #         o = order_service.cancel_order(args.order)
# #         print("Order cancelled (updated):")
# #         print(json.dumps(o, indent=2, default=str))
# #     except Exception as e:
# #         print("Error:", e)
 
# def build_parser():
#     parser = argparse.ArgumentParser(prog="retail-cli")
#     sub = parser.add_subparsers(dest="cmd")
 
#     # product add/list
#     p_prod = sub.add_parser("product", help="product commands")
#     pprod_sub = p_prod.add_subparsers(dest="action")
#     addp = pprod_sub.add_parser("add")
#     addp.add_argument("--name", required=True)
#     addp.add_argument("--sku", required=True)
#     addp.add_argument("--price", type=float, required=True)
#     addp.add_argument("--stock", type=int, default=0)
#     addp.add_argument("--category", default=None)
#     addp.set_defaults(func=cmd_product_add)
 
#     listp = pprod_sub.add_parser("list")
#     listp.set_defaults(func=cmd_product_list)
 
#     # customer add
#     # pcust = sub.add_parser("customer")
#     # pcust_sub = pcust.add_subparsers(dest="action")
#     # addc = pcust_sub.add_parser("add")
#     # addc.add_argument("--name", required=True)
#     # addc.add_argument("--email", required=True)
#     # addc.add_argument("--phone", required=True)
#     # addc.add_argument("--city", default=None)
#     #addc.set_defaults(func=cmd_customer_add)
 
#     # order
#     # porder = sub.add_parser("order")
#     # porder_sub = porder.add_subparsers(dest="action")
 
#     # createo = porder_sub.add_parser("create")
#     # createo.add_argument("--customer", type=int, required=True)
#     # createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
#     # createo.set_defaults(func=cmd_order_create)
 
#     # showo = porder_sub.add_parser("show")
#     # showo.add_argument("--order", type=int, required=True)
#     # showo.set_defaults(func=cmd_order_show)
 
#     # cano = porder_sub.add_parser("cancel")
#     # cano.add_argument("--order", type=int, required=True)
#     # cano.set_defaults(func=cmd_order_cancel)
 
#     return parser#
 
# def main():
#     parser = build_parser()
#     args = parser.parse_args()
#     if not hasattr(args, "func"):
#         parser.print_help()
#         return
#     args.func(args)
 
# if __name__ == "__main__":
#     main()
# -----------------------------------------------------------------------------
import argparse
import json
from src.dao.product_dao import ProductDAO
from src.services.product_service import ProductService
from src.dao.customer_dao import CustomerDAO
from src.services.customer_service import CustomerService
from src.dao.order_dao import OrderDAO
from src.services.order_service import OrderService


class RetailCLI:
    def __init__(self):
        self.product_service = ProductService(ProductDAO())
        self.customer_service = CustomerService(CustomerDAO())
        self.order_service = OrderService(OrderDAO(), CustomerDAO(), ProductDAO())

    # ----------------- PRODUCTS -----------------
    def cmd_product_add(self, args):
        try:
            p = self.product_service.add_product(
                args.name, args.sku, args.price, args.stock, args.category
            )
            print(json.dumps(p, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_product_list(self, args):
        ps = self.product_service.dao.list_products(limit=100)
        print(json.dumps(ps, indent=2, default=str))

    # ----------------- CUSTOMERS -----------------
    def cmd_customer_add(self, args):
        try:
            c = self.customer_service.add_customer(
                args.name, args.email, args.phone, args.city
            )
            print(json.dumps(c, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_customer_update(self, args):
        try:
            c = self.customer_service.update_customer(args.id, args.phone, args.city)
            print(json.dumps(c, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_customer_delete(self, args):
        try:
            c = self.customer_service.delete_customer(args.id)
            print("Deleted:", json.dumps(c, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_customer_list(self, args):
        cs = self.customer_service.list_customers()
        print(json.dumps(cs, indent=2, default=str))

    def cmd_customer_search(self, args):
        try:
            if args.email:
                c = self.customer_service.search_by_email(args.email)
                print(json.dumps(c, indent=2, default=str))
            elif args.city:
                cs = self.customer_service.search_by_city(args.city)
                print(json.dumps(cs, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    # ----------------- ORDERS -----------------
    def cmd_order_create(self, args):
        try:
            items = []
            for item in args.item:
                pid, qty = item.split(":")
                items.append({"prod_id": int(pid), "quantity": int(qty)})
            o = self.order_service.create_order(args.customer, items)
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_order_show(self, args):
        try:
            o = self.order_service.get_order_details(args.id)
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_order_list(self, args):
        try:
            os = self.order_service.list_orders_by_customer(args.customer)
            print(json.dumps(os, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_order_cancel(self, args):
        try:
            o = self.order_service.cancel_order(args.id)
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_order_complete(self, args):
        try:
            o = self.order_service.complete_order(args.id)
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    # ----------------- ARG PARSER -----------------
    def build_parser(self):
        parser = argparse.ArgumentParser(prog="retail-cli")
        sub = parser.add_subparsers(dest="cmd")

        # PRODUCTS
        p_prod = sub.add_parser("product", help="product commands")
        pprod_sub = p_prod.add_subparsers(dest="action")

        addp = pprod_sub.add_parser("add")
        addp.add_argument("--name", required=True)
        addp.add_argument("--sku", required=True)
        addp.add_argument("--price", type=float, required=True)
        addp.add_argument("--stock", type=int, default=0)
        addp.add_argument("--category", default=None)
        addp.set_defaults(func=self.cmd_product_add)

        listp = pprod_sub.add_parser("list")
        listp.set_defaults(func=self.cmd_product_list)

        # CUSTOMERS
        p_cust = sub.add_parser("customer", help="customer commands")
        pcust_sub = p_cust.add_subparsers(dest="action")

        addc = pcust_sub.add_parser("add")
        addc.add_argument("--name", required=True)
        addc.add_argument("--email", required=True)
        addc.add_argument("--phone", required=True)
        addc.add_argument("--city", required=True)
        addc.set_defaults(func=self.cmd_customer_add)

        updatec = pcust_sub.add_parser("update")
        updatec.add_argument("--id", type=int, required=True)
        updatec.add_argument("--phone")
        updatec.add_argument("--city")
        updatec.set_defaults(func=self.cmd_customer_update)

        deletec = pcust_sub.add_parser("delete")
        deletec.add_argument("--id", type=int, required=True)
        deletec.set_defaults(func=self.cmd_customer_delete)

        listc = pcust_sub.add_parser("list")
        listc.set_defaults(func=self.cmd_customer_list)

        searchc = pcust_sub.add_parser("search")
        searchc.add_argument("--email")
        searchc.add_argument("--city")
        searchc.set_defaults(func=self.cmd_customer_search)

        # ORDERS
        p_order = sub.add_parser("order", help="order commands")
        porder_sub = p_order.add_subparsers(dest="action")

        createo = porder_sub.add_parser("create")
        createo.add_argument("--customer", type=int, required=True)
        createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty")
        createo.set_defaults(func=self.cmd_order_create)

        showo = porder_sub.add_parser("show")
        showo.add_argument("--id", type=int, required=True)
        showo.set_defaults(func=self.cmd_order_show)

        listo = porder_sub.add_parser("list")
        listo.add_argument("--customer", type=int, required=True)
        listo.set_defaults(func=self.cmd_order_list)

        cano = porder_sub.add_parser("cancel")
        cano.add_argument("--id", type=int, required=True)
        cano.set_defaults(func=self.cmd_order_cancel)

        completo = porder_sub.add_parser("complete")
        completo.add_argument("--id", type=int, required=True)
        completo.set_defaults(func=self.cmd_order_complete)

        return parser

    def run(self):
        parser = self.build_parser()
        args = parser.parse_args()
        if not hasattr(args, "func"):
            parser.print_help()
            return
        args.func(args)


if __name__ == "__main__":
    RetailCLI().run()
