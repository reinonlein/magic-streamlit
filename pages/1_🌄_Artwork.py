import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

st.set_page_config(page_title="Artwork", page_icon="🌄", layout="wide")

# Get base data
my_cards = pd.read_csv("./data/my-cards.csv")
filtered_cards = my_cards

# visualisation settings
show_cards = st.sidebar.number_input("Show cards", value=1000, step=1)

card_size = st.sidebar.number_input("Card size", value=140, step=10)

card_margin = st.sidebar.number_input("Card margin", value=1.0, step=0.1)

# kies de kwaliteit van de afbeeldingen
quality = st.sidebar.selectbox(
    "Kwaliteit", ["normal", "small", "large", "art_crop", "border_crop"]
)

my_cards["image_url"] = my_cards[quality]


# Add filters to the page
filter_sets = st.sidebar.multiselect(
    "Filter Sets:",
    my_cards["Set Name"].sort_values().unique(),
)

if filter_sets:
    filtered_cards = my_cards.loc[lambda d: d["Set Name"].isin(filter_sets)]

# card type filters
filter_card_type = st.sidebar.multiselect(
    "Card type:",
    my_cards["card_type"].sort_values().unique(),
)

if filter_card_type:
    filtered_cards = my_cards.loc[lambda d: d["card_type"].isin(filter_card_type)]

# card subtype filters
filter_card_subtype = st.sidebar.multiselect(
    "Card subtype:",
    my_cards["card_subtype"].sort_values().unique(),
)

if filter_card_subtype:
    filtered_cards = my_cards.loc[lambda d: d["card_subtype"].isin(filter_card_subtype)]

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

# create html card divs
divs = [
    f"""
    <img src="{card}" style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.5); border-radius: 4%; margin: {card_margin}em" width={card_size}>
    """
    for card in filtered_cards.head(show_cards)["image_url"]
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
    height=2400,
    scrolling=True,
)
