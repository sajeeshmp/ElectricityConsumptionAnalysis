import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Electricity Consumption Analysis", page_icon="⚡", layout="wide")

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTH_LABELS = [f"{i + 1:02d} {m}" for i, m in enumerate(MONTHS)]  # keeps chart order


# ---------------- Module 2: plain Python functions ----------------
def calculate_bill(units):
    """Slab rates: first 100 units @ Rs.3, next 200 @ Rs.5, remaining @ Rs.7."""
    if units <= 100:
        return units * 3
    elif units <= 300:
        return 100 * 3 + (units - 100) * 5
    else:
        return 100 * 3 + 200 * 5 + (units - 300) * 7


def demo(code, result):
    """Show code on the left and its output on the right."""
    left, right = st.columns(2)
    left.code(code, language="python")
    right.write(result)


@st.cache_data
def load_data():
    data = pd.read_csv("data/electricity_usage.csv")
    totals, bills = [], []
    for _, row in data.iterrows():  # for loop + list (Module 2)
        units_list = [int(row[m]) for m in MONTHS]
        totals.append(sum(units_list))
        bills.append(sum(calculate_bill(u) for u in units_list))
    data["Total_Units"] = totals
    data["Annual_Bill"] = bills
    return data


df = load_data()
usage = df[MONTHS].to_numpy()  # 2D NumPy array: consumers x months

page = st.sidebar.radio("Go to", ["1. Home (Module 1)", "2. Python Basics (Module 2)",
                                  "3. NumPy Analysis (Module 3)", "4. Pandas Explorer (Module 4)",
                                  "5. Insights"])
st.sidebar.caption("Python Programming for Data Science (25CD36C)")

# =====================================================================
# PAGE 1: HOME  (Module 1: Introduction to Data Science)
# =====================================================================
if page.startswith("1"):
    st.title("⚡ Electricity Consumption Analysis")
    st.write("A data analysis project built with Python, NumPy, Pandas and Streamlit.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Consumers", len(df))
    c2.metric("Months", len(MONTHS))
    c3.metric("Total units", f"{int(usage.sum()):,}")
    c4.metric("Total billed (₹)", f"{int(df['Annual_Bill'].sum()):,}")

    st.subheader("The data analysis process")
    st.write("**Collect** → **Load** → **Explore** → **Analyse** → **Visualise** → **Interpret**")
    st.write("Data is stored in a CSV file, loaded with Pandas, analysed with NumPy and "
             "Pandas, and the results are visualised in this app.")

    q, l = st.columns(2)
    q.subheader("Quantitative data")
    q.write("Monthly units consumed, total units, annual bill amount (numerical, measurable).")
    l.subheader("Qualitative data")
    l.write("Consumer name, category (Residential / Commercial / Industrial) and city "
            "(descriptive, categorical).")

    st.subheader("Why Python for data analysis?")
    st.write("Simple syntax, powerful libraries (NumPy for arrays, Pandas for tables), "
             "and easy integration with visualisation tools.")

    st.subheader("Dataset preview")
    st.dataframe(df.head(10))

# =====================================================================
# PAGE 2: PYTHON BASICS  (Module 2)
# =====================================================================
elif page.startswith("2"):
    st.header("Module 2: Python Basics")

    st.subheader("A. Bill calculator (variables, operators, if/elif, while)")
    name = st.text_input("Consumer name", "Ravi")
    units = st.number_input("Units consumed", min_value=0, value=250, step=10)
    if st.button("Calculate bill"):
        st.success(f"{name}, your bill for {units} units is ₹{calculate_bill(units)}")
        remaining, i, rows = units, 0, []
        slabs = [(100, 3), (200, 5), (float("inf"), 7)]  # (slab size, rate)
        while remaining > 0 and i < len(slabs):  # while loop
            limit, rate = slabs[i]
            used = min(remaining, limit)
            rows.append({"Slab": i + 1, "Units": used, "Rate (₹)": rate, "Amount (₹)": used * rate})
            remaining -= used
            i += 1
        st.table(rows)

    st.subheader("B. for loop: bills for sample readings")
    lines = []
    for u in [50, 100, 150, 300, 450]:
        lines.append(f"{u} units -> ₹{calculate_bill(u)}")
    st.text("\n".join(lines))

    st.subheader("C. Data structures (using the first consumer's data)")
    first = df.iloc[0]
    monthly = [int(first[m]) for m in MONTHS]
    avg = sum(monthly) / len(monthly)
    pairs = tuple(zip(MONTHS, monthly))

    st.markdown(f"**List**: monthly units of {first['Name']}")
    demo("monthly[:3]\nsorted(monthly, reverse=True)[:3]\nmax(monthly), min(monthly)\nsum(monthly) / len(monthly)",
         {"first 3 months": monthly[:3], "top 3 values": sorted(monthly, reverse=True)[:3],
          "max": max(monthly), "min": min(monthly), "average": round(avg, 1)})

    st.markdown("**Tuple**: (month, units) pairs")
    demo("pairs = tuple(zip(MONTHS, monthly))\npairs[0]\npairs[-3:]\nmax(pairs, key=lambda p: p[1])",
         {"pairs[0]": pairs[0], "pairs[-3:]": pairs[-3:],
          "peak month": max(pairs, key=lambda p: p[1])})

    st.markdown("**Set**: unique values and set operations")
    high_months = {m for m, u in pairs if u > avg}
    summer = {"Mar", "Apr", "May"}
    demo("set(df['Category'])\nhigh_months = {m for m, u in pairs if u > avg}\n"
         "high_months & summer   # intersection\nhigh_months | summer   # union\nsummer - high_months   # difference",
         {"categories": set(df["Category"]), "cities": set(df["City"]),
          "above-average months": high_months, "intersection": high_months & summer,
          "union": high_months | summer, "difference": summer - high_months})

    st.markdown("**Dictionary**: month → units")
    month_dict = dict(pairs)
    demo("month_dict = dict(pairs)\nmonth_dict['Jan']\nlist(month_dict.keys())[:3]\nmonth_dict['Jan'] = month_dict['Jan'] + 10",
         {"Jan": month_dict["Jan"], "first 3 keys": list(month_dict.keys())[:3],
          "items (first 2)": list(month_dict.items())[:2]})

    st.markdown("**Nested dictionary**: consumer → month → units (first 3 consumers, 3 months)")
    nested = {df.loc[i, "Name"]: {m: int(df.loc[i, m]) for m in MONTHS[:3]} for i in range(3)}
    demo("nested = {name: {month: units}}\nnested['" + df.loc[0, "Name"] + "']['Jan']", nested)

