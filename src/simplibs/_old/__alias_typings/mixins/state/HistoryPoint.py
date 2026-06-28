from typing import TypeAlias
from datetime import datetime


# Bod na časové ose, kterým se lze navigovat (index položky nebo přesný čas)
HistoryPoint: TypeAlias = int | datetime