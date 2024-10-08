load("@aspect_rules_py//py:defs.bzl", "py_library", "py_pytest_main", "py_test")
load("@aspect_rules_lint//format:defs.bzl", "format_multirun")
load("@rules_python//python:packaging.bzl", "py_wheel")
load("@cmk_agent_based//:requirements.bzl", "requirement")
load("@rules_python//python:pip.bzl", "compile_pip_requirements", "whl_filegroup")
load("@rules_pkg//pkg:mappings.bzl", "pkg_files")
load("@rules_pkg//pkg:tar.bzl", "pkg_tar")
load("@omd_packages//omd/packages/Python:version.bzl", "PYTHON_MAJOR_DOT_MINOR")

compile_pip_requirements(
    name = "requirements",
    requirements_in = "pyproject.toml",
    requirements_txt = "requirements_lock.txt",  # shall exist, emtpy is okay
)

py_library(
    name = "cmk-agent-based",
    srcs = [
        "cmk/agent_based/prediction_backend.py",
        "cmk/agent_based/v1/__init__.py",
        "cmk/agent_based/v1/_check_levels.py",
        "cmk/agent_based/v1/_checking_classes.py",
        "cmk/agent_based/v1/_detection.py",
        "cmk/agent_based/v1/_inventory_classes.py",
        "cmk/agent_based/v1/_regex.py",
        "cmk/agent_based/v1/_snmp.py",
        "cmk/agent_based/v1/_value_store_utils.py",
        "cmk/agent_based/v1/clusterize.py",
        "cmk/agent_based/v1/register.py",
        "cmk/agent_based/v1/render.py",
        "cmk/agent_based/v1/type_defs.py",
        "cmk/agent_based/v1/value_store.py",
        "cmk/agent_based/v2/__init__.py",
        "cmk/agent_based/v2/_check_levels.py",
        "cmk/agent_based/v2/_get_average.py",
        "cmk/agent_based/v2/_plugins.py",
        "cmk/agent_based/v2/clusterize.py",
        "cmk/agent_based/v2/render.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        requirement("pydantic"),
    ],
)

py_pytest_main(
    name = "__test__",
)

py_test(
    name = "unit",
    srcs = glob(["tests/**/*.py"]) + [":__test__.py"],
    # TODO: Duplicated from pyproject.toml
    args = [
        "--import-mode=importlib",
        "--doctest-modules",
    ],
    imports = ["."],
    main = ":__test__.py",
    deps = [
        ":__test__",
        ":cmk-agent-based",
        requirement("pytest"),
    ],
)

format_multirun(
    name = "format",
    python = "@aspect_rules_lint//format:ruff",
)

py_wheel(
    name = "wheel",
    distribution = "cmk-agent-based",
    strip_path_prefixes = ["packages/cmk-agent-based"],
    # TODO: Duplicated from pyproject.toml
    version = "1.0.0",
    deps = [
        ":cmk-agent-based",
    ],
)

whl_filegroup(
    name = "whl_filegroup",
    whl = ":wheel",
)

pkg_files(
    name = "pkg_files",
    srcs = [
        ":whl_filegroup",
    ],
    # TODO: As soon as we have all omd/packages in bazel, we won't need the intermediate install target anymore.
    # Then we can also completely remove the "python3-modules" prefix - currently it will be deployed to $(DESTDIR) via
    # $(PYTHON3_MODULES_INSTALL) in python3-modules.make
    prefix = "python3-modules/lib/python%s/site-packages" % PYTHON_MAJOR_DOT_MINOR,
    strip_prefix = "whl_filegroup",
)

pkg_tar(
    name = "pkg_tar",
    srcs = [
        ":pkg_files",
    ],
    visibility = ["//visibility:public"],
)