# =====================================================================
# PAGE 3: NUMPY  (Module 3)
# =====================================================================
elif page.startswith("3"):
    st.header("Module 3: NumPy Analysis")
    st.caption("`usage` is a 2D ndarray: rows = consumers, columns = months")

    st.subheader("Creating arrays and data types")
    demo("usage = df[MONTHS].to_numpy()\nusage.shape, usage.ndim, usage.dtype\n"
         "np.arange(1, 13)\nnp.zeros((2, 3))\nnp.array([1, 2, 3], dtype=np.float64)",
         {"shape": usage.shape, "ndim": usage.ndim, "dtype": str(usage.dtype),
          "arange": np.arange(1, 13).tolist(), "zeros": np.zeros((2, 3)).tolist(),
          "float array": np.array([1, 2, 3], dtype=np.float64).tolist()})

    st.subheader("Indexing and slicing")
    demo("usage[0]            # first consumer, all months\nusage[:5, 0]        # Jan units of first 5\n"
         "usage[:3, :4]       # 3 consumers x 4 months\n(usage > 300).sum() # boolean indexing count",
         {"usage[0]": usage[0].tolist(), "usage[:5, 0]": usage[:5, 0].tolist(),
          "usage[:3, :4]": usage[:3, :4].tolist(), "readings above 300": int((usage > 300).sum())})

    st.subheader("Statistics along axes")
    month_totals = usage.sum(axis=0)
    demo("usage.sum(axis=1)[:5]          # total per consumer\nusage.mean(axis=0).round(1)  # average per month\n"
         "month_totals = usage.sum(axis=0)\nMONTHS[month_totals.argmax()]  # peak month",
         {"total of first 5 consumers": usage.sum(axis=1)[:5].tolist(),
          "monthly averages": usage.mean(axis=0).round(1).tolist(),
          "peak month": MONTHS[month_totals.argmax()]})
    st.bar_chart(pd.Series(month_totals, index=MONTH_LABELS))

    st.subheader("Transposing arrays and swapping axes")
    demo("usage.T.shape\nusage.swapaxes(0, 1).shape\nusage.T[0][:5]  # Jan column of first 5",
         {"original shape": usage.shape, "transpose shape": usage.T.shape,
          "swapaxes shape": usage.swapaxes(0, 1).shape, "usage.T[0][:5]": usage.T[0][:5].tolist()})

    st.subheader("Universal functions (ufuncs)")
    a, b = usage[0, :4], usage[1, :4]
    demo("np.sqrt(a)\nnp.add(a, b)\nnp.maximum(a, b)\nnp.where(usage[:, 0] > 200, 'High', 'Normal')[:6]",
         {"a": a.tolist(), "b": b.tolist(), "sqrt(a)": np.sqrt(a).round(1).tolist(),
          "add(a, b)": np.add(a, b).tolist(), "maximum(a, b)": np.maximum(a, b).tolist(),
          "where": np.where(usage[:, 0] > 200, "High", "Normal")[:6].tolist()})

    st.subheader("Random number generation")
    np.random.seed(1)
    demo("np.random.seed(1)\nnp.random.randint(5, 30, size=7)  # 7 daily readings\n"
         "np.random.rand(3)\nnp.random.normal(100, 15, size=3)",
         {"randint": np.random.randint(5, 30, size=7).tolist(),
          "rand": np.random.rand(3).round(3).tolist(),
          "normal": np.random.normal(100, 15, size=3).round(1).tolist()})

