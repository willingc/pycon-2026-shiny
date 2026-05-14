from palmerpenguins import load_penguins
from plotnine import aes, geom_point, ggplot, theme_minimal
from shiny import reactive
from shiny.express import input, render, ui

dat = load_penguins().dropna()
species = dat["species"].unique().tolist()
num_cols = dat.select_dtypes("float64").columns.tolist()

ui.input_checkbox_group("species", "Species", species, selected=species, inline=True)
ui.input_select("x", "X", num_cols, selected="bill_depth_mm")
ui.input_select("y", "Y", num_cols, selected="body_mass_g")


@reactive.calc
def filtered():
    print("filtering...")
    return dat[dat["species"].isin(input.species())]


@render.plot
def plot():
    print("plotting")
    return (
        ggplot(filtered(), aes(x=input.x(), y=input.y(), color="species"))
        + geom_point(alpha=0.7)
        + theme_minimal()
    )


@render.text
def count():
    return f"{len(filtered())} penguins selected"
