def extract_info(oc, dc=None):
    if dc is None:
        dc = {'errors': [0, 0, 0], 'warnings': [0, 0, 0], 'successes': 0}

    if oc['peso'] == 1:
        if oc['type_code'] == 1:
            e = dc['errors'][0]
            dc['errors'][0] = e + 1
        elif oc['type_code'] == 2:
            w = dc['warnings'][0]
            dc['warnings'][0] = w + 1
        elif oc['type_code'] == 0:
            dc['successes'] = dc['successes'] + 1
    elif oc['peso'] == 2:
        if oc['type_code'] == 1:
            e = dc['errors'][1]
            dc['errors'][1] = e + 1
        elif oc['type_code'] == 2:
            w = dc['warnings'][1]
            dc['warnings'][1] = w + 1
        elif oc['type_code'] == 0:
            dc['successes'] = dc['successes'] + 1
    elif oc['peso'] == 3:
        if oc['type_code'] == 1:
            e = dc['errors'][2]
            dc['errors'][2] = e + 1
        elif oc['type_code'] == 2:
            w = dc['warnings'][2]
            dc['warnings'][2] = w + 1
        elif oc['type_code'] == 0:
            dc['successes'] = dc['successes'] + 1
    else:
        print('Ops')

    return dc


def calculate_wab(es, ws):
    """
    Score WAB (Web Accessibility Barrier)

    fórmula: p * ea * (e / a) * w
        p - quantidade de páginas
        ea - total de erros e alertas
        e - total de erros
        a - total de alertas
        w - peso

    :param es: list<int>
    :param ws: list<int>
    :return: float
    """

    parcials = []
    for i in range(3):
        d = 1 if ws[i] == 0 else ws[i]
        c = 1 * ((es[i] + ws[i]) * (es[i] / d)) * (i + 1)
        parcials.append(c)
    return sum(parcials) / len(parcials)


class Scores:
    """
    Análisa as ocorrências, calcula o score de acessibilidade e guarda os resultados.
    """
    def __init__(self, occorrences, cities):
        self.occorrences = occorrences
        self.cities = cities

    def calculate(self):
        amount = {}

        for occorrence in self.occorrences:
            if occorrence['city_id'] in amount.keys():
                amount[occorrence['city_id']] = extract_info(occorrence, amount[occorrence['city_id']])
            else:
                amount[occorrence['city_id']] = extract_info(occorrence)

        for c in amount:
            self.cities[c]['wab'] = round(calculate_wab(amount[c]['errors'], amount[c]['warnings']), 2)
            self.cities[c]['errors'] = sum(amount[c]['errors'])
            self.cities[c]['warnings'] = sum(amount[c]['warnings'])
            self.cities[c]['successes'] = amount[c]['successes']