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
Author: Nathan Rogers
Date: 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

from Model.app_defs import LangEnum
from enum import Enum, auto


class StringsEnum(Enum):
    COMPANY_NAME = auto()
    APP_NAME = auto()
    PROG_OUT_HDR = auto()
    LOG_VER_ID = auto()
    ABOUT_COMPANY = auto()
    ABOUT_APP = auto()
    UPDATE_AVAILABLE = auto()
    NO_UPDATE = auto()
    ERR_UPDATE_CHECK = auto()
    DEV_CON_ERR = auto()
    LOG_OUT_NAME = auto()
    RESTART_PROG = auto()
    UPDATE_HDR = auto()
    UPDATE_HDR_ERR = auto()


company_name = "Red Scientific"
app_name = "RS Companion"
log_out_filename = "companion_app_log.txt"


english = {StringsEnum.COMPANY_NAME: company_name,
           StringsEnum.APP_NAME: app_name,
           StringsEnum.LOG_OUT_NAME: log_out_filename,
           StringsEnum.LOG_VER_ID: company_name + " app version: ",
           StringsEnum.PROG_OUT_HDR: "Timestamp, Author, Location, Message\n",
           StringsEnum.ABOUT_COMPANY: company_name + " Inc was founded in 2015 by Joel Cooper PhD\n\n"
                                                     " Contact Information:\n"
                                                     " joel@redscientific.com\n"
                                                     " 1-801-520-5408",
           StringsEnum.ABOUT_APP: "- Most things in this app have tooltips. Mouse over different parts to see"
                                  " respective tooltips for more information\n\n"
                                  " Along the top of the app you will find a control bar containing the following:\n"
                                  " - Create/End button: Create or end an experiment. Choose a location folder for the"
                                  " app to save device data.\n"
                                  " - Play/Pause button: Begin/resume or pause an experiment in progress.\n"
                                  " - Optional condition name: An optional name that will be associated with the newly"
                                  " created experiment.\n\n"
                                  " - Key Flag: Press a letter key at any time to make a quick reference key that will"
                                  " be associated with the data coming in from the Devices during an experiment.\n\n"
                                  " - Note: Enter a note into the box and press Post to apply that note to all device"
                                  " data files within the current experiment.\n\n"
                                  " - Information: Displays information in regards to the current experiment.\n\n"
                                  " - Drive Info: Displays information in regards to the current volume where data is"
                                  " being saved to.",
           StringsEnum.UPDATE_HDR: "Update",
           StringsEnum.UPDATE_HDR_ERR: "Error",
           StringsEnum.UPDATE_AVAILABLE: "An update is available.",
           StringsEnum.NO_UPDATE: "Your program is up to date.",
           StringsEnum.ERR_UPDATE_CHECK: "There was an unexpected error connecting to the repository. Please check"
                                         " https://redscientific.com/downloads.html manually or contact Red Scientific"
                                         " directly.",
           StringsEnum.DEV_CON_ERR: "There was a problem connecting the device, please retry connection.",
           StringsEnum.RESTART_PROG: "This app must restart for changes to take effect."
           }

# TODO: Verify French version
french = {StringsEnum.COMPANY_NAME: company_name,
          StringsEnum.APP_NAME: app_name,
          StringsEnum.LOG_OUT_NAME: log_out_filename,
          StringsEnum.LOG_VER_ID: company_name + " Version de l'application: ",
          StringsEnum.PROG_OUT_HDR: "Horodatage, Auteur, Emplacement, Message\n",
          StringsEnum.ABOUT_COMPANY: company_name + " Inc a été fondée en 2015 par Joel Cooper PhD\n\n"
                                                    " Informations de contact:\n"
                                                    " joel@redscientific.com\n"
                                                    " 1-801-520-5408",
          StringsEnum.ABOUT_APP: "- La plupart des éléments de cette application comportent des info-bulles."
                                 " Passez la souris sur différentes parties pour voir les info-bulles respectives"
                                 " pour plus d'informations.\n\n"
                                 " En haut de l'application, vous trouverez une barre de contrôle contenant les"
                                 " éléments suivants:\n"
                                 " - Bouton Créer/Fin: créez ou terminez une expérience. Choisissez un dossier"
                                 " d'emplacement pour l'application pour enregistrer les données de l'appareil.\n"
                                 " - Bouton Lecture / Pause: commence / reprend ou suspend une expérience en cours.\n"
                                 " - Nom de condition facultatif: nom facultatif qui sera associé à la nouvelle"
                                 " expérience créée.\n\n"
                                 " - Indicateur de touche: appuyez sur une touche de lettre à tout moment pour créer"
                                 " une touche de référence rapide qui sera associée aux données provenant des"
                                 " appareils pendant une expérience.\n\n"
                                 " - Remarque: entrez une note dans la case et appuyez sur Publier pour appliquer"
                                 " cette note à tous les fichiers de données de l'appareil dans l'expérience"
                                 " en cours.\n\n"
                                 " - Informations: affiche des informations concernant l'expérience en cours.\n\n"
                                 " - Informations sur le lecteur: affiche des informations concernant le volume"
                                 " actuel sur lequel les données sont enregistrées.",
          StringsEnum.UPDATE_HDR: "Mise à jour",
          StringsEnum.UPDATE_HDR_ERR: "Erreur",
          StringsEnum.UPDATE_AVAILABLE: "Une mise à jour est disponible.",
          StringsEnum.NO_UPDATE: "Votre programme est à jour.",
          StringsEnum.ERR_UPDATE_CHECK: "Une erreur inattendue s'est produite lors de la connexion au référentiel."
                                        " Veuillez vérifier https://redscientific.com/downloads.html manuellement"
                                        " ou contacter directement Red Scientific.",
          StringsEnum.DEV_CON_ERR: "Un problème est survenu lors de la connexion de l'appareil. Veuillez réessayer.",
          StringsEnum.RESTART_PROG: "Cette application doit redémarrer pour que les modifications prennent effet."
          }

strings = {LangEnum.ENG: english,
           LangEnum.FRE: french}
