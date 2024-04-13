import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

st.set_page_config(page_title="Ontdubbelen", page_icon="👥", layout="wide")

# Get base data
my_cards = pd.read_csv("./data/my-cards.csv")

# Add filters to the page
filtered_cards = my_cards

filter_folders = st.sidebar.multiselect(
    "Filter Collections:",
    my_cards["Folder Name"].sort_values().unique(),
)

if filter_folders:
    filtered_cards = filtered_cards.loc[lambda d: d["Folder Name"].isin(filter_folders)]

filter_dubbelen = st.sidebar.radio(
    "Ontdubblen", ["Alle kaarten", "Uniek (houden)", "Dubbel"]
)

if filter_dubbelen == "Uniek (houden)":
    filtered_cards = filtered_cards.loc[
        lambda d: (d["TotalQuantity"] == 1)
        | (d["Quantity"] == d["TotalQuantity"])
        | (d["BoxedQuantity"] == 0)
    ]
elif filter_dubbelen == "Dubbel":
    filtered_cards = filtered_cards.loc[lambda d: d["TotalQuantity"] > 1]

# filter op kleur
color = st.sidebar.selectbox(
    "Kleur",
    ["Show all", "white", "blue", "black", "red", "green", "multicolor", "colorless"],
)

if color != "Show all":
    filtered_cards = filtered_cards.loc[lambda d: d["color"] == color]

# card type filters
filter_card_type = st.sidebar.multiselect(
    "Card type:",
    my_cards["card_type"].sort_values().unique(),
)

if filter_card_type:
    filtered_cards = filtered_cards.loc[lambda d: d["card_type"].isin(filter_card_type)]

# card subtype filters
filter_card_subtype = st.sidebar.multiselect(
    "Card subtype:",
    my_cards["card_subtype"].sort_values().unique(),
)

if filter_card_subtype:
    filtered_cards = filtered_cards.loc[
        lambda d: d["card_subtype"].isin(filter_card_subtype)
    ]

# filtered_cards = filtered_cards.loc[
#     lambda d: (len(filter_folders) > 0) & (d["Folder Name"].isin(filter_folders))
# ]

# visualisation settings
show_cards = st.sidebar.number_input("Show cards", value=2000, step=1000)

card_size = st.sidebar.number_input("Card size", value=210, step=10)

card_margin = st.sidebar.number_input("Card margin", value=1.0, step=0.1)


# Create page layout
df_height = 0 if filtered_cards.shape[0] < 10 else 735

col1, col2, col3, col4 = st.columns(4)
col1.metric("Aantal geselecteerde kaarten", filtered_cards["Quantity"].sum())
col2.metric("Unieke kaarten", filtered_cards.shape[0])
col3.metric("Aantal foil", filtered_cards["FoilQuantity"].sum().astype(int))
col4.metric("Waarde", filtered_cards["Value"].sum().round(2))


def highlighter(x):
    # initialize default colors
    color_codes = pd.DataFrame("", index=x.index, columns=x.columns)
    # set Check color to red if consumption exceeds threshold green otherwise
    color_codes["Card Name"] = np.where(
        x["BoxedQuantity"] > 0,
        "color:red",
        np.where(x["OtherQuantity"] > 0, "color: orange", "color:green"),
    )
    return color_codes


st.dataframe(
    filtered_cards.assign(Gevonden=lambda d: False)[
        [
            "image_url",
            "Set Name",
            "Folder Name",
            "Card Name",
            "Quantity",
            "BoxedQuantity",
            "OtherQuantity",
            "FoilQuantity",
            "TotalQuantity",
            # "Value",
        ]
    ]
    .style.apply(highlighter, axis=None)
    .format(
        {"BoxedQuantity": "{:.0f}", "OtherQuantity": "{:.0f}", "FoilQuantity": "{:.0f}"}
    ),
    use_container_width=True,
    height=df_height,
    hide_index=True,
    # disabled=("image_url"),
    column_config={
        "image_url": st.column_config.ImageColumn("Card Image", width="small"),
        "Gevonden": st.column_config.CheckboxColumn(
            "Gevonden?",
            disabled=False,
        ),
    },
)

# create html card divs
divs = [
    f"""
    <img src="{card}" style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.5); border-radius: 4%; margin: {card_margin}em" width={card_size} onclick="this.src='https://cdn.vectorstock.com/i/preview-1x/90/61/green-tick-icon-design-approved-vector-34269061.jpg'">
    """
    for card in filtered_cards["image_url"]
]
divs = "\n".join(divs)

html = """
<html>
  <base target="_blank" />
  <head>
    <style> </style>
  </head>
  <body>
  <div style="display: flex; flex-wrap: wrap; justify-content: center">
  %s
  </div>
  </body>
</html>
""" % (
    divs,
)

components.html(
    html,
    height=15000,
    scrolling=True,
)

st.write(filtered_cards)
