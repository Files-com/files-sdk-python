import datetime
from pathlib import Path
from files_com.api import Api
from files_com.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class File:
    default_attributes = {
        'id': None,     # int64 - File/Folder ID
        'path': None,     # string - File/Folder path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        'display_name': None,     # string - File/Folder display name
        'type': None,     # string - Type: `directory` or `file`.
        'size': None,     # int64 - File/Folder size
        'mtime': None,     # date-time - File last modified date/time, according to the server.  This is the timestamp of the last Files.com operation of the file, regardless of what modified timestamp was sent.
        'provided_mtime': None,     # date-time - File last modified date/time, according to the client who set it.  Files.com allows desktop, FTP, SFTP, and WebDAV clients to set modified at times.  This allows Desktop<->Cloud syncing to preserve modified at times.
        'crc32': None,     # string - File CRC32 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        'md5': None,     # string - File MD5 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        'mime_type': None,     # string - MIME Type.  This is determined by the filename extension and is not stored separately internally.
        'region': None,     # string - Region location
        'permissions': None,     # string - A short string representing the current user's permissions.  Can be `r`,`w`,`p`, or any combination
        'subfolders_locked?': None,     # boolean - Are subfolders locked and unable to be modified?
        'download_uri': None,     # string - Link to download file. Provided only in response to a download request.
        'priority_color': None,     # string - Bookmark/priority color of file/folder
        'preview_id': None,     # int64 - File preview ID
        'preview': None,     # File preview
        'action': None,     # string - The action to perform.  Can be `append`, `attachment`, `end`, `upload`, `put`, or may not exist
        'length': None,     # int64 - Length of file.
        'mkdir_parents': None,     # boolean - Create parent directories if they do not exist?
        'part': None,     # int64 - Part if uploading a part.
        'parts': None,     # int64 - How many parts to fetch?
        'ref': None,     # string -
        'restart': None,     # int64 - File byte offset to restart from.
        'structure': None,     # string - If copying folder, copy just the structure?
        'with_rename': None,     # boolean - Allow file rename instead of overwrite?
    }

    def __init__(self, *args):
        self.set_attributes({})
        self.options = {}
        self.mode = 'r'
        self.write_io = None # TODO: make this StringIO.new python style
        self.bytes_written = 0
        if len(args) >= 1:
            if isinstance(args[0], dict):
                self.set_attributes(args[0])
            elif isinstance(args[0], str):
                self.set_attributes({"path": args[0]})
        if len(args) >= 2:
            if isinstance(args[1], dict):
                self.options = args[1]
            elif isinstance(args[1], str):
                self.mode = args[1]
        if len(args) >= 3:
            if isinstance(args[2], dict):
                self.options = args[2]

    def set_attributes(self, attributes):
        for (attribute, default_value) in File.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in File.default_attributes}

    # def self.binread(name, *args)
    #   new(name).read(*args)
    # end

    # def self.binwrite(name, *args)
    #   new(name).write(*args)
    # end

    # def self.chmod(*_args)
    #   raise NotImplementedError
    # end

    # def self.chown(*_args)
    #   raise NotImplementedError
    # end

    # def self.client(options = {})
    #   options[:client] || ApiClient.active_client
    # end

    # def self.copy(old_path, new_path)
    #   FileAction.copy(old_path, destination: new_path)
    # end

    # def self.copy_stream(*_args)
    #   raise NotImplementedError
    # end

    # def self.directory?(path, options = {})
    #   find(path, {}, options).type == "directory"
    # end

    # def self.exist?(path, options = {})
    #   find(path, {}, options)
    #   true
    # rescue Error => e
    #   if e.code == 404
    #     false
    #   else
    #     raise e
    #   end
    # end

    # def self.exists?(path, options = {})
    #   exist?(path, options)
    # end

    # def self.for_fd(*_args)
    #   raise NotImplementedError
    # end

    # def self.foreach(name, *args, &block)
    #   new(name).each(*args, &block)
    # end

    # def self.get(path, params = {}, options = {})
    #   find(path, params, options)
    # end

    # def self.identical?(path1, path2)
    #   new(path1).crc32 == new(path2).crc32
    # end

    # def self.lstat(path)
    #   new(path).stat
    # end

    # def self.move(old_path, new_path)
    #   FileAction.move(old_path, destination: new_path)
    # end

    # def self.mtime(path)
    #   new(path).mtime
    # end

    # def self.open(path, mode = "r", options = {}, &block)
    #   file = new(path, mode, options)
    #   if block
    #     yield file
    #     file.close
    #   end
    #   file
    # end

    # def self.owned?(_path)
    #   raise NotImplementedError
    # end

    # def self.pipe(*_args)
    #   raise NotImplementedError
    # end

    # def self.popen(*_args)
    #   raise NotImplementedError
    # end

    # def self.read(name, *args)
    #   new(name).read(*args)
    # end

    # def self.readable?(path)
    #   new(path).stat.permissions.include?("read")
    # end

    # def self.readlines(name, *args)
    #   new(name).readlines(*args)
    # end

    # def self.rename(old_path, new_path)
    #   FileAction.move(old_path, destination: new_path)
    # end

    # def self.select(*_args)
    #   raise NotImplementedError
    # end

    # def self.stat(path)
    #   new(path).stat
    # end

    # def self.sysopen(*_args)
    #   raise NotImplementedError
    # end

    # def self.try_convert(*_args)
    #   raise NotImplementedError
    # end

    # def self.unlink(*paths)
    #   paths.map { |p| delete(p) }
    # end

    # def self.upload_chunks(io, path, options, upload = nil, etags = [])
    #   etags ||= []
    #   bytes_written = 0
    #   loop do
    #     begin_upload = FileAction.begin_upload(path, { ref: upload&.ref, part: (upload&.part_number || 0) + 1 }, options)
    #     upload = begin_upload.is_a?(Enumerable) ? begin_upload.first : begin_upload
    #     buf = io.read(upload.partsize) || ""
    #     bytes_written += buf.length
    #     method = upload.http_method.downcase.to_sym
    #     response = client(options).remote_request(method, upload.upload_uri, { "Content-Length": buf.length.to_s }, buf)
    #     etags << { etag: response.headers["ETag"], part: upload.part_number }
    #     return upload, etags, bytes_written if io.eof?
    #   end
    # end

    # def self.write(*_args)
    #   raise NotImplementedError
    # end

    # def self.zero?(path)
    #   new(path).empty?
    # end

    # def initialize(*args)
    #   @attributes = (args[0].is_a?(Hash) && args[0]) || {}
    #   @options = (args[1].is_a?(Hash) && args[1])
    #   @options ||= (args[2].is_a?(Hash) && args[2]) || {}
    #   @attributes[:path] = args[0] if args[0].is_a?(String)
    #   @mode = args[1] || 'r' if args[1].is_a?(String)
    #   @write_io = StringIO.new
    #   @bytes_written = 0
    # end

    # def advise(*_args); end

    # def atime
    #   mtime
    # end

    # def autoclose=(*_args); end

    # def autoclose?(*_args); end

    # def binmode
    #   binmode?
    # end

    # def binmode?
    #   true
    # end

    # def birthtime
    #   raise NotImplementedError
    # end

    # def bytes
    #   read_io.bytes
    # end

    # def chars
    #   read_io.chars
    # end

    # def chmod(*_args)
    #   raise NotImplementedError
    # end

    # def chown(*_args)
    #   raise NotImplementedError
    # end

    # def client
    #   options[:client] || ApiClient.active_client
    # end

    # def close
    #   flush

    #   if @upload
    #     end_options = {
    #       "action": "end",
    #       "etags": @etags,
    #       "provided_mtime": Time.now.to_s,
    #       "ref": @upload.ref,
    #       "size": @bytes_written
    #     }

    #     file = File.create(path, end_options, @options)
    #     @attributes = file.attributes
    #     @upload = nil
    #   end
    #   @write_io.close
    # end

    # def close_on_exec?(*args)
    #   @write_io.close_on_exec? *args
    # end

    # def close_on_exec=(*args)
    #   @write_io.close_on_exec = *args
    # end

    # def close_read(*args)
    #   @write_io.close_read *args
    # end

    # def close_write(*args)
    #   @write_io.close_write *args
    # end

    # def closed?(*args)
    #   @write_io.closed? *args
    # end

    # def codepoints(*args, &block)
    #   @write_io.codepoints *args, &block
    # end

    # def copy(destination)
    #   File.copy(path, destination)
    # end

    # def ctime(*_args)
    #   mtime
    # end


    # def each(*args, &block)
    #   read_io.each *args, &block
    # end

    # def each_byte(*args, &block)
    #   read_io.each_byte *args, &block
    # end

    # def each_char(*args, &block)
    #   read_io.each_char *args, &block
    # end

    # def each_codepoint(*args, &block)
    #   read_io.each_codepoint *args, &block
    # end

    # def each_line(*args, &block)
    #   each(*args, &block)
    # end

    # def empty?
    #   size == 0
    # end

    # def eof
    #   eof?
    # end

    # def eof?
    #   @write_io.eof?
    # end

    # def external_encoding(*args)
    #   internal_encoding *args
    # end

    # def fcntl(*_args)
    #   raise NotImplementedError
    # end

    # def fdatasync(*_args)
    #   flush
    # end

    # def fileno(*_args)
    #   id
    # end

    # def flock(*_args)
    #   raise NotImplementedError
    # end

    # def flush(*_args)
    #   if mode.include? "w"
    #     @write_io.rewind if @write_io.is_a?(StringIO)

    #     @upload, @etags, bytes_written = File.upload_chunks(@write_io, path, options, @upload, @etags)
    #     @bytes_written += bytes_written
    #   elsif mode.include? "a"
    #     raise NotImplementedError
    #   end
    # end

    # def fsync(*args)
    #   flush *args
    # end

    # def getbyte(*args)
    #   read_io.getbyte *args
    # end

    # def getc(*args)
    #   read_io.getc *args
    # end

    # def gets(*args)
    #   read_io.gets *args
    # end

    # def read_io
    #   @read_io ||= begin
    #                  r, w = SizableIO.pipe
    #                  Thread.new do
    #                    download_content(w)
    #                  ensure
    #                    w.close
    #                  end
    #                  r
    #                end
    # end

    # def internal_encoding(*_args)
    #   "".encoding
    # end

    # def ioctl(*_args)
    #   raise NotImplementedError
    # end

    # def isatty(*_args)
    #   false
    # end

    # def lineno(*_args)
    #   @lineno ||= 0
    # end

    # attr_writer :lineno

    # def lines(*args, &block)
    #   each_line *args, &block
    # end

    # def lstat(*_args)
    #   stats
    # end

    # def move(destination)
    #   File.move(path, destination)
    # end

    # def mv(destination)
    #   File.move(path, destination)
    # end

    # def pid(*_args)
    #   Process.pid
    # end

    # def pos
    #   @pos ||= 0
    # end

    # attr_writer :pos

    # def pread(*args)
    #   read_io.pread *args
    # end

    # def print(*args)
    #   @write_io.print *args
    # end

    # def printf(*args)
    #   @write_io.printf *args
    # end

    # def putc(*args)
    #   @write_io.putc *args
    # end

    # def puts(*args)
    #   @write_io.puts *args
    # end

    # def pwrite(*args)
    #   @write_io.pwrite *args
    # end

    # def read(*args)
    #   read_io.read *args
    # end

    # def read_nonblock(*args)
    #   read_io.read_nonblock *args
    # end

    # def readbyte(*args)
    #   read_io.readbyte *args
    # end

    # def readchar(*args)
    #   read_io.readchar *args
    # end

    # def readline(*args)
    #   read_io.readline *args
    # end

    # def readlines(*args)
    #   io.readlines(*args)
    # end

    # def readpartial(*args)
    #   read_io.readpartial *args
    # end

    # def rename(destination)
    #   File.rename(path, destination)
    # end

    # def reopen(*_args)
    #   raise NotImplementedError
    # end

    # def rewind
    #   @pos = 0
    # end

    # def seek(pos)
    #   @pos = pos
    # end

    # def set_encoding(*_args) # rubocop:disable Naming/AccessorMethodName
    #   raise NotImplementedError
    # end

    # def stat(*_args)
    #   stats
    # end

    # def sync
    #   @sync ||= false
    # end

    # attr_writer :sync

    # def sysread(*args)
    #   read *args
    # end

    # def sysseek(*args)
    #   seek *args
    # end

    # def syswrite(*_args)
    #   raise NotImplementedError
    # end

    # def tell
    #   pos
    # end

    # def to_i(*_args)
    #   fileno
    # end

    # def to_io(*_args)
    #   @write_io
    # end

    # def to_path(*_args)
    #   path
    # end

    # def truncate(*_args)
    #   raise NotImplementedError
    # end

    # def tty?(*_args)
    #   false
    # end

    # def ungetbyte(*_args)
    #   raise NotImplementedError
    # end

    # def ungetc(*_args)
    #   raise NotImplementedError
    # end

    # def upload_file(local_file)
    #   File.upload_file(local_file.path)
    # end

    # def write(*args)
    #   @mode ||= 'w'
    #   if args[0].respond_to?(:read)
    #     flush if @write_io.size > 0 # rubocop:disable Style/ZeroLengthPredicate
    #     @write_io = args[0]
    #   else
    #     @write_io.write *args
    #   end
    # end

    # def write_nonblock(*args)
    #   @write_io.write_nonblock *args
    # end

    @staticmethod
    def do_upload_chunks(io, path, options, upload = None, etags = []):
        if not etags:
            etags = []
        bytes_written = 0
        # TODO pick back up here
