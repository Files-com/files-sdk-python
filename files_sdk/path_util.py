import unicodedata

TRANSLIT_MAP = {
    entry[0]: entry[1:]
    for entry in "ÀA,ÁA,ÂA,ÃA,ÄA,ÅA,ÆAE,ÇC,ÈE,ÉE,ÊE,ËE,ÌI,ÍI,ÎI,ÏI,ÐD,ÑN,ÒO,ÓO,ÔO,ÕO,ÖO,ØO,ÙU,ÚU,ÛU,ÜU,ÝY,ßss,àa,áa,âa,ãa,äa,åa,æae,çc,èe,ée,êe,ëe,ìi,íi,îi,ïi,ðd,ñn,òo,óo,ôo,õo,öo,øo,ùu,úu,ûu,üu,ýy,ÿy,ĀA,āa,ĂA,ăa,ĄA,ąa,ĆC,ćc,ĈC,ĉc,ĊC,ċc,ČC,čc,ĎD,ďd,ĐD,đd,ĒE,ēe,ĔE,ĕe,ĖE,ėe,ĘE,ęe,ĚE,ěe,ĜG,ĝg,ĞG,ğg,ĠG,ġg,ĢG,ģg,ĤH,ĥh,ĦH,ħh,ĨI,ĩi,ĪI,īi,ĬI,ĭi,ĮI,įi,İI,ĲIJ,ĳij,ĴJ,ĵj,ĶK,ķk,ĹL,ĺl,ĻL,ļl,ĽL,ľl,ŁL,łl,ŃN,ńn,ŅN,ņn,ŇN,ňn,ŉ'n,ŌO,ōo,ŎO,ŏo,ŐO,őo,ŒOE,œoe,ŔR,ŕr,ŖR,ŗr,ŘR,řr,ŚS,śs,ŜS,ŝs,ŞS,şs,ŠS,šs,ŢT,ţt,ŤT,ťt,ŨU,ũu,ŪU,ūu,ŬU,ŭu,ŮU,ůu,ŰU,űu,ŲU,ųu,ŴW,ŵw,ŶY,ŷy,ŸY,ŹZ,źz,ŻZ,żz,ŽZ,žz".split(
        ","
    )
}


def _cleanpath(path_element: str) -> bool:
    return path_element not in ["", ".", ".."]


def is_same(a: str, b: str) -> bool:
    return normalize_for_comparison(a) == normalize_for_comparison(b)


def normalize_for_comparison(path_str: str) -> str:
    return (
        unicode_normalize_and_transliterate(normalize(path_str))
        .lower()
        .rstrip()
    )


def normalize(path_str: str) -> str:
    return "/".join(
        filter(
            _cleanpath,
            path_str.replace("\x00", "").replace("\\", "/").split("/"),
        )
    )


def unicode_normalize_and_transliterate(path_str: str) -> str:
    # convert multi-code-point characters into single-code-point characters
    normalized_string = unicodedata.normalize("NFKC", path_str)

    return "".join(
        [TRANSLIT_MAP.get(char, char) for char in normalized_string]
    )
