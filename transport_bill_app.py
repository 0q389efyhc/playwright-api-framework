import streamlit as st
import sqlite3
import html
from datetime import date, datetime
from pathlib import Path

DB_FILE = "transport_bills.db"


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transport_bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_no TEXT UNIQUE NOT NULL,
            bill_date TEXT NOT NULL,
            truck_no TEXT NOT NULL,
            from_location TEXT NOT NULL,
            to_location TEXT NOT NULL,
            pay_to TEXT NOT NULL,
            consignor TEXT,
            consignee TEXT,
            driver_name TEXT,
            driver_mobile TEXT,
            material TEXT,
            weight REAL DEFAULT 0,
            weight_unit TEXT DEFAULT 'MT',
            freight_rate REAL DEFAULT 0,
            freight_amount REAL DEFAULT 0,
            loading_charges REAL DEFAULT 0,
            unloading_charges REAL DEFAULT 0,
            other_charges REAL DEFAULT 0,
            advance_paid REAL DEFAULT 0,
            balance_payable REAL DEFAULT 0,
            remarks TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def generate_bill_no():
    today = datetime.now().strftime("%Y%m%d")
    conn = get_connection()
    row = conn.execute(
        "SELECT COUNT(*) AS cnt FROM transport_bills WHERE bill_no LIKE ?",
        (f"TB-{today}-%",)
    ).fetchone()
    conn.close()
    return f"TB-{today}-{int(row['cnt']) + 1:03d}"


