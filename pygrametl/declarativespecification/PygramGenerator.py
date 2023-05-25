from pygrametl.declarativespecification.parsing import *
import os


class PygramGenerator:
    def __init__(self, specification: IntermediateSpecification):
        self.dimblocks = []
        self.factblocks = []
        # TODO: Update to use internal key_refs of ParsedFactTable
        self.keys = []
        for dimension in specification.dimensions:
            self.keys.append(f"'{dimension.name}{specification.pk_name}'")
        self.header = """# This file was generated by PygramETL-DeclarativeSpecification in conformity with a given specification.
# Credit Simon Mathiasen 2023 (AAU)

import psycopg2
import pygrametl
from pygrametl.datasources import SQLSource, CSVSource
from pygrametl.tables import CachedDimension, FactTable"""

    def generate_dimension(self, dimension: ParsedDimension):
        attribute_str = ""
        attribute: ParsedAttribute
        for attribute in dimension.members:
            attribute_str += f"'{attribute.name}' "

        dimblock = PythonCodeBlock(f"{dimension.name}_dimension = CachedDimension(", [
            f"name='{dimension.name}',",
            f"key='{dimension.keys}',",
            f"attributes=[{attribute_str.strip()}])"])

        # TODO: Consider returning instead
        self.dimblocks.append(dimblock)

    def generate_fact_table(self, fact_table: ParsedFactTable):
        keyref_string = ", ".join(self.keys)
        measure_list = []
        for measure in fact_table.members:
            measure_list.append(f"'{measure.name}'")
        measure_names = ", ".join(measure_list)
        factblock = PythonCodeBlock(f"{fact_table.name}_fact_table = FactTable(", [
            f"name='{fact_table.name}',",
            f"keyrefs=[{keyref_string}],",
            f"measures=[{measure_names}])"
        ])

        # TODO: Consider returning instead
        self.factblocks.append(factblock)

    def create_pygram_file(self, specification: IntermediateSpecification):
        for dim in specification.dimensions:
            self.generate_dimension(dim)
        for fact_table in specification.fact_tables:
            self.generate_fact_table(fact_table)

        # TODO: Change for better output dir
        working_dir = os.getcwd()
        file = open(working_dir + "/Pygram-generated-setup", 'w')
        file.write(self.header + "\n\n")
        for block in self.dimblocks:
            file.write(str(block))
            file.write("\n\n")
        for block in self.factblocks:
            file.write(str(block) + "\n\n")
        file.close()


class PythonCodeBlock:
    def __init__(self, head, block):
        self.head = head
        self.block = block

    def __str__(self, indent=""):
        result = indent + self.head + "\n"
        indent += "    "
        for block in self.block:
            if isinstance(block, PythonCodeBlock):
                result += block.__str__(indent)
            else:
                result += indent + block + "\n"
        return result
