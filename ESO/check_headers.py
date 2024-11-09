from pathlib import Path

from astropy.io import fits

PATH_HERE = Path(__file__).parent
PATH_OUTPUT = PATH_HERE / "output"

print(PATH_OUTPUT)

ks_toplevel_allowed = {"ESO", "WISE"}

fns_fits = PATH_OUTPUT.glob("*.fits")

for fn_fits in fns_fits:
    print(fn_fits)
    hdus = fits.open(fn_fits)
    for hdu in hdus:
        for card in hdu.header.cards:
            k, v, c = card
            ks = k.split()
            # Assert keyword is uppercase.
            assert k.upper() == k, k
            # Assert HIERARCH keywords start with allowed top level key.
            if len(ks) > 1:
                assert ks[0] in ks_toplevel_allowed, k
            # Assert all subsystems in HIERARCH keyword are max 8 characters.
            assert all(len(ki) <= 8 for ki in ks), k
