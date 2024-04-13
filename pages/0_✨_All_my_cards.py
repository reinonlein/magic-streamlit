import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(page_title="All my cards", page_icon="✨", layout="wide")


# Get all my cards
my_cards = pd.read_csv("./data/my-cards.csv")

filtered_cards = my_cards

# Add filters to the page
filter_sets = st.sidebar.multiselect(
    "Filter Sets:",
    my_cards["Set Name"].sort_values().unique(),
)

if filter_sets:
    filtered_cards = my_cards.loc[lambda d: d["Set Name"].isin(filter_sets)]

# filter op kleur
color = st.sidebar.selectbox(
    "Kleur",
    ["Show all", "white", "blue", "black", "red", "green", "multicolor", "colorless"],
)

if color != "Show all":
    filtered_cards = filtered_cards.loc[lambda d: d["color"] == color]

# filter op zeldzaamheid
rarity = st.sidebar.selectbox(
    "Rarity",
    ["Show all", "common", "uncommon", "rare", "mythic", "special"],
)

if rarity != "Show all":
    filtered_cards = filtered_cards.loc[lambda d: d["rarity"] == rarity]

# Create page layout
df_height = 0 if filtered_cards.shape[0] < 10 else 735

col1, col2, col3, col4 = st.columns(4)
col1.metric("Aantal geselecteerde kaarten", filtered_cards["Quantity"].sum())
col2.metric("Unieke kaarten", filtered_cards.shape[0])
col3.metric("Aantal foil", filtered_cards["FoilQuantity"].sum().astype(int))
col4.metric("Totale waarde", filtered_cards["Value"].sum().round(2))

st.dataframe(
    filtered_cards[
        [
            "image_url",
            "Card Name",
            "Set Name",
            "Card Number",
            "rarity",
            "FoilQuantity",
            "TotalQuantity",
            "Value",
        ]
    ],
    use_container_width=True,
    height=df_height,
    hide_index=True,
    column_config={
        "image_url": st.column_config.ImageColumn("Card Image", width="small"),
    },
)

st.dataframe(my_cards)
