import mimetypes

EXTRA_MIMETYPE_EXTENSIONS = {
    None: [],

    "application/x-bytecode.python": [".pyc"],
    "application/x-rar": [".rar"],
    "application/x-mach-binary": [".so"],
    "application/x-rpm": [".rpm"],
    "application/x-dosexec": [".exe", ".dll"],
    "application/x-makefile": [".txt", ".am", ".m4"],
    "application/x-archive": [".lib"],
    "application/x-yaml": [".yml", ".yaml"],
    "application/vnd.sqlite3": [".coverage", ".db", ".sqlite3", ".sqlite"],
    "application/gzip": [".gz"],
    "application/x-gzip": [".gz"],
    "application/x-bzip2": [".bz2", ".bzip2", ".tbz2", ".tb2"],

    "text/x-script.python": [".py", ".java", ".go"], # language has import may missing detected by puremagic
    "text/x-script.perl": [".pl"],
    "text/x-script.shell": [".sh"],
    "text/x-python": [".py", ".java", ".go"], # language has import may missing detected by puremagic
    "text/x-shellscript": [".sh"],
    "text/x-perl": [".pl"],
    "text/x-java": [".java", ".py", ".go"], # language has import may missing detected by puremagic
    "text/troff": [".1"],
    "text/PGP": [".txt", ""],
    # fix for zip based files
    "application/zip": [
        ".whl",
        ".pages",
        ".xmind",
        ".wps",
        ".wpt",
    ],
    # fix for wps
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
        ".docx",
        ".doc",
        ".dot",
        ".wps",
        ".wpt",
    ],
    # 'application/vnd.binary' equivalent to 'application/octet-stream'
    "application/vnd.binary": [
        "",
        ".a",
        ".bin",
        ".bpk",
        ".dat",
        ".data",
        ".deploy",
        ".dist",
        ".distz",
        ".dll",
        ".dms",
        ".dump",
        ".elc",
        ".exe",
        ".lrf",
        ".mar",
        ".mobipocket-ebook",
        ".o",
        ".obj",
        ".pkg",
        ".so",
    ],
    # fix for .dat, data
    "application/octet-stream": [
        "",
        ".a",
        ".bin",
        ".bpk",
        ".dat",
        ".data",
        ".deploy",
        ".dist",
        ".distz",
        ".dll",
        ".dms",
        ".dump",
        ".elc",
        ".exe",
        ".lrf",
        ".mar",
        ".mobipocket-ebook",
        ".o",
        ".obj",
        ".pkg",
        ".so",
    ],
    # fix for text/xml
    "text/xml": [
        ".xml",
        ".xsl",
        ".wsdl",
    ],
    # fix for programming source code and config files
    "text/plain": [
        "",
        ".gitignore",
        ".py",
        ".pl",
        ".sh",
        ".pl",
        ".java",
        ".c",
        ".h",
        ".hpp",
        ".cpp",
        ".json",
        ".yml",
        ".yaml",
        ".sql",
        ".css",
        ".js",
        ".json",
        ".django",
        ".html",
        ".htm",
        ".xml",
        ".xsl",
        ".out",
        ".jsp",
        ".php",
        ".log",
        ".conf",
        ".cnf",
        ".ini",
        ".properties",
        ".rules",
        ".cnf",
        ".pem",
        ".pub",
        ".crt",
        ".key",
        ".cmd",
        ".bat",
        ".pxd",
        ".pyi",
        ".md",
        ".rst",
        ".in",
    ],
    # ===================================================================
    # Hacks
    # ===================================================================

    # fix some old libimage treat java source code as c source code.
    "text/x-c": [".java",],
}

def register_mimetype_extensions(mimetype, exts):
    if isinstance(extra_exts, str):
        extra_exts = [extra_exts]
    if mimetype in EXTRA_MIMETYPE_EXTENSIONS:
        EXTRA_MIMETYPE_EXTENSIONS[mimetype] += exts
    else:
        EXTRA_MIMETYPE_EXTENSIONS[mimetype] = [] + exts

def guess_all_extensions(mimetype):
    mimetype = mimetype or "text/plain"
    exts =  mimetypes.guess_all_extensions(mimetype)
    extra_exts = EXTRA_MIMETYPE_EXTENSIONS.get(mimetype, [])
    result = list(set(exts + extra_exts))
    result.sort()
    return result

def get_mimetype_by_extension(ext):
    mimetype = mimetypes.types_map.get(ext, None)
    if not mimetype:
        for mt, exts in EXTRA_MIMETYPE_EXTENSIONS.items():
            if ext in exts:
                return mt
    return None

    