import marimo

__generated_with = "0.6.1-dev29"
app = marimo.App()


@app.cell
def __(mo):
    comp_values = mo.md(
        """
        - Electron source semi-angle: {conv_angle}
        - Beam tilt: {beam_tilt_x}
        """
    ).batch(
        conv_angle=mo.ui.slider(
            start=0.05,
            stop=0.5,
            step=0.01,
            value=0.3,
        ),
        beam_tilt_x=mo.ui.slider(
            start=-0.45,
            stop=0.45,
            step=0.01,
            value=0.
        )
    )
    comp_values
    return comp_values,


@app.cell
def __(plt, temgymlite, tilted_beam_model_pos):
    fig, ax = plt.subplots(figsize=(6.5, 8))

    fig, ax = temgymlite.show_matplotlib(
        tilted_beam_model_pos,
        figax=(fig, ax),
        label_fontsize=12,
        plot_rays=False,
        fill_color="green",
        highlight_edges=True,
        fill_alpha=0.75,
        show_labels=True,
    )

    # ax.set_xlim([-0.5,2.5])

    fig.tight_layout()
    ax
    return ax, fig


@app.cell
async def __():
    # imports
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import sys

    if "pyodide" in sys.modules:
        import micropip

        repo = "https://raw.githubusercontent.com/gvarnavi/TemGymLite/main/dist/"
        wheel = "temgymlite-0.6.0.0-py3-none-any.whl"
        await micropip.install(repo + wheel)

    import temgymlite
    return micropip, mo, np, plt, repo, sys, temgymlite, wheel


@app.cell
def __(temgymlite):
    components = [
        temgymlite.Lens(name="Electrostatic Lens", z=3, f=-0.2),
        temgymlite.Lens(name="1st Condenser Lens", z=2.6, f=-0.2),
        temgymlite.Lens(name="2nd Condenser Lens", z=2.5, f=-0.2),
        # temgymlite.Aperture(
        #     name="Condenser Aperture", z=2.3, aperture_radius_inner=0.5
        # ),
        temgymlite.Quadrupole(name="Condenser Stig", z=2.2),
        temgymlite.Lens(name="Condenser Mini Lens", z=1.8, f=-0.2),
        # temgymlite.Aperture(
        #     name="Objective Aperture", z=1.7, aperture_radius_inner=0.05
        # ),
        temgymlite.Lens(name="Sample Inside Objective Lens", z=1.5, f=-0.2),
        temgymlite.Sample(z=1.5),
        temgymlite.Quadrupole(name="Objective Stig", z=1.4),
        temgymlite.Lens(name="Objective Mini Lens", z=1.3, f=-0.2),
        # temgymlite.Aperture(
        #     name="Selected Area Aperture",
        #     z=0.9,
        #     aperture_radius_inner=0.05,
        # ),
        temgymlite.Quadrupole(name="Intermediate Lens Stigmator", z=0.8),
        temgymlite.Lens(name="1st Intermediate Lens", z=0.7, f=-0.2),
        temgymlite.Lens(name="2nd Intermediate Lens", z=0.6, f=-0.2),
        temgymlite.Lens(name="3rd Intermediate Lens", z=0.5, f=-0.2),
        temgymlite.Lens(name="Projector Lens", z=0.2, f=-0.2),
    ]
    return components,


@app.cell
def __(comp_values, components, temgymlite):
    conv_angle = comp_values.value["conv_angle"]
    beam_tilt_x = comp_values.value["beam_tilt_x"]

    tilted_beam_model_pos = temgymlite.Model(
        components,
        beam_z=3.5,
        beam_type="x_axial",
        num_rays=2,
        beam_tilt_x=beam_tilt_x,
        gun_beam_semi_angle=conv_angle,
    )
    return beam_tilt_x, conv_angle, tilted_beam_model_pos


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
