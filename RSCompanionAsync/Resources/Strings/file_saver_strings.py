""" 
Licensed under GNU GPL-3.0-or-later

This file is part of RS Companion.

RS Companion is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RS Companion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with RS Companion.  If not, see <https://www.gnu.org/licenses/>.

Author: Phillip Riskin
Date: 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

from RSCompanionAsync.Model.app_defs import LangEnum
from enum import Enum, auto


class StringsEnum(Enum):
    HDR_1 = auto()
    HDR_2 = auto()
    FLAG = auto()
    NOTE = auto()
    EVENT = auto()
    TSTAMP_HDR = auto()
    FLG_HDR = auto()
    ID_HDR = auto()
    EVNT_HDR = auto()
    NOTE_HDR = auto()


english = {StringsEnum.HDR_1: "id, condition name, timestamp, block #",
           StringsEnum.HDR_2: "keyflag, event/note",
           StringsEnum.FLAG: "Flag",
           StringsEnum.NOTE: "Note",
           StringsEnum.EVENT: "Event",
           StringsEnum.ID_HDR: "device id",
           StringsEnum.FLG_HDR: "key flag",
           StringsEnum.TSTAMP_HDR: "timestamp",
           }

dutch = {StringsEnum.HDR_1: "Identificatie, conditienaam, tijdstempel, blok #",
         StringsEnum.HDR_2: "sleutel vlag, evenement/notitie",
         StringsEnum.FLAG: "Flag",
         StringsEnum.NOTE: "Notitie",
         StringsEnum.EVENT: "Evenement",
         StringsEnum.ID_HDR: "apparaat identificatie",
         StringsEnum.FLG_HDR: "sleutel vlag",
         StringsEnum.TSTAMP_HDR: "tijdstempel",
         }

french = {StringsEnum.HDR_1: "id, nom de la condition, horodatage, bloc #",
          StringsEnum.HDR_2: "drapeau, l' événement/remarque",
          StringsEnum.FLAG: "Drapeau",
          StringsEnum.NOTE: "Remarque",
          StringsEnum.EVENT: "Evénement",
          StringsEnum.ID_HDR: "appareil id",
          StringsEnum.FLG_HDR: "drapeau clé",
          StringsEnum.TSTAMP_HDR: "horodatage",
          }

german = {StringsEnum.HDR_1: "ID, Bedingungsname, Zeitstempel, Blocknummer",
          StringsEnum.HDR_2: "schlüsselflagge, veranstaltung/notieren",
          StringsEnum.FLAG: "Flagge",
          StringsEnum.NOTE: "Notieren",
          StringsEnum.EVENT: "Veranstaltung",
          StringsEnum.ID_HDR: "gerät id",
          StringsEnum.FLG_HDR: "schlüsselflagge",
          StringsEnum.TSTAMP_HDR: "zeitstempel",
          }

# TODO: Translate
russian = {StringsEnum.HDR_1: "Header 1",
           StringsEnum.HDR_2: "Header 2",
           StringsEnum.FLAG: "Flag",
           StringsEnum.NOTE: "Note",
           StringsEnum.EVENT: "Event",
           StringsEnum.ID_HDR: "device id",
           StringsEnum.FLG_HDR: "key flag",
           StringsEnum.TSTAMP_HDR: "timestamp",
           }

spanish = {StringsEnum.HDR_1: "id, nombre de condición, marca de tiempo, bloque #",
           StringsEnum.HDR_2: "bandera clave, evento/nota",
           StringsEnum.FLAG: "Bandera clave",
           StringsEnum.NOTE: "Nota",
           StringsEnum.EVENT: "Evento",
           StringsEnum.ID_HDR: "dispositivo id",
           StringsEnum.FLG_HDR: "bandera clave",
           StringsEnum.TSTAMP_HDR: "marca de tiempo",
           }

# TODO: Translate
chinese = {StringsEnum.HDR_1: "Header 1",
           StringsEnum.HDR_2: "Header 2",
           StringsEnum.FLAG: "Flag",
           StringsEnum.NOTE: "Note",
           StringsEnum.EVENT: "Event",
           StringsEnum.ID_HDR: "device id",
           StringsEnum.FLG_HDR: "key flag",
           StringsEnum.TSTAMP_HDR: "timestamp",
           }

# TODO: Translate
japanese = {StringsEnum.HDR_1: "Header 1",
            StringsEnum.HDR_2: "Header 2",
            StringsEnum.FLAG: "Flag",
            StringsEnum.NOTE: "Note",
            StringsEnum.EVENT: "Event",
            StringsEnum.ID_HDR: "device id",
            StringsEnum.FLG_HDR: "key flag",
            StringsEnum.TSTAMP_HDR: "timestamp",
            }

strings = {LangEnum.ENG: english,
           LangEnum.DUT: dutch,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.RUS: russian,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese,
           LangEnum.JPN: japanese}
