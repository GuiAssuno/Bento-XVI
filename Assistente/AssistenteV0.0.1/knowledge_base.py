"""
Módulo de Base de Conhecimento
Contém informações sobre mecânica automotiva e conhecimentos gerais
"""

class KnowledgeBase:
    def __init__(self):
        print("Base de Conhecimento: Inicializada.")
        self.mechanics_data = {
            "carburador": "Um carburador é um dispositivo que mistura ar e combustível em proporções adequadas para a combustão interna de um motor.",
            "injeção eletrônica": "A injeção eletrônica é um sistema que controla eletronicamente a quantidade de combustível injetada no motor, otimizando a combustão."
        }
        self.general_data = {
            "temperatura do motor": "A temperatura ideal do motor varia, mas geralmente fica entre 90°C e 105°C."
        }

    def query_mechanics(self, query):
        """Consulta informações sobre mecânica"""
        for key in self.mechanics_data:
            if key in query.lower():
                return self.mechanics_data[key]
        return "Não encontrei informações específicas sobre mecânica para esta pergunta."

    def query_general(self, query):
        """Consulta informações gerais"""
        for key in self.general_data:
            if key in query.lower():
                return self.general_data[key]
        return "Não encontrei informações gerais para esta pergunta."

