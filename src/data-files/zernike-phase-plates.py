import marimo

__generated_with = "0.6.2"
app = marimo.App()


@app.cell(hide_code=True)
def __():
    import marimo as mo
    import numpy as np
    import sys
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    return make_axes_locatable, mo, np, plt, sys


@app.cell(hide_code=True)
def __():
    class PotentialArray:
        def __init__(self, array, slice_thickness, sampling):
            self.array = array
            self.slice_thickness = slice_thickness
            self.sampling = sampling
            self.gpts = array.shape[1:]
    return PotentialArray,


@app.cell(hide_code=True)
async def __(PotentialArray, defocus, np, sys):
    # embedded_potential_array_xyz = np.load("data/apoF-ice-embedded-potential.npy")

    # res = embedded_potential_array_xyz.shape[0]
    # bin_factor_z = res // 32
    # bin_factor_xy = 2
    # pixel_size = 2 / 3
    # binned_volume_xyz = embedded_potential_array_xyz.reshape(
    #     (
    #         res // bin_factor_xy,
    #         bin_factor_xy,
    #         res // bin_factor_xy,
    #         bin_factor_xy,
    #         res // bin_factor_z,
    #         bin_factor_z,
    #     )
    # ).sum((1, 3, 5))

    # binned_volume_zxy = binned_volume_xyz.transpose(
    #     2, 0, 1
    # )  # abtem expects the first dimension to be z

    file_name = "apoF-ice-embedded-potential-binned.npy"
    if "pyodide" in sys.modules:

        from pyodide.http import pyfetch
        import os

        async def download_remote_file(url, filename, overwrite=False):
            if not os.path.isfile(filename) or overwrite:
                #print(f"Downloading file to {filename}")
                response = await pyfetch(url)
                if response.status == 200:
                    with open(filename, "wb") as f:
                        f.write(await response.bytes())
        file_url = (
            "https://raw.githubusercontent.com/gvarnavi/py4DSTEM-lite/dev/data/"
        )
        await download_remote_file(
            file_url + "apoF-ice-embedded-potential-binned.npy",
            file_name        
        )

        binned_volume_zxy = np.load(file_name)

    else:
        binned_volume_zxy = np.load("src/data-files/data/"+file_name)
    pixel_size = 2 / 3
    bin_factor_xy = 2
    bin_factor_z = 6

    potential = PotentialArray(
        binned_volume_zxy,
        slice_thickness=pixel_size * bin_factor_z,
        sampling=(pixel_size * bin_factor_xy, pixel_size * bin_factor_xy),
    )

    potential.slice_thickness += 1e4 * defocus / binned_volume_zxy.shape[0]
    return (
        bin_factor_xy,
        bin_factor_z,
        binned_volume_zxy,
        download_remote_file,
        file_name,
        file_url,
        os,
        pixel_size,
        potential,
        pyfetch,
    )


@app.cell(hide_code=True)
def __():
    semiangle  = 4 # mrad
    wavelength = 0.0197 # A (300kV)
    sigma = 0.00065 # 1/V (300kV)
    rolloff = 0.125 # mrad
    return rolloff, semiangle, sigma, wavelength


@app.cell
def __(mo, np):
    slider_inputs = mo.md(
        r"""
        defocus [µm]: {defocus}    
        electron dose [$e/\AA^2$]:  {electrons_per_area}  
        insert Zernike phase-plate :{show_zernike}
        """
    ).batch(
        defocus=mo.ui.slider(
            value=0, start=-2, stop=2, step=0.05, show_value=True
        ),
        electrons_per_area=mo.ui.slider(
            steps=list(np.logspace(1, 3, num=10)), value=1000.0, show_value=True
        ),
        show_zernike=mo.ui.switch(),
    )
    slider_inputs
    return slider_inputs,


@app.cell
def __(slider_inputs):
    defocus = slider_inputs.value["defocus"]
    electrons_per_area = slider_inputs.value['electrons_per_area']
    show_zernike = slider_inputs.value['show_zernike']
    return defocus, electrons_per_area, show_zernike


@app.cell
def __(exit_wave, exit_wave_zernike, plt, show_zernike):
    fig, axs = plt.subplots(1, 2, figsize=(8.75, 4))

    axs[0].imshow(
        exit_wave,
        cmap="gray"
    )
    axs[0].set_title(
        "CTEM image intensity",
        fontsize=14,
    )

    if show_zernike:
        axs[1].imshow(
            exit_wave_zernike,
            cmap="gray"
        )
        axs[1].set_title(
            "Zernike phase-plate intensity",
            fontsize=14,
        )
    else:
        axs[1].axis("off")
        
    for ax in axs:
        ax.set_xticks([])
        ax.set_yticks([])


    fig.tight_layout()
    fig
    return ax, axs, fig


