#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from cpt.packager import ConanMultiPackager


def docker_entry_script():
    if os.getenv("CONAN_CLANG_VERSIONS", "") != "7.0":
        return None

    return " ".join(["conan config install http://github.com/conan-io/hooks.git -sf hooks -tf hooks &&",
                     "conan config set hooks.attribute_checker &&",
                     "conan config set hooks.binary_linter &&",
                     "conan config set hooks.bintray_updater &&",
                     "conan config set hooks.conan-center_reviewer &&",
                     "conan config set hooks.export_metadata &&",
                     "conan config set hooks.github_updater &&",
                     "conan config set hooks.spdx_checker"])

def pip_extra_packages():
    if os.getenv("CONAN_CLANG_VERSIONS", "") != "7.0":
        return None
    return ["https://github.com/lief-project/packages/raw/lief-master-latest/pylief-0.9.0.dev.zip", "spdx_lookup"]

if __name__ == "__main__":
    builder = ConanMultiPackager(docker_entry_script=docker_entry_script(), pip_install=pip_extra_packages())
    builder.add_common_builds(pure_c=True)
    builder.run()