#        while True:
#            begin_upload = FileAction.begin_upload(path, { ref: upload&.ref, part: (upload&.part_number || 0) + 1 }, options)
#            upload = begin_upload.is_a?(Enumerable) ? begin_upload.first : begin_upload
#            buf = io.read(upload.partsize) || ""
#            bytes_written += buf.length
#            method = upload.http_method.downcase.to_sym
#            response = client(options).remote_request(method, upload.upload_uri, { "Content-Length": buf.length.to_s }, buf)
#            etags << { etag: response.headers["ETag"], part: upload.part_number }
#            return upload, etags, bytes_written if io.eof?

    @staticmethod
    def do_upload_file(path, destination = None, options = {}):
        pth = Path(path)
        stat = pth.stat()
        with File.open(path, 'r') as local_file:
            if not destination:
                destination = pth.name
                upload, etags = upload_chunks(local_file, destination, options)

            params = {
              action: "end",
              etags: etags,
              provided_mtime: stat.st_mtime.to_s,
              ref: upload.ref,
              size: stat.st_size
            }

            File.do_create(destination, params, options)

    def download_uri_with_load(self):
        if self.download_uri:
            return self.download_uri 

        f = File.do_download(self.path, {}, self.options)
        self.set_attributes(f.get_attributes())
        return self.download_uri

    def download_content(self, io):
        Api.api_client().stream_download(self.download_uri_with_load(), io)

    def download_file(self, output_file):
        with open(output_file, 'wb') as file:
        #::File.open(output_file, 'wb') do |file|
            self.download_content(file)

    @staticmethod
    def do_download_file(path, local_path = None):
        if not local_path:
            local_path = Path(path).name
        return File(path).download_file(local_path)

    @staticmethod
    def do_find(path, params = {}, options = {}):
        params["action"] = "stat"
        return File.do_download(path, params, options)

    # Download file
    #
    # Parameters:
    #   action - string - Can be blank, `redirect` or `stat`.  If set to `stat`, we will return file information but without a download URL, and without logging a download.  If set to `redirect` we will serve a 302 redirect directly to the file.  This is used for integrations with Zapier, and is not recommended for most integrations.
    #   preview_size - string - Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
    #   with_previews - boolean - Include file preview information?
    #   with_priority_color - boolean - Include file priority color information?
    def download(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "path") and self.path:
            params['path'] = self.path
        else:
            raise MissingParameterError("Current object doesn't have a path")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "preview_size" in params and not isinstance(params["preview_size"], str):
            raise InvalidParameterError("Bad parameter: preview_size must be an str")
        return Api.send_request("GET", "/files/{path}".format(path=params['path']), params, self.options)

    # Parameters:
    #   provided_mtime - string - Modified time of file.
    #   priority_color - string - Priority/Bookmark color of file.
    def update(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "path") and self.path:
            params['path'] = self.path
        else:
            raise MissingParameterError("Current object doesn't have a path")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "provided_mtime" in params and not isinstance(params["provided_mtime"], str):
            raise InvalidParameterError("Bad parameter: provided_mtime must be an str")
        if "priority_color" in params and not isinstance(params["priority_color"], str):
            raise InvalidParameterError("Bad parameter: priority_color must be an str")
        return Api.send_request("PATCH", "/files/{path}".format(path=params['path']), params, self.options)

    # Parameters:
    #   recursive - boolean - If true, will recursively delete folers.  Otherwise, will error on non-empty folders.  For legacy reasons, this parameter may also be provided as the HTTP header `Depth: Infinity`
    def delete(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "path") and self.path:
            params['path'] = self.path
        else:
            raise MissingParameterError("Current object doesn't have a path")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        return Api.send_request("DELETE", "/files/{path}".format(path=params['path']), params, self.options)

    def destroy(self, params = {}):
        self.delete(params)

    def save(self):
        if hasattr(self, "path") and self.path:
            self.update(self.get_attributes())
        else:
            new_obj = File.do_create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

    # Download file
    #
    # Parameters:
    #   action - string - Can be blank, `redirect` or `stat`.  If set to `stat`, we will return file information but without a download URL, and without logging a download.  If set to `redirect` we will serve a 302 redirect directly to the file.  This is used for integrations with Zapier, and is not recommended for most integrations.
    #   preview_size - string - Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
    #   with_previews - boolean - Include file preview information?
    #   with_priority_color - boolean - Include file priority color information?
    @staticmethod
    def do_download(path, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["path"] = path
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "preview_size" in params and not isinstance(params["preview_size"], str):
            raise InvalidParameterError("Bad parameter: preview_size must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")

        response, options = Api.send_request("GET", "/files/{path}".format(path=params['path']), params, options)
        return File(response.data, options)
    
    # Parameters:
    #   path (required) - string - Path to operate on.
    #   action - string - The action to perform.  Can be `append`, `attachment`, `end`, `upload`, `put`, or may not exist
    #   etags[etag] (required) - array(string) - etag identifier.
    #   etags[part] (required) - array(int64) - Part number.
    #   length - int64 - Length of file.
    #   mkdir_parents - boolean - Create parent directories if they do not exist?
    #   part - int64 - Part if uploading a part.
    #   parts - int64 - How many parts to fetch?
    #   provided_mtime - string - User provided modification time.
    #   ref - string -
    #   restart - int64 - File byte offset to restart from.
    #   size - int64 - Size of file.
    #   structure - string - If copying folder, copy just the structure?
    #   with_rename - boolean - Allow file rename instead of overwrite?
    @staticmethod
    def do_create(path, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["path"] = path
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "length" in params and not isinstance(params["length"], int):
            raise InvalidParameterError("Bad parameter: length must be an int")
        if "part" in params and not isinstance(params["part"], int):
            raise InvalidParameterError("Bad parameter: part must be an int")
        if "parts" in params and not isinstance(params["parts"], int):
            raise InvalidParameterError("Bad parameter: parts must be an int")
        if "provided_mtime" in params and not isinstance(params["provided_mtime"], str):
            raise InvalidParameterError("Bad parameter: provided_mtime must be an str")
        if "ref" in params and not isinstance(params["ref"], str):
            raise InvalidParameterError("Bad parameter: ref must be an str")
        if "restart" in params and not isinstance(params["restart"], int):
            raise InvalidParameterError("Bad parameter: restart must be an int")
        if "size" in params and not isinstance(params["size"], int):
            raise InvalidParameterError("Bad parameter: size must be an int")
        if "structure" in params and not isinstance(params["structure"], str):
            raise InvalidParameterError("Bad parameter: structure must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")

        response, options = Api.send_request("POST", "/files/{path}".format(path=params['path']), params, options)
        return File(response.data, options)
    
    # Parameters:
    #   provided_mtime - string - Modified time of file.
    #   priority_color - string - Priority/Bookmark color of file.
    @staticmethod
    def do_update(path, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["path"] = path
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "provided_mtime" in params and not isinstance(params["provided_mtime"], str):
            raise InvalidParameterError("Bad parameter: provided_mtime must be an str")
        if "priority_color" in params and not isinstance(params["priority_color"], str):
            raise InvalidParameterError("Bad parameter: priority_color must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")

        response, options = Api.send_request("PATCH", "/files/{path}".format(path=params['path']), params, options)
        return File(response.data, options)
    
    # Parameters:
    #   recursive - boolean - If true, will recursively delete folers.  Otherwise, will error on non-empty folders.  For legacy reasons, this parameter may also be provided as the HTTP header `Depth: Infinity`
    @staticmethod
    def do_delete(path, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["path"] = path
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")

        response, _options = Api.send_request("DELETE", "/files/{path}".format(path=params['path']), params, options)
        return response.data

    @staticmethod
    def do_destroy(path, params = {}):
        File.do_delete(path, params)
    