# =====================================================================
# PAGE 4: PANDAS EXPLORER  (Module 4)
# =====================================================================
elif page.startswith("4"):
    st.header("Module 4: Pandas Explorer")

    st.subheader("Series")
    jan = pd.Series(df["Jan"].values, index=df["Name"])
    demo("jan = pd.Series(df['Jan'].values, index=df['Name'])\njan.head(3)\njan.mean(), jan.max(), jan.idxmax()",
         {"head": jan.head(3).to_dict(), "mean": round(jan.mean(), 1),
          "max": int(jan.max()), "idxmax": jan.idxmax()})

    st.subheader("DataFrame")
    demo("df.shape\ndf.columns[:6]\ndf.dtypes.head(5)",
         {"shape": df.shape, "columns": df.columns[:6].tolist(), "dtypes": df.dtypes.head(5).astype(str).to_dict()})
    st.dataframe(df.describe())

    st.subheader("Reindexing")
    indexed = df.set_index("ConsumerID")
    new_order = list(indexed.index[:3])[::-1] + ["C999"]  # C999 does not exist
    st.code("indexed = df.set_index('ConsumerID')\nnew_order = ['C003', 'C002', 'C001', 'C999']\n"
            "indexed[['Name', 'Jan']].reindex(new_order)", language="python")
    st.dataframe(indexed[["Name", "Jan"]].reindex(new_order))
    st.caption("The missing label C999 becomes NaN.")

    st.subheader("Data selection")
    cols = st.multiselect("Choose columns", df.columns.tolist(), default=["Name", "Category", "Total_Units"])
    st.dataframe(df[cols].head(10))
    demo("df.loc[0, 'Name']\ndf.iloc[0:3, 0:3]\ndf.loc[df['Name'] == 'Ravi']",
         {"loc[0, 'Name']": df.loc[0, "Name"], "iloc[0:3, 0:3]": df.iloc[0:3, 0:3].to_dict("records")})

    st.subheader("Filtering")
    f1, f2, f3 = st.columns(3)
    category = f1.selectbox("Category", ["All"] + sorted(set(df["Category"])))
    month = f2.selectbox("Month", MONTHS)
    min_units = f3.slider("Minimum units", 0, int(df[month].max()), 200)
    mask = df[month] >= min_units
    if category != "All":
        mask = mask & (df["Category"] == category)
    st.write(f"**{int(mask.sum())}** consumers match")
    st.dataframe(df[mask][["ConsumerID", "Name", "Category", "City", month]])

    st.subheader("Indexing and sorting")
    s1, s2 = st.columns(2)
    sort_col = s1.selectbox("Sort by", ["Total_Units", "Annual_Bill"] + MONTHS)
    order = s2.radio("Order", ["Descending", "Ascending"], horizontal=True)
    st.dataframe(df.sort_values(sort_col, ascending=(order == "Ascending")).head(10))
    st.code("df.set_index('Name').sort_index().head()", language="python")
    st.dataframe(df.set_index("Name").sort_index().head())

# =====================================================================
# PAGE 5: INSIGHTS  (uses Modules 2-4 only)
# =====================================================================
else:
    st.header("Insights")

    month_totals = df[MONTHS].sum()
    peak, low = month_totals.idxmax(), month_totals.idxmin()
    top = df.sort_values("Annual_Bill", ascending=False).iloc[0]
    high_users = int((df["Total_Units"] / 12 > 300).sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Peak month", peak, f"{int(month_totals[peak]):,} units")
    c2.metric("Lowest month", low, f"{int(month_totals[low]):,} units")
    c3.metric("Highest bill", top["Name"], f"₹{int(top['Annual_Bill']):,}")
    c4.metric("Avg > 300 units/month", high_users)

    st.subheader("Monthly consumption")
    st.line_chart(pd.Series(month_totals.values, index=MONTH_LABELS))

    st.subheader("Top 5 consumers by annual bill")
    st.dataframe(df.sort_values("Annual_Bill", ascending=False).head(5)
                 [["ConsumerID", "Name", "Category", "City", "Total_Units", "Annual_Bill"]])

    st.subheader("Category-wise summary")
    rows = []
    for cat in sorted(set(df["Category"])):  # set + loop + filter (no groupby)
        subset = df[df["Category"] == cat]
        rows.append({"Category": cat, "Consumers": len(subset),
                     "Avg annual units": round(subset["Total_Units"].mean(), 1),
                     "Avg annual bill (₹)": round(subset["Annual_Bill"].mean(), 1)})
    st.table(rows)
    st.bar_chart(pd.DataFrame(rows).set_index("Category")["Avg annual bill (₹)"])

    st.subheader("Conclusions")
    st.write(f"- Consumption peaks in **{peak}**, likely due to higher cooling demand in summer.")
    st.write(f"- **{top['Name']}** ({top['Category']}) has the highest annual bill of ₹{int(top['Annual_Bill']):,}.")
    st.write("- Industrial consumers use far more electricity than residential ones.")
    st.write("- The slab system means heavy users pay a much higher average rate per unit.")
