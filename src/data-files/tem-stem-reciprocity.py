import marimo

__generated_with = "0.6.1-dev29"
app = marimo.App()


@app.cell(hide_code=True)
def __(
    bf_stem,
    df_stem,
    plt,
    ray_diagrams,
    scattered_model,
    temgymlite,
    unscattered_model,
):
    fig, (ax, ax_stem) = plt.subplots(1, 2, figsize=(9, 6))

    if ray_diagrams.value["ctem"]:
        fig, ax = temgymlite.show_matplotlib(
            scattered_model,
            figax=(fig, ax),
            label_fontsize=12,
            plot_rays=False,
            fill_color="purple",
            fill_between=True,
            highlight_edges=False,
            fill_alpha=0.5,
        )

        fig, ax = temgymlite.show_matplotlib(
            unscattered_model,
            figax=(fig, ax),
            label_fontsize=12,
            plot_rays=False,
            fill_color="green",
            fill_between=True,
            highlight_edges=False,
            fill_alpha=0.5,
            show_labels=False,
        )

        ax.set_title("CTEM", fontsize=16)
    else:
        ax.axis("off")

    if ray_diagrams.value["stem"]:
        fig, ax_stem = temgymlite.show_matplotlib(
            bf_stem,
            figax=(fig, ax_stem),
            label_fontsize=12,
            plot_rays=True,
            ray_lw=1,
            ray_color="purple",
            fill_between=False,
            highlight_edges=False,
            show_labels=False,
        )

        fig, ax_stem = temgymlite.show_matplotlib(
            df_stem,
            figax=(fig, ax_stem),
            label_fontsize=12,
            plot_rays=True,
            ray_lw=1,
            ray_color="green",
            fill_between=False,
            highlight_edges=False,
            show_labels=True,
        )

        ax_stem.set_title("STEM", fontsize=16)
        if ray_diagrams.value["invert_source"]:
            ax_stem.invert_yaxis()
    else:
        ax_stem.axis("off")

    # fig.tight_layout()
    ax
    return ax, ax_stem, fig


@app.cell(hide_code=True)
def __(temgymlite):
    components = [
        temgymlite.Lens(name="Condenser Lens", z=1, f=-0.5),
        temgymlite.Lens(name="Objective Lens", z=0.5, f=-0.1725),
    ]

    components_scattered = [
        temgymlite.Lens(name="Condenser Lens", z=1, f=-0.5),
        temgymlite.Deflector(name="Sample", z=0.75, defx=0.3),
        temgymlite.Lens(name="Objective Lens", z=0.5, f=-0.1725),
    ]


    unscattered_model = temgymlite.Model(
        components,
        beam_z=1.5,
        beam_type="x_axial",
        num_rays=2,
        gun_beam_semi_angle=0.15,
    )

    scattered_model = temgymlite.Model(
        components_scattered,
        beam_z=1.5,
        beam_type="x_axial",
        num_rays=2,
        gun_beam_semi_angle=0.15,
    )
    return (
        components,
        components_scattered,
        scattered_model,
        unscattered_model,
    )


@app.cell(hide_code=True)
def __(mo):
    ray_diagrams = mo.md(
        """
        Show ray diagrams:  
        CTEM {ctem} | STEM {stem}  
        invert source: {invert_source}
        """
    ).batch(
        ctem=mo.ui.checkbox(value=True),
        stem=mo.ui.checkbox(value=False),
        invert_source=mo.ui.switch(value=False),
    )
    ray_diagrams
    return ray_diagrams,


@app.cell(hide_code=True)
def __(temgymlite):
    components_stem = [
        temgymlite.DoubleDeflector(
            name="Scan Coil",
            z_up=1.3,
            z_low=1.2,
            updefx=-1,
            lowdefx=2,
        ),
        temgymlite.Lens(name="Objective Lens", z=1, f=-0.1),
        temgymlite.Sample(name="Sample", z=0.875),
        temgymlite.DoubleDeflector(
            name="Scan Coil",
            z_up=0.75,
            z_low=0.65,
            updefx=-0.1,
            lowdefx=-0.05,
        ),
        temgymlite.Aperture(
            name="BF Aperture", z=0.125, aperture_radius_inner=0.05
        ),
    ]

    df_stem = temgymlite.Model(
        components_stem,
        beam_z=1.5,
        beam_type="x_axial",
        num_rays=2,
        gun_beam_semi_angle=0.05,
    )

    bf_stem = temgymlite.Model(
        components_stem,
        beam_z=1.5,
        beam_type="x_axial",
        num_rays=3,
        gun_beam_semi_angle=0.05,
    )
    return bf_stem, components_stem, df_stem


@app.cell(hide_code=True)
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


if __name__ == "__main__":
    app.run()
