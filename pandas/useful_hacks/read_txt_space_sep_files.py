@dataclass
class PositionMapping:
    column_name: str
    position: int
    length: int
    type: str

mobility_mapping = [
    PositionMapping(column_name="code_free", position=1, length=3, type="string"),
    PositionMapping(
        column_name="code_entreprise", position=4, length=10, type="string"
    ),
    PositionMapping(
        column_name="code_salarie",
        position=14,
        length=15,
        type="string",
    ),
]

colspecs = [
    (m.position - 1, m.position - 1 + m.length) for m in mobility_mapping
]
names = [m.column_name for m in mobility_mapping]

df = pd.read_fwf(file, colspecs=colspecs, names=names)
