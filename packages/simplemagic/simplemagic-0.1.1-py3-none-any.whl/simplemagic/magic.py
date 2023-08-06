
import os
import logging
import subprocess
import puremagic
from binaryornot.helpers import is_binary_string

from . import fixpuremagic # required
from .utils import SafeStreamReader
from .extra_mimetypes import get_mimetype_by_extension

USING_FILE_COMMAND = True
USING_PUREMAGIC = True
try:
    import magic
    from . import fixmagic # required
    USING_MAGIC = True
except:
    magic = None
    USING_MAGIC = False

from .extra_mimetypes import guess_all_extensions

FILE_COMMAND = "file"
MAGIC_CONTENT_LENGTH = 1024*64
MIMETYPE_FOR_TEXT = "text/plain"
MIMETYPE_FOR_BINARY = "application/octet-stream"
PRIORITY_EXTS = [
    ".zip",
]

logger = logging.getLogger(__name__)

def disable_using_magic():
    global USING_MAGIC
    USING_MAGIC = False

def enable_using_magic():
    global USING_MAGIC
    USING_MAGIC = True

def disable_using_puremagic():
    global USING_PUREMAGIC
    USING_PUREMAGIC = False

def enable_using_puremagic():
    global USING_PUREMAGIC
    USING_PUREMAGIC = True

def disable_using_file_command():
    global USING_FILE_COMMAND
    USING_FILE_COMMAND = False

def enable_using_file_command():
    global USING_FILE_COMMAND
    USING_FILE_COMMAND = True

def set_file_command(cmd):
    global FILE_COMMAND
    FILE_COMMAND = cmd


def get_mimetype_simple_by_stream(stream, filename=None):
    with SafeStreamReader(stream) as stream:
        data = stream.read(MAGIC_CONTENT_LENGTH)
        if is_binary_string(data):
            return MIMETYPE_FOR_BINARY
        else:
            return MIMETYPE_FOR_TEXT


def get_mimetype_simple_by_filename(filename):
    with open(filename, "rb") as fobj:
        data = fobj.read(MAGIC_CONTENT_LENGTH)
        if is_binary_string(data):
            return MIMETYPE_FOR_BINARY
        else:
            return MIMETYPE_FOR_TEXT


