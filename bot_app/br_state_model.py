from django.db import models

# Brazilian States, ordered by GDP
class BrazilianState(models.TextChoices):
    SAO_PAULO = 'SP', 'São Paulo'
    RIO_DE_JANEIRO = 'RJ', 'Rio de Janeiro'
    MINAS_GERAIS = 'MG', 'Minas Gerais'
    RIO_GRANDE_DO_SUL = 'RS', 'Rio Grande do Sul'
    PARANA = 'PR', 'Paraná'
    SANTA_CATARINA = 'SC', 'Santa Catarina'
    BAHIA = 'BA', 'Bahia'
    DISTRITO_FEDERAL = 'DF', 'Distrito Federal'
    GOIAS = 'GO', 'Goiás'
    PERNAMBUCO = 'PE', 'Pernambuco'
    PARA = 'PA', 'Pará'
    CEARA = 'CE', 'Ceará'
    MATO_GROSSO = 'MT', 'Mato Grosso'
    ESPIRITO_SANTO = 'ES', 'Espírito Santo'
    MATO_GROSSO_DO_SUL = 'MS', 'Mato Grosso do Sul'
    AMAZONAS = 'AM', 'Amazonas'
    MARANHAO = 'MA', 'Maranhão'
    RIO_GRANDE_DO_NORTE = 'RN', 'Rio Grande do Norte'
    PARAIBA = 'PB', 'Paraíba'
    ALAGOAS = 'AL', 'Alagoas'
    PIAUI = 'PI', 'Piauí'
    RONDONIA = 'RO', 'Rondônia'
    SERGIPE = 'SE', 'Sergipe'
    TOCANTINS = 'TO', 'Tocantins'
    AMAPA = 'AP', 'Amapá'
    ACRE = 'AC', 'Acre'
    RORAIMA = 'RR', 'Roraima'