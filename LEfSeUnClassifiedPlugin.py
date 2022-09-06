# Objective:
#   To fix bacterial names
#   For example, instead of "k__Bacteria|p__Bacteroidetes|__|__|__|__",
#   output "k__Bacteria|p__Bacteroidetes|p__Bacteroidetes_Unclassified|c__Bacteroidetes_Unclassified|o__Bacteroidetes_Unclassified|f__Bacteroidetes_Unclassified|g__Bacteroidetes_Unclassified"

#lefse_in = "../lefSe_analysis/lefse_final.txt"
#lefse_out = "../lefSe_analysis/lefse_final_fixed.txt"

levels = ["k","p","c","o","f","g"]

class LEfSeUnClassifiedPlugin:
    def input(self, infile):
        self.lefse_in = infile

    def run(self):
        pass

    def output(self, outfile):
      with open(self.lefse_in, 'r') as f:
       with open(outfile, "w") as out:
        for line in f.readlines():
            if ("|" not in line) or ("Unassigned" in line):
                row_fixed = line
            else:
                line_split = line.split("\t")
                bacteria = line_split[0]
                lineage = bacteria.split("|")
                previous_name=""
                previous_level="k"
                fixed_name = ""
                for level in lineage:
                    if level.split("__")[1]=="":
                        level = levels[levels.index(previous_level)+1] + "__" + previous_name + "_Unclassified"
                    else:
                        previous_name = level.split("__")[1]
                    previous_level = level.split("__")[0]

                    fixed_name+="|"+level
                fixed_name = fixed_name.strip("|")
                for i, element in enumerate(line_split):
                    if i==0:
                        row_fixed = fixed_name
                    else:
                        row_fixed += "\t" + element
            out.write(row_fixed)
