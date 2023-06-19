from from_wandb_to_paper.tables.string_table import StringTable


class LatexStringTable(StringTable):
    def __str__(self, *args, **kwargs):
        return self.data.to_latex(*args, **kwargs)
