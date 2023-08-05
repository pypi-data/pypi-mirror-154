"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.descriptor_pb2
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class Version(google.protobuf.message.Message):
    """The version number of protocol compiler."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MAJOR_FIELD_NUMBER: builtins.int
    MINOR_FIELD_NUMBER: builtins.int
    PATCH_FIELD_NUMBER: builtins.int
    SUFFIX_FIELD_NUMBER: builtins.int
    major: builtins.int
    minor: builtins.int
    patch: builtins.int
    suffix: typing.Text
    """A suffix for alpha, beta or rc release, e.g., "alpha-1", "rc2". It should
    be empty for mainline stable releases.
    """

    def __init__(self,
        *,
        major: typing.Optional[builtins.int] = ...,
        minor: typing.Optional[builtins.int] = ...,
        patch: typing.Optional[builtins.int] = ...,
        suffix: typing.Optional[typing.Text] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["major",b"major","minor",b"minor","patch",b"patch","suffix",b"suffix"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["major",b"major","minor",b"minor","patch",b"patch","suffix",b"suffix"]) -> None: ...
global___Version = Version

class CodeGeneratorRequest(google.protobuf.message.Message):
    """An encoded CodeGeneratorRequest is written to the plugin's stdin."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    FILE_TO_GENERATE_FIELD_NUMBER: builtins.int
    PARAMETER_FIELD_NUMBER: builtins.int
    PROTO_FILE_FIELD_NUMBER: builtins.int
    COMPILER_VERSION_FIELD_NUMBER: builtins.int
    @property
    def file_to_generate(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """The .proto files that were explicitly listed on the command-line.  The
        code generator should generate code only for these files.  Each file's
        descriptor will be included in proto_file, below.
        """
        pass
    parameter: typing.Text
    """The generator parameter passed on the command-line."""

    @property
    def proto_file(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[google.protobuf.descriptor_pb2.FileDescriptorProto]:
        """FileDescriptorProtos for all files in files_to_generate and everything
        they import.  The files will appear in topological order, so each file
        appears before any file that imports it.

        protoc guarantees that all proto_files will be written after
        the fields above, even though this is not technically guaranteed by the
        protobuf wire format.  This theoretically could allow a plugin to stream
        in the FileDescriptorProtos and handle them one by one rather than read
        the entire set into memory at once.  However, as of this writing, this
        is not similarly optimized on protoc's end -- it will store all fields in
        memory at once before sending them to the plugin.

        Type names of fields and extensions in the FileDescriptorProto are always
        fully qualified.
        """
        pass
    @property
    def compiler_version(self) -> global___Version:
        """The version number of protocol compiler."""
        pass
    def __init__(self,
        *,
        file_to_generate: typing.Optional[typing.Iterable[typing.Text]] = ...,
        parameter: typing.Optional[typing.Text] = ...,
        proto_file: typing.Optional[typing.Iterable[google.protobuf.descriptor_pb2.FileDescriptorProto]] = ...,
        compiler_version: typing.Optional[global___Version] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["compiler_version",b"compiler_version","parameter",b"parameter"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["compiler_version",b"compiler_version","file_to_generate",b"file_to_generate","parameter",b"parameter","proto_file",b"proto_file"]) -> None: ...
global___CodeGeneratorRequest = CodeGeneratorRequest

class CodeGeneratorResponse(google.protobuf.message.Message):
    """The plugin writes an encoded CodeGeneratorResponse to stdout."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class _Feature:
        ValueType = typing.NewType('ValueType', builtins.int)
        V: typing_extensions.TypeAlias = ValueType
    class _FeatureEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[CodeGeneratorResponse._Feature.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        FEATURE_NONE: CodeGeneratorResponse._Feature.ValueType  # 0
        FEATURE_PROTO3_OPTIONAL: CodeGeneratorResponse._Feature.ValueType  # 1
    class Feature(_Feature, metaclass=_FeatureEnumTypeWrapper):
        """Sync with code_generator.h."""
        pass

    FEATURE_NONE: CodeGeneratorResponse.Feature.ValueType  # 0
    FEATURE_PROTO3_OPTIONAL: CodeGeneratorResponse.Feature.ValueType  # 1

    class File(google.protobuf.message.Message):
        """Represents a single generated file."""
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        NAME_FIELD_NUMBER: builtins.int
        INSERTION_POINT_FIELD_NUMBER: builtins.int
        CONTENT_FIELD_NUMBER: builtins.int
        GENERATED_CODE_INFO_FIELD_NUMBER: builtins.int
        name: typing.Text
        """The file name, relative to the output directory.  The name must not
        contain "." or ".." components and must be relative, not be absolute (so,
        the file cannot lie outside the output directory).  "/" must be used as
        the path separator, not "\\".

        If the name is omitted, the content will be appended to the previous
        file.  This allows the generator to break large files into small chunks,
        and allows the generated text to be streamed back to protoc so that large
        files need not reside completely in memory at one time.  Note that as of
        this writing protoc does not optimize for this -- it will read the entire
        CodeGeneratorResponse before writing files to disk.
        """

        insertion_point: typing.Text
        """If non-empty, indicates that the named file should already exist, and the
        content here is to be inserted into that file at a defined insertion
        point.  This feature allows a code generator to extend the output
        produced by another code generator.  The original generator may provide
        insertion points by placing special annotations in the file that look
        like:
          @@protoc_insertion_point(NAME)
        The annotation can have arbitrary text before and after it on the line,
        which allows it to be placed in a comment.  NAME should be replaced with
        an identifier naming the point -- this is what other generators will use
        as the insertion_point.  Code inserted at this point will be placed
        immediately above the line containing the insertion point (thus multiple
        insertions to the same point will come out in the order they were added).
        The double-@ is intended to make it unlikely that the generated code
        could contain things that look like insertion points by accident.

        For example, the C++ code generator places the following line in the
        .pb.h files that it generates:
          // @@protoc_insertion_point(namespace_scope)
        This line appears within the scope of the file's package namespace, but
        outside of any particular class.  Another plugin can then specify the
        insertion_point "namespace_scope" to generate additional classes or
        other declarations that should be placed in this scope.

        Note that if the line containing the insertion point begins with
        whitespace, the same whitespace will be added to every line of the
        inserted text.  This is useful for languages like Python, where
        indentation matters.  In these languages, the insertion point comment
        should be indented the same amount as any inserted code will need to be
        in order to work correctly in that context.

        The code generator that generates the initial file and the one which
        inserts into it must both run as part of a single invocation of protoc.
        Code generators are executed in the order in which they appear on the
        command line.

        If |insertion_point| is present, |name| must also be present.
        """

        content: typing.Text
        """The file contents."""

        @property
        def generated_code_info(self) -> google.protobuf.descriptor_pb2.GeneratedCodeInfo:
            """Information describing the file content being inserted. If an insertion
            point is used, this information will be appropriately offset and inserted
            into the code generation metadata for the generated files.
            """
            pass
        def __init__(self,
            *,
            name: typing.Optional[typing.Text] = ...,
            insertion_point: typing.Optional[typing.Text] = ...,
            content: typing.Optional[typing.Text] = ...,
            generated_code_info: typing.Optional[google.protobuf.descriptor_pb2.GeneratedCodeInfo] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["content",b"content","generated_code_info",b"generated_code_info","insertion_point",b"insertion_point","name",b"name"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["content",b"content","generated_code_info",b"generated_code_info","insertion_point",b"insertion_point","name",b"name"]) -> None: ...

    ERROR_FIELD_NUMBER: builtins.int
    SUPPORTED_FEATURES_FIELD_NUMBER: builtins.int
    FILE_FIELD_NUMBER: builtins.int
    error: typing.Text
    """Error message.  If non-empty, code generation failed.  The plugin process
    should exit with status code zero even if it reports an error in this way.

    This should be used to indicate errors in .proto files which prevent the
    code generator from generating correct code.  Errors which indicate a
    problem in protoc itself -- such as the input CodeGeneratorRequest being
    unparseable -- should be reported by writing a message to stderr and
    exiting with a non-zero status code.
    """

    supported_features: builtins.int
    """A bitmask of supported features that the code generator supports.
    This is a bitwise "or" of values from the Feature enum.
    """

    @property
    def file(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___CodeGeneratorResponse.File]: ...
    def __init__(self,
        *,
        error: typing.Optional[typing.Text] = ...,
        supported_features: typing.Optional[builtins.int] = ...,
        file: typing.Optional[typing.Iterable[global___CodeGeneratorResponse.File]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["error",b"error","supported_features",b"supported_features"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["error",b"error","file",b"file","supported_features",b"supported_features"]) -> None: ...
global___CodeGeneratorResponse = CodeGeneratorResponse
