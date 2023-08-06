from setuptools import setup, find_packages
import glob
  
with open("README.md", 'r') as f:
    long_description = f.read()
  
setup(
        name ='qepseudos',
        version ='0.0.3',
        author ='Harish PVV',
        author_email ='harishpvv@gmail.com',
        description ="Pseudo potentials for QuantumEspresso calculations",
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        packages = find_packages(),
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        keywords ='quantum espresso pseudo potentials dft harishpvv',
        zip_safe = False,
        data_files = [("pseudos/PBE/", glob.glob("src/qepseudos/pseudos/PBE_ONCV/*.UPF")),
                      ("pseudos/LDA/", glob.glob("src/qepseudos/pseudos/LDA_ONCV/*.UPF")),
                      ("pseudos/PBESOL/", glob.glob("src/qepseudos/pseudos/PBESOL_ONCV/*.UPF"))],
        include_package_data = True

        )
