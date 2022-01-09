import csv


class CSVEdit:
    def __init__(self, id_):
        self.id_ = id_

    def delete_row(self):
        lines = list()
        with open('product_info.csv', 'r') as readFile:

            reader = csv.reader(readFile)

            for row in reader:

                lines.append(row)

                for field in row:

                    if str(self.id_) in field:
                        lines.remove(row)

        with open('product_info.csv', 'w') as writeFile:

            writer = csv.writer(writeFile)

            writer.writerows(lines)

    def edit_row(self, product, quantity, category):
        self.delete_row()
        csv_row = f"{product}, {quantity}, {category}, {self.id_}\n"
        with open('product_info.csv', 'a') as fd:
            fd.write(csv_row)
