from datetime import datetime


class PaymentFormatter:
    def __init__(self, payment, owner, line_width):
        self.payment = payment
        self.owner = owner
        self.line_width = line_width

    def format_item(self, name, price, product_quantity, product_total, is_last):
        lines = [
            f"кількість {product_quantity:.2f}",
            f"ціна {price:.2f}",
            f"товар {name}",
            f"вартість {product_total:.2f}"
        ]
        if not is_last:
            lines.append("-" * self.line_width)
        return "\n".join(lines)

    def format_receipt(self):
        date_obj = datetime.fromisoformat(str(self.payment.created_at))
        lines = [
            f"ФОП {self.owner.fop_title}".center(self.line_width),
            "=" * self.line_width,
            *[
                self.format_item(
                    prod.name,
                    prod.price_per_unit,
                    prod.quantity if prod.quantity is not None else prod.weight,
                    prod.product_total,
                    is_last=(i == len(self.payment.products) - 1)
                )
                for i, prod in enumerate(self.payment.products)
            ],
            "=" * self.line_width,
            f"сума {self.payment.amount:.2f}",
            f"повна вартість {self.payment.payment_total:.2f}",
            f"решта {self.payment.rest:.2f}",
            f"метод оплати {self.payment.pay_type}",
            "=" * self.line_width,
            date_obj.strftime("%d.%m.%Y %H:%M").center(self.line_width),
            "Дякуємо за покупку!".center(self.line_width),
        ]
        return "\n".join(lines)
