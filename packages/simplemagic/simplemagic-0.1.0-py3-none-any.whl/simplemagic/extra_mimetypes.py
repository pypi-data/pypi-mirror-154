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

    "text/x-script.python": [".py"],
    "text/x-script.perl": [".pl"],
    "text/x-script.shell": [".sh"],
    "text/x-python": [".py"],
    "text/x-shellscript": [".sh"],
    "text/x-perl": [".pl"],
    "text/x-java": [".java"],
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
    # fix some old libimage treat java source code as c source code.
    "text/x-c": [".java",],
    # fix for .dat
    "application/octet-stream": [
        ".data",
        ".dat",
        ".bin",
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
    ]
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
