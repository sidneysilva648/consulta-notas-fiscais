import os
import requests

def conectar_salesforce():
    try:
        from simple_salesforce import Salesforce
        sf = Salesforce(
            username=os.environ.get("SF_USERNAME"),
            password=os.environ.get("SF_PASSWORD"),
            security_token=os.environ.get("SF_SECURITY_TOKEN", ""),
            domain=os.environ.get("SF_DOMAIN", "login")
        )
        return sf
    except Exception as e:
        raise Exception(f"Erro ao conectar: {str(e)}")

def buscar_nota_fiscal(numero_nf: str):
    try:
        sf = conectar_salesforce()
        query = f"""
            SELECT Id, Name, NF_Number__c, Phone__c, 
                   Reference_Point__c, Status
            FROM Order
            WHERE NF_Number__c = '{numero_nf}'
            LIMIT 1
        """
        resultado = sf.query(query)
        registros = resultado.get("records", [])

        if not registros:
            return None, "Nota fiscal não encontrada."

        dados = registros[0]
        return {
            "numero_nf": numero_nf,
            "telefone": dados.get("Phone__c", "Não informado"),
            "ponto_referencia": dados.get("Reference_Point__c", "Não informado"),
            "status": dados.get("Status", "Não informado"),
            "nome": dados.get("Name", "Não informado"),
        }, None

    except Exception as e:
        return None, f"Erro: {str(e)}"
