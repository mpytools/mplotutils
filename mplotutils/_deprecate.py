import warnings


def _module_renamed_warning_init(attr):

    old_module = f"mplotutils.{attr}"
    new_module = f"mplotutils._{attr}"

    msg = (
        f"``{old_module}`` is deprecated and has been renamed to ``{new_module}`` in v0.6.0.."
        f" Note that importing ``{new_module}`` is discuraged. Please use"
        f" functions directly from the  main namespace."
    )

    warnings.warn(msg, FutureWarning, stacklevel=2)


def _module_renamed_warning(attr, submodule):

    old_module = f"mplotutils.{submodule}"
    new_module = f"mplotutils._{submodule}"

    warnings.warn(
        f"``{old_module}`` is deprecated and has been renamed to ``{new_module}`` in v0.6.0."
        f" Note that importing from ``{new_module}`` is discuraged. Please use"
        f" functions directly from the  main namespace, i.e., ``mplotutils.{attr}``",
        FutureWarning,
        stacklevel=3,
    )