@app.cell(hide_code=True)
def __(np):
    class CTF:
        def __init__(
            self,
            semiangle_cutoff,
            rolloff,
        ):
            self.semiangle_cutoff = semiangle_cutoff
            self.rolloff = rolloff

        def evaluate_aperture(self, alpha, phi):
            semiangle_cutoff = self.semiangle_cutoff / 1000
            if self.rolloff > 0:
                rolloff = self.rolloff / 1000
                array = 0.5 * (
                    1
                    + np.cos(
                        np.pi * (alpha - semiangle_cutoff + rolloff) / rolloff
                    )
                )
                array[alpha > semiangle_cutoff] = 0.0
                array = np.where(
                    alpha > semiangle_cutoff - rolloff,
                    array,
                    np.ones_like(alpha),
                )
            else:
                array = np.array(alpha < semiangle_cutoff)
            return array
    return CTF,


@app.cell(hide_code=True)
def __(np):
    class FresnelPropagator:
        def __init__(self):
            return None

        def evaluate_propagator_array(self, gpts, sampling, wavelength, dz, tilt):
            kx = np.fft.fftfreq(gpts[0], sampling[0])
            ky = np.fft.fftfreq(gpts[1], sampling[1])
            k = np.sqrt(kx[:, None] ** 2 + ky[None, :] ** 2)
            f = np.exp(
                -1j * (kx[:, None] ** 2 * np.pi * wavelength * dz)
            ) * np.exp(-1j * (ky[None, :] ** 2 * np.pi * wavelength * dz))

            if tilt is not None:
                f *= np.exp(
                    -1j * (kx[:, None] * np.tan(tilt[0] / 1e3) * dz * 2 * np.pi)
                )
                f *= np.exp(
                    -1j * (ky[None, :] * np.tan(tilt[1] / 1e3) * dz * 2 * np.pi)
                )

            kcut = 1 / np.max(sampling) / 2 * 2 / 3
            mask = 0.5 * (1 + np.cos(np.pi * (k - kcut + 0.1) / 0.1))
            mask[k > kcut] = 0.0
            mask = np.where(k > kcut - 0.1, mask, np.ones_like(k))

            return f * mask

        def propagate(
            self,
            array,
            propagator_array,
        ):
            array_fft = np.fft.fft2(array)
            return np.fft.ifft2(array_fft * propagator_array)
    return FresnelPropagator,


@app.cell(hide_code=True)
def __(FresnelPropagator, np, sigma):
    class Waves:
        def __init__(self, array, sampling, wavelength, tilt):
            self.array = array
            self.sampling = sampling
            self.wavelength = wavelength
            self.tilt = tilt
            self.gpts = array.shape
            self.propagator = FresnelPropagator()

        def get_spatial_frequencies(self):
            sx, sy = self.sampling
            nx, ny = self.gpts
            kx = np.fft.fftfreq(nx, sx)
            ky = np.fft.fftfreq(ny, sy)
            return kx, ky

        def get_scattering_angles(self):
            kx, ky = self.get_spatial_frequencies()
            alpha = np.sqrt(kx[:, None] ** 2 + ky[None, :] ** 2) * self.wavelength
            phi = np.arctan2(ky[None, :], kx[:, None])
            return alpha, phi

        def multislice(self, potential):
            dz = potential.slice_thickness
            out_array = self.array.copy()
            prop = self.propagator
            prop_array = prop.evaluate_propagator_array(
                self.gpts, self.sampling, self.wavelength, dz, self.tilt
            )
            for slice in potential.array:
                out_array = out_array * np.exp(1j * sigma * slice)
                out_array = prop.propagate(out_array, prop_array)
            return out_array
    return Waves,


@app.cell
def __(Waves, np, potential, wavelength):
    tilted_plane_wave = Waves(
        array=np.ones(potential.gpts, dtype=np.complex64),
        sampling=potential.sampling,
        wavelength=wavelength,
        tilt=(0, 0),
    )
    return tilted_plane_wave,


@app.cell(hide_code=True)
def __(ctf, np, tilted_plane_wave):
    alpha, phi = tilted_plane_wave.get_scattering_angles()
    bright_field_disk = np.fft.fftshift(ctf.evaluate_aperture(alpha, phi))
    return alpha, bright_field_disk, phi


@app.cell
def __(
    CTF,
    electrons_per_area,
    np,
    potential,
    rolloff,
    semiangle,
    show_zernike,
    tilted_plane_wave,
):
    ctf = CTF(
        semiangle_cutoff=semiangle,
        rolloff=rolloff,
    )

    exit_wave = tilted_plane_wave.multislice(potential)
    exit_wave_zernike = np.fft.fft2(exit_wave)
    if show_zernike:
        zernike_kernel = np.zeros_like(np.abs(exit_wave_zernike))
        zernike_kernel[0,0] = np.pi/2
        zernike_kernel = np.exp(1j*zernike_kernel)
        exit_wave_zernike = np.fft.ifft2(exit_wave_zernike * zernike_kernel)
        exit_wave_zernike = np.random.poisson(
            (
                np.abs(exit_wave_zernike) ** 2
                * np.prod(potential.sampling)
                * electrons_per_area
            ).clip(0)
        )

    exit_wave = np.random.poisson(
        (
            np.abs(exit_wave) ** 2
            * np.prod(potential.sampling)
            * electrons_per_area
        ).clip(0)
    )
    return ctf, exit_wave, exit_wave_zernike, zernike_kernel


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
