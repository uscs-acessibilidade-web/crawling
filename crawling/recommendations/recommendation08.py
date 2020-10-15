from bs4 import BeautifulSoup, Comment
import re

from ..occurrences.occurrences import Occurrences
from ..occurrences.occurrence_interface import OccurrenceInterface


class Recommendation08:
    """
    Recomendação 08: Separar links adjacentes
    """

    def __init__(self, sourcecode):
        self.rec = 8
        self.sourcecode = sourcecode
        self.occurrences = Occurrences()

    def avaliacao(self):
        # ispassou = True
        soap = BeautifulSoup(self.sourcecode, 'html.parser')
        remove = soap.find_all(text=lambda text: isinstance(text, Comment))
        for removeitem in remove:  # remove o código html comentado
            removeitem.extract()
        soapfiltro = BeautifulSoup(soap.prettify(), 'html.parser')

        for paragraph in soap.find_all('p'):
            ispassou = True
            tags_a = paragraph.find_all('a')
            if len(tags_a) > 1:
                par = str(paragraph).lower()
                paragrafosemespaco = re.sub('\s', "", par)  # tira os espacos para verificar o "\n"
                conj = ['</a><br><a', '</a><br/><a', '</a><br /><a']

                if '</a><a' in par:  # verifica se tem um fechamento ligado na abertura de outra tag a
                    # dispara erro
                    ispassou = False
                    self.occurrences.add(OccurrenceInterface(self.rec, 1, par, 2))
                if '</a> <a' in par:  # verifica se tem espaço entre fechamento e abertura de outra tag a
                    # dispara erro
                    self.occurrences.add(OccurrenceInterface(self.rec, 1, par, 2))
                    ispassou = False
                if conj[0] in paragrafosemespaco or conj[1] in paragrafosemespaco or conj[2] in paragrafosemespaco:
                    # verifica se tem a tag de quebra de linha entre fechamento e abertura de outra tag a
                    # dispara erro
                    self.occurrences.add(OccurrenceInterface(self.rec, 1, par, 2))
                    ispassou = False
                if str("</a>\n<a") in paragrafosemespaco:
                    # verifica se tem quebra de linha entra o fechamento e abertura de outra tag a
                    self.occurrences.add(OccurrenceInterface(self.rec, 1, par, 2))
                    ispassou = False
                if "</a><br>\n<a" in paragrafosemespaco:
                    self.occurrences.add(OccurrenceInterface(self.rec, 1, par, 2))
                    ispassou = False

                if ispassou:
                    self.occurrences.add(OccurrenceInterface(self.rec, 0,par, 2))

        return self.occurrences.list_of_occurrences
