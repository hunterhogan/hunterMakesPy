from setuptools import Extension, setup

setup(ext_modules = [
	Extension(name = "humpy_cytoolz.dicttoolz", sources = ["humpy_cytoolz/dicttoolz.pyx"]),
	Extension(name = "humpy_cytoolz.functoolz", sources = ["humpy_cytoolz/functoolz.pyx"]),
	Extension(name = "humpy_cytoolz.itertoolz", sources = ["humpy_cytoolz/itertoolz.pyx"]),
	Extension(name = "humpy_cytoolz.recipes", sources = ["humpy_cytoolz/recipes.pyx"]),
	Extension(name = "humpy_cytoolz.utils", sources = ["humpy_cytoolz/utils.pyx"]),
])