def save_bill(data):
    conn = get_connection()

    conn.execute("""
        INSERT INTO transport_bills (
            bill_no, bill_date, truck_no, from_location, to_location,
            pay_to, consignor, consignee, driver_name, driver_mobile,
            material, weight, weight_unit, freight_rate, freight_amount,
            loading_charges, unloading_charges, other_charges,
            advance_paid, balance_payable, remarks, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["bill_no"],
        data["bill_date"],
        data["truck_no"],
        data["from_location"],
        data["to_location"],
        data["pay_to"],
        data["consignor"],
        data["consignee"],
        data["driver_name"],
        data["driver_mobile"],
        data["material"],
        data["weight"],
        data["weight_unit"],
        data["freight_rate"],
        data["freight_amount"],
        data["loading_charges"],
        data["unloading_charges"],
        data["other_charges"],
        data["advance_paid"],
        data["balance_payable"],
        data["remarks"],
        datetime.now().isoformat(timespec="seconds")
    ))

    conn.commit()
    conn.close()


def get_all_bills():
    conn = get_connection()
    rows = conn.execute("""
        SELECT id, bill_no, bill_date, truck_no, from_location,
               to_location, pay_to, weight, weight_unit,
               freight_amount, balance_payable
        FROM transport_bills
        ORDER BY id DESC
    """).fetchall()
    conn.close()
    return rows


def get_bill(bill_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM transport_bills WHERE id = ?",
        (bill_id,)
    ).fetchone()
    conn.close()
    return row


# ============================================================
# BILL HTML
# ============================================================

def money(value):
    return f"₹ {float(value):,.2f}"


def create_bill_html(bill):
    e = lambda x: html.escape(str(x or ""))

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Transport Bill - {e(bill['bill_no'])}</title>
<style>
    @page {{
        size: A4;
        margin: 12mm;
    }}

    body {{
        font-family: Arial, Helvetica, sans-serif;
        color: #111;
        margin: 0;
        background: #fff;
    }}

    .bill {{
        max-width: 900px;
        margin: 20px auto;
        border: 2px solid #222;
        padding: 22px;
    }}

    .header {{
        text-align: center;
        border-bottom: 2px solid #222;
        padding-bottom: 12px;
        margin-bottom: 15px;
    }}

    .header h1 {{
        margin: 0;
        font-size: 28px;
        letter-spacing: 1px;
    }}

    .header p {{
        margin: 5px 0 0;
        color: #555;
    }}

    .top {{
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 15px;
    }}

    .box {{
        border: 1px solid #555;
        padding: 10px;
        flex: 1;
    }}

    .label {{
        font-size: 11px;
        color: #555;
        text-transform: uppercase;
        margin-bottom: 3px;
    }}

    .value {{
        font-size: 15px;
        font-weight: bold;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
    }}

    th, td {{
        border: 1px solid #555;
        padding: 9px;
        text-align: left;
    }}

    th {{
        background: #f0f0f0;
    }}

    .right {{
        text-align: right;
    }}

    .total {{
        font-size: 17px;
        font-weight: bold;
    }}

    .footer {{
        margin-top: 30px;
        display: flex;
        justify-content: space-between;
    }}

    .signature {{
        width: 220px;
        text-align: center;
        padding-top: 45px;
        border-top: 1px solid #333;
    }}

    .remarks {{
        margin-top: 18px;
        border: 1px solid #555;
        padding: 10px;
        min-height: 50px;
    }}

    @media print {{
        .bill {{
            margin: 0;
            border: 2px solid #222;
        }}
    }}
</style>
</head>

<body>
<div class="bill">

    <div class="header">
        <h1>TRANSPORT BILL</h1>
        <p>Freight / Transportation Service Bill</p>
    </div>

    <div class="top">
        <div class="box">
            <div class="label">Bill Number</div>
            <div class="value">{e(bill['bill_no'])}</div>
        </div>

        <div class="box">
            <div class="label">Bill Date</div>
            <div class="value">{e(bill['bill_date'])}</div>
        </div>

        <div class="box">
            <div class="label">Truck Number</div>
            <div class="value">{e(bill['truck_no'])}</div>
        </div>
    </div>

    <div class="top">
        <div class="box">
            <div class="label">From</div>
            <div class="value">{e(bill['from_location'])}</div>
        </div>

        <div class="box">
            <div class="label">To</div>
            <div class="value">{e(bill['to_location'])}</div>
        </div>

        <div class="box">
            <div class="label">Pay To</div>
            <div class="value">{e(bill['pay_to'])}</div>
        </div>
    </div>

    <table>
        <tr>
            <th>Consignor</th>
            <td>{e(bill['consignor'])}</td>
            <th>Consignee</th>
            <td>{e(bill['consignee'])}</td>
        </tr>
        <tr>
            <th>Driver Name</th>
            <td>{e(bill['driver_name'])}</td>
            <th>Driver Mobile</th>
            <td>{e(bill['driver_mobile'])}</td>
        </tr>
        <tr>
            <th>Material / Goods</th>
            <td>{e(bill['material'])}</td>
            <th>Weight</th>
            <td>{float(bill['weight']):,.2f} {e(bill['weight_unit'])}</td>
        </tr>
    </table>

    <table>
        <tr>
            <th>Description</th>
            <th class="right">Amount</th>
        </tr>
        <tr>
            <td>Freight Amount</td>
            <td class="right">{money(bill['freight_amount'])}</td>
        </tr>
        <tr>
            <td>Loading Charges</td>
            <td class="right">{money(bill['loading_charges'])}</td>
        </tr>
        <tr>
            <td>Unloading Charges</td>
            <td class="right">{money(bill['unloading_charges'])}</td>
        </tr>
        <tr>
            <td>Other Charges</td>
            <td class="right">{money(bill['other_charges'])}</td>
        </tr>
        <tr class="total">
            <td>Gross Total</td>
            <td class="right">{money(
                bill['freight_amount']
                + bill['loading_charges']
                + bill['unloading_charges']
                + bill['other_charges']
            )}</td>
        </tr>
        <tr>
            <td>Advance Paid</td>
            <td class="right">{money(bill['advance_paid'])}</td>
        </tr>
        <tr class="total">
            <td>Balance Payable</td>
            <td class="right">{money(bill['balance_payable'])}</td>
        </tr>
    </table>

    <div class="remarks">
        <strong>Remarks:</strong><br>
        {e(bill['remarks'])}
    </div>

    <div class="footer">
        <div class="signature">Transporter / Authorized Signatory</div>
        <div class="signature">Receiver Signature</div>
    </div>

</div>
</body>
</html>
"""


# ============================================================
# STREAMLIT UI
# ============================================================

st.set_page_config(
    page_title="Transport Bill Generator",
    page_icon="🚚",
    layout="wide"
)

init_db()

st.title("🚚 Transport Bill Generator")
st.caption("Create, save and generate transport/freight bills using Python + Streamlit + SQLite.")

if "page" not in st.session_state:
    st.session_state.page = "home"

if "last_bill_id" not in st.session_state:
    st.session_state.last_bill_id = None


# ---------------- HOME ----------------

if st.session_state.page == "home":

    st.subheader("Transport Billing System")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("➕ New Bill", use_container_width=True, type="primary"):
            st.session_state.page = "new_bill"
            st.rerun()

    with c2:
        if st.button("📋 View Saved Bills", use_container_width=True):
            st.session_state.page = "saved_bills"
            st.rerun()

    with c3:
        rows = get_all_bills()
        st.metric("Bills Generated", len(rows))

    st.divider()

    st.info(
        "Click **New Bill** to enter truck and transport details. "
        "After submission, the record is stored in SQLite and the generated bill "
        "can be downloaded or printed."
    )

    rows = get_all_bills()

    if rows:
        st.subheader("Recent Bills")

        for row in rows[:5]:
            with st.container(border=True):
                a, b, c, d = st.columns([2, 2, 2, 1])

                a.write(f"**{row['bill_no']}**")
                b.write(f"{row['from_location']} → {row['to_location']}")
                c.write(f"Truck: **{row['truck_no']}**")

                if d.button("Open", key=f"open_{row['id']}"):
                    st.session_state.last_bill_id = row["id"]
                    st.session_state.page = "bill"
                    st.rerun()


# ---------------- NEW BILL ----------------

elif st.session_state.page == "new_bill":

    st.subheader("➕ New Transport Bill")

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    bill_no = generate_bill_no()

    st.info(f"Bill Number: **{bill_no}**")

    with st.form("transport_bill_form"):

        st.markdown("### 1. Bill & Vehicle Details")

        c1, c2, c3 = st.columns(3)

        with c1:
            bill_date = st.date_input("Bill Date", value=date.today())

        with c2:
            truck_no = st.text_input(
                "Truck / Vehicle Number *",
                placeholder="e.g. HR55AB1234"
            )

        with c3:
            driver_name = st.text_input(
                "Driver Name",
                placeholder="Driver name"
            )

        c1, c2 = st.columns(2)

        with c1:
            driver_mobile = st.text_input(
                "Driver Mobile",
                placeholder="10-digit mobile number"
            )

        with c2:
            pay_to = st.text_input(
                "Pay To *",
                placeholder="Transporter / Party name"
            )

        st.markdown("### 2. Route & Party Details")

        c1, c2 = st.columns(2)

        with c1:
            from_location = st.text_input(
                "From *",
                placeholder="Origin location"
            )

        with c2:
            to_location = st.text_input(
                "To *",
                placeholder="Destination location"
            )

        c1, c2 = st.columns(2)

        with c1:
            consignor = st.text_input(
                "Consignor",
                placeholder="Sender / consignor"
            )

        with c2:
            consignee = st.text_input(
                "Consignee",
                placeholder="Receiver / consignee"
            )

        st.markdown("### 3. Material & Weight")

        c1, c2, c3 = st.columns([2, 1, 1])

        with c1:
            material = st.text_input(
                "Material / Goods Description",
                placeholder="e.g. Electronics, Cement, Steel"
            )

        with c2:
            weight = st.number_input(
                "Weight",
                min_value=0.0,
                step=0.01,
                format="%.2f"
            )

        with c3:
            weight_unit = st.selectbox(
                "Weight Unit",
                ["MT", "KG", "TON", "QUINTAL"]
            )

        st.markdown("### 4. Freight & Charges")

        c1, c2 = st.columns(2)

        with c1:
            freight_rate = st.number_input(
                "Freight Rate",
                min_value=0.0,
                step=0.01,
                format="%.2f",
                help="Rate per selected weight unit. Freight amount is calculated automatically."
            )

        with c2:
            freight_amount = weight * freight_rate
            st.number_input(
                "Calculated Freight Amount",
                value=float(freight_amount),
                disabled=True,
                format="%.2f"
            )

        c1, c2, c3 = st.columns(3)

        with c1:
            loading_charges = st.number_input(
                "Loading Charges",
                min_value=0.0,
                step=0.01,
                format="%.2f"
            )

        with c2:
            unloading_charges = st.number_input(
                "Unloading Charges",
                min_value=0.0,
                step=0.01,
                format="%.2f"
            )

        with c3:
            other_charges = st.number_input(
                "Other Charges",
                min_value=0.0,
                step=0.01,
                format="%.2f"
            )

        gross_total = (
            freight_amount
            + loading_charges
            + unloading_charges
            + other_charges
        )

        st.markdown("### 5. Payment")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Gross Total", money(gross_total))

        with c2:
            advance_paid = st.number_input(
                "Advance Paid",
                min_value=0.0,
                step=0.01,
                format="%.2f"
            )

        balance_payable = max(gross_total - advance_paid, 0)

        with c3:
            st.metric("Balance Payable", money(balance_payable))

        remarks = st.text_area(
            "Remarks",
            placeholder="Enter any additional transport / payment remarks..."
        )

        submitted = st.form_submit_button(
            "✅ Submit Details & Generate Bill",
            use_container_width=True,
            type="primary"
        )

        if submitted:

            errors = []

            if not truck_no.strip():
                errors.append("Truck / Vehicle Number is required.")

            if not from_location.strip():
                errors.append("From location is required.")

            if not to_location.strip():
                errors.append("To location is required.")

            if not pay_to.strip():
                errors.append("Pay To is required.")

            if weight <= 0:
                errors.append("Weight must be greater than 0.")

            if freight_rate < 0:
                errors.append("Freight rate cannot be negative.")

            if advance_paid > gross_total:
                errors.append("Advance paid cannot be greater than the gross total.")

            if errors:
                for error in errors:
                    st.error(error)
            else:
                data = {
                    "bill_no": bill_no,
                    "bill_date": bill_date.isoformat(),
                    "truck_no": truck_no.strip().upper(),
                    "from_location": from_location.strip(),
                    "to_location": to_location.strip(),
                    "pay_to": pay_to.strip(),
                    "consignor": consignor.strip(),
                    "consignee": consignee.strip(),
                    "driver_name": driver_name.strip(),
                    "driver_mobile": driver_mobile.strip(),
                    "material": material.strip(),
                    "weight": weight,
                    "weight_unit": weight_unit,
                    "freight_rate": freight_rate,
                    "freight_amount": freight_amount,
                    "loading_charges": loading_charges,
                    "unloading_charges": unloading_charges,
                    "other_charges": other_charges,
                    "advance_paid": advance_paid,
                    "balance_payable": balance_payable,
                    "remarks": remarks.strip()
                }

                try:
                    save_bill(data)

                    conn = get_connection()
                    row = conn.execute(
                        "SELECT id FROM transport_bills WHERE bill_no = ?",
                        (bill_no,)
                    ).fetchone()
                    conn.close()

                    st.session_state.last_bill_id = row["id"]
                    st.session_state.page = "bill"
                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error("Bill number already exists. Please submit again.")


# ---------------- GENERATED BILL ----------------

elif st.session_state.page == "bill":

    bill = get_bill(st.session_state.last_bill_id)

    if not bill:
        st.error("Bill not found.")
        if st.button("Back to Home"):
            st.session_state.page = "home"
            st.rerun()
    else:

        st.subheader(f"✅ Bill Generated — {bill['bill_no']}")

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()

        with c2:
            if st.button("➕ Create Another Bill", use_container_width=True):
                st.session_state.page = "new_bill"
                st.rerun()

        with c3:
            bill_html = create_bill_html(bill)

            st.download_button(
                "⬇️ Download Bill",
                data=bill_html,
                file_name=f"{bill['bill_no']}.html",
                mime="text/html",
                use_container_width=True
            )

        st.markdown(
            """
            **Tip:** Open the downloaded HTML file in Chrome/Edge and use
            **Print → Save as PDF** if you need a PDF copy.
            """
        )

        st.divider()

        # Render the generated bill directly in the app.
        st.components.v1.html(bill_html, height=1100, scrolling=True)


# ---------------- SAVED BILLS ----------------

elif st.session_state.page == "saved_bills":

    st.subheader("📋 Saved Transport Bills")

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    rows = get_all_bills()

    if not rows:
        st.info("No bills have been generated yet.")
    else:

        for row in rows:

            with st.container(border=True):

                c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])

                c1.write(f"**{row['bill_no']}**")
                c2.write(row["bill_date"])
                c3.write(f"🚚 {row['truck_no']}")
                c4.write(
                    f"{row['from_location']} → {row['to_location']}"
                )

                if c5.button("Open", key=f"saved_{row['id']}"):
                    st.session_state.last_bill_id = row["id"]
                    st.session_state.page = "bill"
                    st.rerun()

                st.caption(
                    f"Pay To: {row['pay_to']} | "
                    f"Weight: {row['weight']} {row['weight_unit']} | "
                    f"Balance: {money(row['balance_payable'])}"
                )
