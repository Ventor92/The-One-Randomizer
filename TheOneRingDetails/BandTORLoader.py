import pandas as pd
from TheOneRingDetails.BandTOR import BandTOR, BandArmamentType, BandSizeType, BandFacultyType
from TheOneRingDetails.AllieTOR import AllieTOR, InjuryTORType, FatigueTORType

class BandTORLoader:
    def __init__(self, filepath: str="data/Band.xlsx", sheetName: str ="Bands"):
        self.filepath = filepath
        self.sheet_name = sheetName
        self.__table = pd.read_excel(filepath, sheet_name=sheetName)
        self.__tableAllies = pd.read_excel(filepath, sheet_name="Allies")
        # print(self.__table)
        self.__bands: list[BandTOR] = self.__load()

    def __load(self) -> list[BandTOR]:
        if self.__table.empty or self.__tableAllies.empty:
            raise ValueError("Plik jest pusty lub nie zawiera żadnych danych.")

        bands: list[BandTOR] = []

        for _, row in self.__table.iterrows():
            band = BandTOR(
                id=int(row.get('id', 0)),
                name=row.get('name', "Band of the Ring"),
                armament=BandArmamentType[row.get('armament', BandArmamentType.READY.name)],
                size=BandSizeType[row.get('size', BandSizeType.MEDIUM.name)],
                faculty=BandFacultyType[row.get('faculty', BandFacultyType.NONE.name)],
                eyeAwareness=row.get('eyeAwareness', 0),
                huntThreshold=row.get('huntThreshold', 14),
                hopePts=row.get('hopePts', 12),
                shadowPts=row.get('shadowPts', 12),
                shadowScars=row.get('shadowScars', 0),
            )
        
            for _, rowA in self.__tableAllies.iterrows():
                ally = AllieTOR(
                    id=rowA.get('id', 0),
                    idBand=rowA.get('idBand', 0),
                    active=rowA.get('active', False),
                    name=rowA.get('name', "Loaded Ally"),
                    injuries=InjuryTORType[rowA.get('injuries', InjuryTORType.NONE.name)],
                    fatigue=FatigueTORType[rowA.get('fatigue', FatigueTORType.NONE.name)],
                    hardened=rowA.get('hardened', False),
                    gift=rowA.get('gift', "DUAP"),
                    giftWasted=rowA.get('giftWasted', False),
                    kinglyGift=rowA.get('kinglyGift', "None"),
                    kinglyGiftWasted=rowA.get('kinglyGiftWasted', False),
                    quirksOrNotes=rowA.get('quirksOrNotes', "None"),
                )
                if ally.idBand == band.id:
                    band.addAlly(ally)

            band.updateSize()
            bands.append(band)

        return bands

    def getBands(self) -> list[BandTOR]:
        if not self.__bands:
            raise RuntimeError("Nie załadowano danych. Użyj metody `load()`.")
        return self.__bands