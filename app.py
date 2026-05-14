from palmerpenguins import load_penguins
from plotnine import aes, geom_point, ggplot, theme_minimal
from shiny.express import input, render, ui

dat = load_penguins().dropna()
num_cols = dat.select_dtypes("float64").columns.tolist()
print(f"Number of columns: {num_cols}")
print(f"count of num_cols: {len(num_cols)}")

ui.input_select("x", "", num_cols, selected="bill_depth_mm")
ui.input_select("y", "", num_cols, selected="body_mass_g")


@render.plot
def plot():
    return (
        ggplot(dat, aes(x=input.x(), y=input.y(), color="species"))
        + geom_point(alpha=0.7)
        + theme_minimal()
    )
