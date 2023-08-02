import io
from pathlib import Path

from elftools.elf.elffile import ELFFile

from capa.features.extractors.elffile import extract_file_export_names, extract_file_import_names

CD = Path(__file__).resolve().parent
SAMPLE_PATH = CD / "data" / "055da8e6ccfe5a9380231ea04b850e18.elf_"


def test_elffile_import_features():
    expected_imports = [
        "memfrob",
        "puts",
        "__libc_start_main",
        "malloc",
        "__cxa_finalize",
        "memfrob@@GLIBC_2.2.5",
        "puts@@GLIBC_2.2.5",
        "__libc_start_main@@GLIBC_2.2.5",
        "malloc@@GLIBC_2.2.5",
        "__cxa_finalize@@GLIBC_2.2.5",
    ]
    path = Path(SAMPLE_PATH)
    elf = ELFFile(io.BytesIO(path.read_bytes()))
    # Extract imports
    imports = list(extract_file_import_names(elf))

    # Verify that at least one import was found
    assert len(imports) > 0, "No imports were found."

    # Extract the symbol names from the extracted imports
    extracted_symbol_names = [imported[0].value for imported in imports]

    # Check if all expected symbol names are found
    for symbol_name in expected_imports:
        assert symbol_name in extracted_symbol_names, f"Symbol '{symbol_name}' not found in imports."


def test_elffile_export_features():
    expected_exports = [
        "deregister_tm_clones",
        "register_tm_clones",
        "__do_global_dtors_aux",
        "completed.8060",
        "__do_global_dtors_aux_fini_array_entry",
        "frame_dummy",
        "_init",
        "__libc_csu_fini",
        "_fini",
        "__dso_handle",
        "_IO_stdin_used",
        "__libc_csu_init",
    ]
    path = Path(SAMPLE_PATH)
    elf = ELFFile(io.BytesIO(path.read_bytes()))
    # Extract imports
    exports = list(extract_file_export_names(elf))

    # Verify that at least one export was found
    assert len(exports) > 0, "No exports were found."

    # Extract the symbol names from the extracted imports
    extracted_symbol_names = [exported[0].value for exported in exports]

    # Check if all expected symbol names are found
    for symbol_name in expected_exports:
        assert symbol_name in extracted_symbol_names, f"Symbol '{symbol_name}' not found in exports."
