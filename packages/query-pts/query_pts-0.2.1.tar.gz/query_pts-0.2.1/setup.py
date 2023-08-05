"""author: SunYangtian
   time: 2022/06/07
"""

from gzip import READ
from setuptools import find_packages, setup, Extension
from torch.utils import cpp_extension

with open("./README.md", 'r', encoding='utf-8') as f:
      README = f.read()

setup(name='query_pts',
      version='0.2.1',
      author="SunYangtian",
      author_email="sunyangtian98@gmail.com",
      description="A package for calculate barycentric coordinates in the tetrahedras.",
      long_description=README,
      long_description_content_type="text/markdown",
      packages=find_packages(where='src'),
      package_dir={"": "src"},
      install_requires=[
            'torch>=1.7.1',],
      ext_modules=[cpp_extension.CUDAExtension('query_cpp', 
                    ["src/query_pts/cpp_extension/cpp_query.cpp", "src/query_pts/cpp_extension/knn.cu"],)],
      cmdclass={'build_ext': cpp_extension.BuildExtension})

### query_pts.cuda: the name of .egg, and the name for pip install
### query_cpp: the name of cpp build file

# >>>> equivalent code >>>>
# Extension(
#    name='lltm_cpp',
#    sources=['lltm.cpp'],
#    include_dirs=cpp_extension.include_paths(),
#    language='c++')