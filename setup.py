from setuptools import setup

setup(
    name="pd2tfrecord",
    py_modules=["pd2tfrecord"],
    version="0.2",
    license="MIT",
    description="Library to convert pandas data frame to tfrecord and vice versa",
    author="Nitin Aggarwal",
    author_email="nitin.agg1909@gmail.com",
    url="https://github.com/NitinAgg/pd2tfrecord",
    download_url="https://github.com/NitinAgg/pd2tfrecord/archive/v_02.tar.gz",
    keywords="tensorflow tfrecord pandas dataframe tf.example",
    install_requires=["tensorflow>=2.0", "pandas"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