def get_mimetype_using_file_command_by_stream(stream, filename=None):
    with SafeStreamReader(stream) as stream:
        content = stream.read(MAGIC_CONTENT_LENGTH)
        proc = subprocess.Popen(
            [FILE_COMMAND, "--mime-type", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
            )
        proc.stdin.buffer.write(content)
        proc.stdin.buffer.close()
        proc.wait(1)
        output = proc.stdout.readlines()
        if output:
            return output[0].split(":")[1].strip()
        return get_mimetype_simple_by_stream(stream, filename=filename)


def get_mimetype_using_file_command_by_filename(filename):
    proc = subprocess.Popen(
        [FILE_COMMAND, "--mime-type", filename],
        stdout=subprocess.PIPE,
        universal_newlines=True,
        )
    proc.wait(1)
    output = proc.stdout.readlines()
    if output:
        return output[0].split(":")[1].strip()
    return get_mimetype_simple_by_filename(filename)


def get_mimetype_using_magic_by_stream(stream, filename=None):
    with SafeStreamReader(stream) as stream:
        content = stream.read(MAGIC_CONTENT_LENGTH)
        result = magic.detect_from_content(content)
        if result:
            return result.mime_type
        else:
            return None

def get_mimetype_using_magic_by_filename(filename):
    result = magic.detect_from_filename(filename)
    if result:
        return result.mime_type
    else:
        return None

def _get_best_mimetype_from_puremagic_result(guessed_types, ext):
    if not guessed_types:
        return None

    mimetype = None
    if not mimetype:
        for guessed_type in guessed_types:
            if guessed_type.extension == ext:
                if guessed_type.mime_type:
                    mimetype = guessed_type.mime_type
                    break
                else:
                    mimetype = get_mimetype_by_extension(guessed_type.extension)
                    if mimetype:
                        break

    if not mimetype:
        for guessed_type in guessed_types:
            if guessed_type.confidence > 0.5:
                if guessed_type.mime_type:
                    mimetype = guessed_type.mime_type
                    break
                else:
                    mimetype = get_mimetype_by_extension(guessed_type.extension)
                    if mimetype:
                        break
    
    if not mimetype:
        for guessed_type in guessed_types:
            if guessed_type.extension in PRIORITY_EXTS:
                if guessed_type.mime_type:
                    mimetype = guessed_type.mime_type
                    break
                else:
                    mimetype = get_mimetype_by_extension(guessed_type.extension)
                    break
    
    if not mimetype:
        if guessed_types[0].mime_type:
            mimetype = guessed_types[0].mime_type
        else:
            mimetype = guessed_types[0].mime_type

    return mimetype



def get_mimetype_using_puremagic_by_stream(stream, filename):
    with SafeStreamReader(stream) as stream:
        try:
            guessed_types = puremagic.magic_stream(stream, filename=filename)
            ext = os.path.splitext(filename)[1]
            return _get_best_mimetype_from_puremagic_result(guessed_types, ext)
        except Exception:
            return None

def get_mimetype_using_puremagic_by_filename(filename):
    try:
        guessed_types = puremagic.magic_file(filename)
        ext = os.path.splitext(filename)[1]
        return _get_best_mimetype_from_puremagic_result(guessed_types, ext)
    except Exception:
        return None


def get_mimetype_by_stream(stream, filename, enable_using_magic=True, enable_using_file_command=True, enable_using_puremagic=True):
    mimetype = None
    if (not mimetype) and magic and USING_MAGIC and enable_using_magic:
        try:
            mimetype = get_mimetype_using_magic_by_stream(stream, filename)
        except Exception as error:
            logger.warning("get mimetype using magic by stream failed: {error}...".format(error=error))
    if (not mimetype) and USING_FILE_COMMAND and enable_using_file_command:
        try:
            mimetype = get_mimetype_using_file_command_by_stream(stream, filename)
        except Exception as error:
            logger.warning("get mimetype using file command by stream failed: {error}...".format(error=error))
    if (not mimetype) and USING_PUREMAGIC and enable_using_puremagic:
        try:
            mimetype = get_mimetype_using_puremagic_by_stream(stream, filename)
        except Exception as error:
            logger.warning("get mimetype using puremagic by stream failed: {error}...".format(error=error))
    if not mimetype:
        mimetype = get_mimetype_simple_by_stream(stream, filename)
    return mimetype


def get_mimetype_by_filename(filename, enable_using_magic=True, enable_using_file_command=True, enable_using_puremagic=True):
    mimetype = None
    if (not mimetype) and magic and USING_MAGIC and enable_using_magic:
        try:
            mimetype = get_mimetype_using_magic_by_filename(filename)
        except Exception as error:
            logger.warning("get mimetype using magic by filename failed: {error}...".format(error=error))
    if (not mimetype) and USING_FILE_COMMAND and enable_using_file_command:
        try:
            mimetype = get_mimetype_using_file_command_by_filename(filename)
        except Exception as error:
            logger.warning("get mimetype using file command by filename failed: {error}...".format(error=error))
    if (not mimetype) and USING_PUREMAGIC and enable_using_puremagic:
        try:
            mimetype = get_mimetype_using_puremagic_by_filename(filename)
        except Exception as error:
            logger.warning("get mimetype using puremagic by filename failed: {error}...".format(error=error))
    if not mimetype:
        mimetype = get_mimetype_simple_by_filename(filename)
    return mimetype


def is_file_content_matches_with_file_suffix(filename, stream=None, enable_using_magic=True, enable_using_file_command=True, enable_using_puremagic=True):
    if stream:
        mimetype = get_mimetype_by_stream(stream, filename=filename, enable_using_magic=enable_using_magic, enable_using_file_command=enable_using_file_command, enable_using_puremagic=enable_using_puremagic)
    else:
        mimetype = get_mimetype_by_filename(filename, enable_using_magic=enable_using_magic, enable_using_file_command=enable_using_file_command, enable_using_puremagic=enable_using_puremagic)
    ext = os.path.splitext(filename)[1]
    exts = guess_all_extensions(mimetype)
    if ext in exts:
        return True
    else:
        return False
