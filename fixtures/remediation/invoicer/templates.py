import html

REPORT_ROW = "<tr><td>{customer}</td><td>{amount}</td><td>{created}</td></tr>"
REPORT_PAGE = "<table><thead><tr><th>Customer</th><th>Amount</th><th>Created</th></tr></thead><tbody>{rows}</tbody></table>"


def render_report(rows):
    body = "".join(
        REPORT_ROW.format(
            customer=html.escape(r["customer"]),
            amount="{:.2f}".format(r["amount_cents"] / 100),
            created=html.escape(r["created"]),
        )
        for r in rows
    )
    return REPORT_PAGE.format(rows=body)
