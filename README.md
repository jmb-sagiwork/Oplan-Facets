# FACETS Click Test

This proof-of-concept Windows automation script connects to an existing FACETS
window and double-clicks the TreeItem named `Hospital Claims Processing`.

It uses only `pywinauto` with the UIA backend. It does not use image
recognition, OCR, or coordinate-based clicking.

## Download

[Download FacetsClickTest.exe](https://github.com/jmb-sagiwork/Oplan-Facets/raw/refs/heads/main/dist/FacetsClickTest.exe)

## Requirements

- Windows
- Python 3
- An open and accessible FACETS window titled `Facets`

## Install

From PowerShell in this directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

Open FACETS and make sure the target tree item is visible, then run:

```powershell
python test_facets_click.py
```

The script waits up to 15 seconds for the FACETS window and target TreeItem. If
it cannot find them, it prints diagnostic visible window titles or visible
TreeItem names.

## Build An EXE

Build the executable on a Windows machine:

```powershell
python -m pip install pyinstaller
pyinstaller --onefile --console --name FacetsClickTest test_facets_click.py
```

Expected output:

```text
dist/FacetsClickTest.exe
```

If PyInstaller reports missing imports at runtime, rebuild with the optional
hidden imports:

```powershell
pyinstaller --onefile --console --name FacetsClickTest `
  --hidden-import pywinauto `
  --hidden-import comtypes `
  --hidden-import comtypes.client `
  --hidden-import comtypes.gen `
  --hidden-import comtypes.stream `
  test_facets_click.py
```

Run the packaged test while FACETS is open:

```powershell
.\dist\FacetsClickTest.exe
```

The EXE must be built and run on Windows because FACETS and `pywinauto` depend
on Windows UI Automation.
