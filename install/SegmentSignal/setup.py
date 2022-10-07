from   distutils.core                            import setup
from   distutils.core                            import Extension
import pybind11

sfc_module = Extension(
    "SegmentSignalPy",
    sources=["module.cpp", "SegmentSignalFunctions.cpp", "SegmentationResults.cpp", "SegmentSignal.cpp"],
    include_dirs=[pybind11.get_include()],
    language="c++",
    extra_compile_args=[],
)

setup(
    name="SegmentSignalPy",
    version="1.0",
    description="Signal segmentation algorithm  by S.Radhakrishnan, et al.  This is a Python interface for the algorithm whish is in C++.",
    ext_modules=[sfc_module],
)