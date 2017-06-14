from conan.packager import ConanMultiPackager
import platform


if __name__ == "__main__":
    mingw_configurations = [("4.9", "x86_64", "seh", "posix"),
                            ("4.9", "x86_64", "sjlj", "posix"),
                            ("4.9", "x86", "sjlj", "posix"),
                            ("4.9", "x86", "dwarf2", "posix")]
    builder = ConanMultiPackager(mingw_configurations=mingw_configurations)
    builder.add_common_builds(shared_option_name="zlib:shared", pure_c=True)
    builder.run()
